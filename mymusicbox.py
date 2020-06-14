#!/bin/env python3
#from gpiozero import Button
from signal import pause
from subprocess import Popen
import vlc
from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import json

app = Flask("mbsrv") # musicbox server
CORS(app, resources={r"/*": {"origins": "*" }})
api = Api(app)


class Player:
    def __init__(self):
        self.radio_index = 0
        with open("stations.json","r") as f:
            self.radio_list = json.load(f)
        self.vlc_player = None
        self.stream_number = -1

    def change_volume(self, volume_change):
        new_vol = max(min(100, self.vlc_player.audio_get_volume() + volume_change),0)
        self.vlc_player.audio_set_volume(new_vol)

    def mute_volume(self):
        self.vlc_player.audio_set_mute(True)

    def unmute_volume(self):
        self.vlc_player.audio_set_mute(False)

    def increase_volume(self):
        self.change_volume(5)

    def decrease_volume(self):
        self.change_volume(-5)

    def next_stream(self):
        self.stream_number += 1
        if self.stream_number >= len(self.radio_list):
            self.stream_number = 0
        self.play(stream_number=self.stream_number)

    def previous_stream(self):
        self.stream_number -= 1
        if self.stream_number < 0:
            self.stream_number = len(self.radio_list)-1
        self.play(stream_number=self.stream_number)

    def play(self, stream_number=0):
        if self.vlc_player is not None:
            self.vlc_player.stop()
        self.vlc_player = vlc.MediaPlayer(self.radio_list[stream_number]["url"])
        self.vlc_player.play()
        self.stream_number = stream_number

    def stop(self, stream_number=0):
        if self.vlc_player is not None:
            self.vlc_player.stop()
        self.stream_number = -1

    def get_streams_list(self):
        response = jsonify(streams=self.radio_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'True')
        return response

    def get_stream_number(self):
        st_number = -1
        if self.vlc_player is not None:
            if self.vlc_player.is_playing() == 1:
                st_number = self.stream_number
        response = jsonify(stream_number=st_number)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'True')
        return response

pl = Player()

@app.route("/volume/up")
def volume_up():
    pl.increase_volume()
    return ''

@app.route("/volume/down")
def volume_down():
    pl.decrease_volume()
    return ''

@app.route("/volume/mute")
def volume_mute():
    pl.mute_volume()
    return ''

@app.route("/volume/unmute")
def volume_unmute():
    pl.unmute_volume()
    return ''

@app.route("/stop")
def stop():
    pl.stop()
    return ''

@app.route("/shutdown")
def shutdown():
    pl.stop()
    Popen(['shutdown', '-h', 'now' ])
    return ''

@app.route("/play/<int:stream_number>")
def play_stream(stream_number):
    pl.play(stream_number=stream_number)
    return ''

@app.route("/get_streams_list")
def get_streams_list():
    return pl.get_streams_list()

@app.route("/get_stream_number")
def get_stream_numer():
    return pl.get_stream_number()


# button_up = Button(5)
# button_up.when_pressed = increase_volume
# button_down = Button(7)
# button_down.when_pressed = decrease_volume
# button_down.when_held = mute_volume


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

    pause()

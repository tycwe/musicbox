# Description
Raspberry pi internet radio. \ 
Install, edit the list of your favorites radios in stations.json, plug an audio amplifier and loudspeaker, connect to musicbox.local and enjoy! \
you can now remote control, from any browser, your internet radios.

# Prerequisites
## Raspbian
Raspbian Lite image should be installed

# Raspberry Pi Configuration
Edit the raspberry hostname in /etc/hostname and /etc/hosts \
Assign (preferably)) a static IP address to the raspberry pi by
adding the following lines to /etc/dhcpcd.conf and reboot:

    interface eth0
    static ip_address=192.168.1.XX/24
    static routers=192.168.1.1
    static domain_name_servers=192.168.1.1

Update the password for pi user. \

## VLC (app & Python bindings)
sudo apt-get install alsa-base pulseaudio \
sudo apt-get install vlc \
pip3 install python-vlc

## Web server
sudo apt-get install python3-pip \
sudo apt-get install lighttpd \
sudo apt-get install python3-setup-tools \
pip3 install flask \
pip3 install flask-restful \
pip3 install flask-cors

# Installation
cp mymusicbox.py /home/pi/ \
cp stations.json /home/pi/ \
cp mymusicbox.html /var/www/html/index.html \
cp *.jpg /var/www/html/ \
cp *.gif /var/www/html/ \
cp favicon/* /var/www/html/ \
Note: the favicons were genrated automatically with https://www.favicon-generator.org/ \
cp mymusicbox.service /lib/systemd/system/

sudo chmod 644 /lib/systemd/system/ \
sudo systemctl daemon-reload \
sudo systemctl enable mymusicbox.service \
sudo systemctl start mymusicbox.service 

pulseaudio --start \

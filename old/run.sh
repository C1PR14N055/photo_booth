#!/bin/bash

sleep 20
# set display
export DISPLAY=:0
#set volume max
amixer sset 'PCM' 100% &
# remove mouse pointer
unclutter -idle 0.01 -root &
# start node
cd /home/pi/selphone/ && /usr/bin/nodejs srv.js & 
sleep 5
/usr/bin/python /home/pi/selphone/takepic.py &
sleep 5
# start chrome
chromium-browser --no-first-run --touch-events=enabled --fast --fast-start --disable-popup-blocking --disable-infobars --disable-session-crashed-bubble \
 --disable-tab-switcher --disable-translate --enable-low-res-tiling --noerrdialogs --incognito --start-fullscreen --use-fake-ui-for-media-stream --kiosk http://localhost:3000 &
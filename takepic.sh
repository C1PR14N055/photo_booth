#!/bin/bash

echo "Opening video stream..."
raspivid -hf -t -1 -w 1080 -h 1920 -o > /dev/null &
vidPID=$!
echo "Playing sound..."
omxplayer -o hdmi shutter.mp3 > /dev/null &
echo "Sleeping..."
sleep 6.5
echo "Slept..."
raspi2png --pngname "./pics/IMG-$( date '+%F-%H:%M:%S' ).png" &
sleep 1
echo "Took pic..."
kill -9 $vidPID
echo "Done"
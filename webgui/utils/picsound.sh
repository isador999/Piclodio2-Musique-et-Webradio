#!/bin/bash

usage(){
echo "picsound --debug"

echo "picsound --getDevice"
echo "picsound --getLevel"
echo "picsound --getSwitch"

echo "picsound --setDevice <0-3>"
echo "picsound --setLevel <0-100>"
echo "picsound --setSwitch <on|off>"
}

idPlaybackRoute=$(amixer controls | grep 'Playback Route' | cut -d'=' -f2 | cut -d',' -f1)
idPlaybackSwitch=$(amixer controls | grep 'Playback Switch' | cut -d'=' -f2 | cut -d',' -f1)
idPlaybackVolume=$(amixer controls | grep 'Playback Volume' | cut -d'=' -f2 | cut -d',' -f1)

currentDevice=$(amixer cget numid=$idPlaybackRoute | grep ': values=' | grep -oE '[0-2]')
currentLevel=$(amixer scontents|grep -oE '[0-9]+%'|grep -oE '[0-9]+')
currentSwitch=$(amixer cget numid=2 |grep ': values'|cut -d'=' -f2)

case $1 in
        --debug)
                amixer
                echo "----------------------------------------------------"
                amixer controls
                echo "----------------------------------------------------"
                echo idPlaybackRoute : $idPlaybackRoute
                echo idPlaybackSwitch : $idPlaybackSwitch
                echo idPlaybackVolume : $idPlaybackVolume
                echo "----------------------------------------------------"
                echo currentDevice : $currentDevice
                echo 0=auto, 1=analog, 2=hdmi
                echo currentLevel : $currentLevel
                echo currentSwitch : $currentSwitch
                echo "----------------------------------------------------"
                exit
                ;;
        --help)
                usage
                exit
                ;;
        --getDevice)
                echo $currentDevice;
                exit
                ;;
        --getLevel)
                echo $currentLevel;
                exit
                ;;
        --getSwitch)
                echo $currentSwitch;
                exit
                ;;
        --setLevel)
                amixer cset numid=$idPlaybackVolume $2%
                exit
                ;;
        --setDevice)
                amixer cset numid=$idPlaybackRoute $2
                exit
                ;;
        --setSwitch)
                amixer cset numid=$idPlaybackSwitch $2
                exit
                ;;
esac

echo "Bad arguments"
echo ""
echo "Help :"
usage
exit

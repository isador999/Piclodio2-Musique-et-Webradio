#!/bin/bash

usage(){
echo "picsound --debug"

echo "picsound --getDevice"
echo "picsound --getLevel"
echo "picsound --getSwitch"

echo "picsound --setDevice <0-3>"
echo "picsound --setLevel <0-100>"
echo "picsound --toggleSwitch"

echo "picsound --up <\d>"
echo "picsound --down <\d>"
}

getIdPlaybackRoute() { echo $(amixer controls | grep 'Playback Route' | cut -d'=' -f2 | cut -d',' -f1); }
getIdPlaybackSwitch() { echo $(amixer controls | grep 'Playback Switch' | cut -d'=' -f2 | cut -d',' -f1); }
getIdPlaybackVolume() { echo $(amixer controls | grep 'Playback Volume' | cut -d'=' -f2 | cut -d',' -f1); }

getCurrentDevice() { echo $(amixer cget numid=$(getIdPlaybackRoute) | grep ': values=' | grep -oE '[0-2]'); }
getCurrentLevel() { echo $(amixer scontents|grep -oE '[0-9]+%'|grep -oE '[0-9]+'); }
getCurrentSwitch() { echo $(amixer cget numid=$(getIdPlaybackSwitch) |grep ': values'|cut -d'=' -f2); }

case $1 in
        --debug)
                amixer
                echo "----------------------------------------------------"
                amixer controls
                echo "----------------------------------------------------"
                echo idPlaybackRoute : $(getIdPlaybackRoute)
                echo idPlaybackSwitch : $(getIdPlaybackSwitch)
                echo idPlaybackVolume : $(getIdPlaybackVolume)
                echo "----------------------------------------------------"
                echo currentDevice : $(getCurrentDevice)
                echo 0=auto, 1=analog, 2=hdmi
                echo currentLevel : $(getCurrentLevel)
                echo currentSwitch : $(getCurrentSwitch)
                echo "----------------------------------------------------"
                exit
                ;;
        --help)
                usage
                exit
                ;;
        --getDevice)
                echo $(getCurrentDevice)
                exit
                ;;
        --getLevel)
                echo $(getCurrentLevel)
                exit
                ;;
        --getSwitch)
                echo $(getCurrentSwitch)
                exit
                ;;
        --setLevel)
                amixer cset numid=$(getIdPlaybackVolume) $2%
                exit
                ;;
        --setDevice)
                amixer cset numid=$(getIdPlaybackRoute) $2
                exit
                ;;
        --toggleSwitch)
		if [ "$(getCurrentSwitch)" == "on" ]
		then
                	amixer cset numid=$(getIdPlaybackSwitch) off
		else
                	amixer cset numid=$(getIdPlaybackSwitch) on
		fi
                exit
                ;;
	--up)
		level=$(($(getCurrentLevel) + $2))
                amixer cset numid=$(getIdPlaybackVolume) $level%
		exit
		;;
	--down)
		level=$(($(getCurrentLevel) - $2))
                amixer cset numid=$(getIdPlaybackVolume) $level%
		exit
		;;
esac

echo "Bad arguments"
echo ""
echo "Help :"
usage
exit

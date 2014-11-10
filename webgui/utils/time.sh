#!/bin/bash

usage(){
echo ""
echo "To display current Time :"
echo "time --get"
echo ""
echo "To set Time :"
echo "time --set Hour:Minutes"
}


getCurrentTime() { echo $(date +'%H:%M'); }


case $1 in
        --help)
                usage
                exit
                ;;
        --get)
                echo $(getCurrentTime)
                exit
                ;;
        --set)
		date -s $2:$3
                exit
                ;;
esac

echo "Bad arguments"
echo ""
echo "Help :"
usage
exit

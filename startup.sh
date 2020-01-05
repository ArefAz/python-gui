#! /bin/bash
echo ------------------------------------ &>> i-drive.log
echo "starting i-drive..." &>> i-drive.log
date &>> i-drive.log
sudo killall -q -9 python 
cd /home/pi/i-drive/ 
export DISPLAY=:0
while true; do
    echo "starting program..." &>> i-drive.log 
    python main.pyc --fcw on  --ldw off --alaram on --regressor off --tracker off --gui off --save-fcw --save-input&>> i-drive.log
    echo "program ended (status: $?)" &>> i-drive.log
done

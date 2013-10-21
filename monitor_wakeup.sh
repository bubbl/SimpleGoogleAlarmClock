#!/bin/bash

cd /path/to/your/alarm/clock

running=`ps -ef | grep 'python wakeup.py' | grep -v 'grep' | wc -l`

if [ "$running" -eq "0" ]
then
    nohup python wakeup.py &
fi
if [ "$running" -eq "1" ]
then
    echo "Already running!"
fi

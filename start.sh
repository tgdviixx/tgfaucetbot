#!/usr/bin/env bash
# pip3 install -r requirements.txt
export LC_ALL="en_US.utf8"
echo "" >tg.log
#/usr/local/bin/python3.8
#python3
for pid in $(ps aux | grep -i 'python3 tgoktinit.py' | awk '{print $2}'); do kill $pid; done
nohup python3 tgoktinit.py > tg.log &
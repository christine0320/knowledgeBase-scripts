#!/bin/bash

# netstat -tulen | grep 27017 &>/dev/null
# mongoDBRes=$?
# echo ${mongoDBRes}
# 
# logFile=${HOME}/.local/ihefe/python.log
# 
# if [ ${mongoDBRes} != 0 ];then
# 	echo "Error: localhost has no mongodb listening in 27017." > ${logFile}
# 	exit -1;
# fi

# nohup python run.py &>>${logFile} &

## Source both just in case.
# Dev env.
#source ~/extern/env.sh
# Deploy env.
#source ~/.local/ihefe/extern/env.sh


# rm $(HOME)/.local/ihefe/ihefeMedImgCRM.log

if [ -f /tmp/uwsgi.pid ]; then
	uwsgi --reload /tmp/knowledgeBase.pid
else
	uwsgi --ini uwsgi.ini
fi


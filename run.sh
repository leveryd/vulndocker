#!/usr/bin/env bash
# start redis
PID=`/usr/sbin/lsof -i :6379|grep -v "PID" | awk '{print $2}'`
if [ "$PID" != "" ]; then
    echo "redis is runing!"
else
    docker run -d -p 6379:6379 redis
    echo "redis started!"
fi

# start dockertty
cd dockertty/src
PID=`/usr/sbin/lsof -i :9999|grep -v "PID" | awk '{print $2}'`
if [ "$PID" != "" ]; then
    echo "dockertty is runing!"
else
    sudo python dockertty.py -p 9999 &
    echo "dockertty started!"
fi

# start app
cd ../../
sudo python app.py
echo "app exit!"

#!/bin/bash

###########################################################
#File Name:
#Author: bahuafeng
#Mail: bahuafeng@gmail.com  
#Created Time: 2017-07-17 19:10:42
#Brief: 
#    instdown 服务控制脚本.
#    参考: http://zhaotao110.blog.sohu.com/258442991.html
###########################################################

root_dir=`pwd`
src_dir=$root_dir/src
SERVICE="instdown"
SERVICE_LOG="$root_dir/log/instdown.log"
SERVICE_PID=$root_dir/instdown.pid
python_bin=`which python`

start(){
    echo "starting..."
    cd $src_dir
    nohup $python_bin $src_dir/instdown_server.py > $SERVICE_LOG 2>&1 &
    if [ $? -ne 0 ]
    then 
        echo "start failed, please check the log!"
        tail -30 $SERVICE_LOG
        exit $?
    else
        echo $! > $SERVICE_PID  
        echo "start success" 
        cd $root_dir
    fi
}

debug(){
    echo "starting..."
    cd $src_dir
    nohup $python_bin $src_dir/instdown_server.py --debug > $SERVICE_LOG 2>&1 &   
    if [ $? -ne 0 ]
    then 
        echo "start failed, please check the log!"
        tail -30 $SERVICE_LOG
        exit $?
    else
        echo $! > $SERVICE_PID  
        echo "start success" 
        cd $root_dir
    fi
}

stop(){
    echo "stopping..."
    kill -9 `cat $SERVICE_PID` 
    if [ $? -ne 0 ]
    then 
        echo "stop failed, may be $SERVICE isn't running"
        exit $? 
    else 
        rm -rf $SERVICE_PID  
        echo "stop success" 
    fi
}

restart(){
    stop&&start
}

status(){
    num=`ps -ef | grep $SERVICE | grep -v grep | wc -l`
    if [ $num -eq 0 ]
    then 
        echo "$SERVICE isn't running"
    else
        echo "$SERVICE is running"
    fi
}

case $1 in     
    start)      start ;;   
    stop)       stop ;;   
    restart)    restart ;; 
    status)     status ;;
    debug)      debug ;;
    *)          echo "Usage: $0 {start|stop|restart|status}" ;;      
esac   

exit 0  

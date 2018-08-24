#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
echo $basepath
for i in $(seq 1 30);do
    echo $i
    process_id=`ps -ef|grep $1 |grep -v session_tracker.sh |grep -v sshpass|grep -v grep|awk '{print $2}'`
    echo $process_id
    if [[ ! -z $process_id ]];then
        echo "start run"
        strace -fp $process_id -t -o $basepath/../../log/ssh_audit_$2.log;
        break;
    fi
done

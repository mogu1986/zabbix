#!/bin/bash
domain=$1
para=$2
ret="/tmp/ping_ret_"$domain$para
/bin/ping  $domain -c 4 -w 10 >$ret
case $para in
     delay)
      result=`more $ret|grep rtt |awk -F "/"  '{print $5}'`
     if [ $result ];then
       echo $result
     else
       exit 
     fi
     ;;
    loss)
      grep loss $ret|awk -F "," '{print $3}' |awk -F "%" '{print $1}'
    ;;
    *)
    echo "please input two parameter,like www.baidu.com delay or loss"
esac
rm $ret

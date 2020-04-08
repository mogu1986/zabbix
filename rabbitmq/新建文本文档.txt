  181  rabbitmqctl set_user_tags zabbix monitoring
  182  rabbitmqctl set_permissions -p / zabbix '^aliveness-test$' '^amq\.default$' '^aliveness-test$'
  183  rabbitmqctl --h
  184  rabbitmqctl list_permissions


   72  df -h
   73  rabbitmqctl add_user zabbix evZ8CneJVBLGTlFG
   74  rabbitmqctl set_user_tags zabbix monitoring
   75  rabbitmqctl set_permissions -p / zabbix '^aliveness-test$' '^amq\.default$' '^aliveness-test$'


telnet.status[api.weixin.qq.com,80]


zabbix_sender -s "production-xcx01" -z 172.16.0.233 -p 10050 -k "trap" -o 1


PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
LogFileSize=0
ListenPort=10050
Server=172.16.0.233
ServerActive=172.16.0.233
Hostname=production-admin01
HostMetadataItem=system.uname
Include=/etc/zabbix/zabbix_agentd.d/*.conf
UnsafeUserParameters=1
Timeout=30
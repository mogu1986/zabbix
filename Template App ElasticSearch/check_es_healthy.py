import commands
command = 'curl 172.17.0.137:9200/_cat/health'
(a, b) = commands.getstatusoutput(command)
status= b.split(' ')[157]
if status=='red':
    healthy=0
else: 
    healthy=1

print healthy

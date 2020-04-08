#!/usr/bin/python
# -*- coding: utf-8 -*-


import jpype
from jpype import java
from jpype import javax
from jpype import *

import subprocess
import sys
import os


HOST='127.0.0.1'
PORT=sys.argv[3]
URL = "service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi" % (HOST, PORT)
#jpype.startJVM("/usr/local/jdk1.8.0_152/jre/lib/amd64/server/libjvm.so")
#jpype.startJVM("/usr/local/jdk/jre/lib/amd64/server/libjvm.so")
jpype.startJVM("/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.242.b08-0.el7_7.x86_64/jre/lib/amd64/server/libjvm.so")


jhash = java.util.HashMap()
jarray=jpype.JArray(java.lang.String)
jhash.put (javax.management.remote.JMXConnector.CREDENTIALS, jarray);
jmxurl = javax.management.remote.JMXServiceURL(URL)
jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl,jhash)
connection = jmxsoc.getMBeanServerConnection();

if sys.argv[1]=="java.lang:type=GarbageCollector,name=ConcurrentMarkSweep" or sys.argv[1]=="java.lang:type=OperatingSystem" or sys.argv[1]=="java.lang:type=Threading" or sys.argv[1]=="java.lang:type=GarbageCollector,name=ParNew":
    object=sys.argv[1]
    attribute=sys.argv[2]
    attr=connection.getAttribute(javax.management.ObjectName(object),attribute)
    print  attr
#elif "Tomcat" in sys.argv[1]:
elif "Catalina" in sys.argv[1]:
    object=sys.argv[1]
    attribute=sys.argv[2]
    attr=connection.getAttribute(javax.management.ObjectName(object),attribute)
    print  attr
elif sys.argv[1]=="process.num":
    args = "/usr/sbin/lsof -i :" + PORT + "|grep LISTEN|awk 'END {print}' |awk '{print $2}'"
    PID = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE).communicate()[0].replace("\n", "")
    argsnum = "ss -anp |grep " + PID + "|wc -l"
    num = subprocess.Popen(argsnum, shell=True, stdout=subprocess.PIPE).communicate()[0].replace("\n", "")
    print num
else:
    object = sys.argv[1]
    if sys.argv[2]=="Usage.max":
        attribute = "Usage"
        attr = connection.getAttribute(javax.management.ObjectName(object), attribute)
        print attr.contents.get("max")
    elif sys.argv[2] == "Usage.used":
        attribute = "Usage"
        attr = connection.getAttribute(javax.management.ObjectName(object), attribute)
        print attr.contents.get("used")
    elif sys.argv[2] == "HeapMemoryUsage.used":
        attribute = "HeapMemoryUsage"
        attr = connection.getAttribute(javax.management.ObjectName(object), attribute)
        print attr.contents.get("used")
    elif sys.argv[2] =="HeapMemoryUsage.committed":
        attribute = "HeapMemoryUsage"
        attr = connection.getAttribute(javax.management.ObjectName(object), attribute)
        print attr.contents.get("committed")
    elif sys.argv[2] == "HeapMemoryUsage.max":
        attribute = "HeapMemoryUsage"
        attr = connection.getAttribute(javax.management.ObjectName(object), attribute)
        print attr.contents.get("max")
    elif sys.argv[2] == "NonHeapMemoryUsage.used":
        attribute = "NonHeapMemoryUsage"
        attr = connection.getAttribute(javax.management.ObjectName(object), attribute)
        print attr.contents.get("used")
    elif sys.argv[2] == "NonHeapMemoryUsage.committed":
        attribute = "NonHeapMemoryUsage"
        attr = connection.getAttribute(javax.management.ObjectName(object), attribute)
        print attr.contents.get("committed")
    elif sys.argv[2] == "NonHeapMemoryUsage.max":
        attribute = "NonHeapMemoryUsage"
        attr = connection.getAttribute(javax.management.ObjectName(object), attribute)
        print attr.contents.get("max")

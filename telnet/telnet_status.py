#!/usr/bin/python  
import telnetlib,sys  
IP=sys.argv[1]  
PORT=sys.argv[2]  
try:  
        tn = telnetlib.Telnet(IP,PORT,timeout=10)  
        ok=tn.set_debuglevel(2)  
        print 1  
except:  
        print 0

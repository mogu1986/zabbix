#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

data = {
    "data":[
        {
            "{#JMXPORT}":"58080",
            "{#TOMCATPORT}":8080
        }
    ]
}


print(json.dumps(data, sort_keys=True, indent=2))

# print json.dumps(x,sort_keys=True,indent=4,separators=(',',':'))

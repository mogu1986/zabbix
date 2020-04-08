#!/bin/bash
ulimit -a |grep "open files" |awk '{print $NF}'

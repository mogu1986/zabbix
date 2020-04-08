#!/bin/bash
case $1 in
  cluster_name)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\" '/cluster_name/ {print $4}' ;;
  status)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\" 'NR==3 {print $4}' ;;
  timed_out)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==4 {print $1}' |awk -F: '{print $2}' ;;
  number_nodes)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==5 {print $1}' |awk -F: '{print $2}' ;;
  data_nodes)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==6 {print $1}' |awk -F: '{print $2}' ;;
  active_primary_shards)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==7 {print $1}' |awk -F: '{print $2}' ;;
  active_shards)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==8 {print $1}' |awk -F: '{print $2}' ;;
  relocating_shards)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==9 {print $1}' |awk -F: '{print $2}' ;;
  initializing_shards)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==10 {print $1}' |awk -F: '{print $2}' ;;
  unassigned_shards)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==11 {print $1}' |awk -F: '{print $2}' ;;
  delayed_unassigned_shards)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==12 {print $1}' |awk -F: '{print $2}' ;;
  number_of_pending_tasks)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==13 {print $1}' |awk -F: '{print $2}' ;;
  active_shards_percent_as_number)
      curl -s -XGET 'http://10.50.4.214:9200/_cluster/health?pretty' |awk -F\, 'NR==16 {print $1}' |awk -F: '{print $2}' ;;
    *)
      echo "Usage: $0 { cluster_name | status | timed_out | number_nodes | data_nodes | active_primary_shards | active_shards | relocating_shards | initializing_shards | unassigned_shards|delayed_unassigned_shards|number_of_pending_tasks|active_shards_percent_as_number}" ;;
esac

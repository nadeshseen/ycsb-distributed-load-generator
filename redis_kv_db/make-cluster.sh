ssh seen1@192.168.122.114 \
'
echo yes | redis-cli --cluster create 192.168.122.114:7000 192.168.122.114:7001 192.168.122.111:7002 192.168.122.111:7003 192.168.122.31:7004 192.168.122.31:7005 --cluster-replicas 1
'

# cluster-info
# redis-cli --cluster call 192.168.122.77:7000 info
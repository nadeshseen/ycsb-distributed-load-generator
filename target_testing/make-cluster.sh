ssh redis1@192.168.122.77 \
'
echo yes | redis-cli --cluster create 192.168.122.77:7000 192.168.122.77:7001 192.168.122.57:7002 192.168.122.57:7003 192.168.122.16:7004 192.168.122.16:7005 --cluster-replicas 1
'

# cluster-info
# redis-cli --cluster call 192.168.122.77:7000 info
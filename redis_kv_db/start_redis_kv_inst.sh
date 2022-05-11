ssh seen1@192.168.122.114 \
'
cd cluster-test/7000 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &
ssh seen1@192.168.122.114 \
'
cd cluster-test/7001 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &

ssh seen2@192.168.122.111 \
'
cd cluster-test/7002 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &
ssh seen2@192.168.122.111 \
'
cd cluster-test/7003 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &

ssh seen3@192.168.122.31 \
'
cd cluster-test/7004 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &
ssh seen3@192.168.122.31 \
'

cd cluster-test/7005 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &

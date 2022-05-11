ssh redis1@192.168.122.77 \
'
cd cluster-test/7000 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &
ssh redis1@192.168.122.77 \
'
cd cluster-test/7001 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &

ssh redis2@192.168.122.57 \
'
cd cluster-test/7002 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &
ssh redis2@192.168.122.57 \
'
cd cluster-test/7003 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &

ssh redis3@192.168.122.16 \
'
cd cluster-test/7004 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &
ssh redis3@192.168.122.16 \
'

cd cluster-test/7005 && 
rm -f appendonly.aof  dump.rdb  nodes.conf &&
redis-server ./redis.conf --protected-mode no
' &

# ssh redis1@192.168.122.132 \
# '
# pkill -f "redis-server"
# '
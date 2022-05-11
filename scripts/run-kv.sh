# Loading
# ssh seen1@192.168.122.114 'cd KV-replay && bin/kv-replay load redis -P workloads/replay_template -p "redis.host=192.168.122.77" -p "redis.port=7000" -p "redis.cluster=true"' > results/reportl_1.txt &
# ssh seen2@192.168.122.111 'cd KV-replay && bin/kv-replay load redis -P workloads/replay_template -p "redis.host=192.168.122.57" -p "redis.port=7002" -p "redis.cluster=true"' > results/reportl_2.txt &
# ssh seen3@192.168.122.31 'cd KV-replay && bin/kv-replay load redis -P workloads/replay_template -p "redis.host=192.168.122.16" -p "redis.port=7004" -p "redis.cluster=true"' > results/reportl_3.txt &

# Running
ssh seen1@192.168.122.114 'cd KV-replay && bin/kv-replay run redis -P workloads/replay_template -p "redis.host=192.168.122.77" -p "redis.port=7000" -p "redis.cluster=true"' > results/report_1.txt &
ssh seen2@192.168.122.111 'cd KV-replay && bin/kv-replay run redis -P workloads/replay_template -p "redis.host=192.168.122.57" -p "redis.port=7002" -p "redis.cluster=true"' > results/report_2.txt &
ssh seen3@192.168.122.31 'cd KV-replay && bin/kv-replay run redis -P workloads/replay_template -p "redis.host=192.168.122.16" -p "redis.port=7004" -p "redis.cluster=true"' > results/report_3.txt &


# ssh nadesh1@192.168.122.132 'redis-cli -p 6379 flushall'
# ssh seen1@192.168.122.114 'cd KV-replay && bin/kv-replay run redis -P workloads/replay_template -p "redis.host=192.168.122.132" -p "redis.port=6379"' > results/report_temp.txt
# ssh nadesh2@192.168.122.48 'cd KV-replay && bin/kv-replay run redis -P workloads/replay_template -p "redis.host=192.168.122.77" -p "redis.port=7000" -p "redis.cluster=true"' > results/report_1.txt
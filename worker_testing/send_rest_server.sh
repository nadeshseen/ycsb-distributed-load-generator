# scp -r cluster-test seen1@192.168.122.114:
# scp -r cluster-test seen2@192.168.122.111:
# scp -r cluster-test seen3@192.168.122.31:

scp rest_server.py seen1@192.168.122.114:KV-replay/
scp rest_server.py seen2@192.168.122.111:KV-replay/
scp rest_server.py seen3@192.168.122.31:KV-replay/

# scp ReplayWorkload.java seen1@192.168.122.114:KV-replay/core/src/main/java/com/yahoo/ycsb/workloads/ReplayWorkload.java
# scp ReplayWorkload.java seen2@192.168.122.111:KV-replay/core/src/main/java/com/yahoo/ycsb/workloads/ReplayWorkload.java
# scp ReplayWorkload.java seen3@192.168.122.31:KV-replay/core/src/main/java/com/yahoo/ycsb/workloads/ReplayWorkload.java

# scp ./hpdos_worker_rest_server.py ub-05@10.129.2.181:~/nadesh/worker_node/cppclient/YCSB/
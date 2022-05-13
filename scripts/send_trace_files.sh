# split -d -n l/3 1000_lines_rep.dat splitted_files/kv_trace_ &&
# echo "Enter number of instances : "
# read instances
# echo This is the thing guys $1
# echo $1 $2 $3
splitted_trace_file_name=kv_trace_$1.dat
# echo $splitted_trace_file_name
scp -r splitted_files/$splitted_trace_file_name $2@$3:$4/kv_trace.dat
var=$(wc -l splitted_files/$splitted_trace_file_name | awk '{print $1}')
# echo $var
splitted_trace_parameter_file_name=replay_$1
awk -v lines=${var} '{gsub("number_of_lines_in_trace",lines); print $0}' trace_workloads/replay_template > trace_workloads/$splitted_trace_parameter_file_name
scp -r trace_workloads/$splitted_trace_parameter_file_name $2@$3:$4/workload_template


# scp -r splitted_files/kv_trace_00.dat seen1@192.168.122.114:KV-replay/workloads/kv_trace.dat
# scp -r splitted_files/kv_trace_01.dat seen2@192.168.122.111:KV-replay/workloads/kv_trace.dat
# scp -r splitted_files/kv_trace_02.dat seen3@192.168.122.31:KV-replay/workloads/kv_trace.dat
# var=$(wc -l splitted_files/kv_trace_00.dat | awk '{print $1}')
# awk -v lines=${var} '{gsub("number_of_lines_in_trace",lines); print $0}' trace_workloads/replay_template > trace_workloads/replay_1
# var=$(wc -l splitted_files/kv_trace_01.dat | awk '{print $1}')
# awk -v lines=${var} '{gsub("number_of_lines_in_trace",lines); print $0}' trace_workloads/replay_template > trace_workloads/replay_2
# var=$(wc -l splitted_files/kv_trace_02.dat | awk '{print $1}')
# awk -v lines=${var} '{gsub("number_of_lines_in_trace",lines); print $0}' trace_workloads/replay_template > trace_workloads/replay_3
# scp -r trace_workloads/replay_1 seen1@192.168.122.114:KV-replay/workloads/replay_template
# scp -r trace_workloads/replay_2 seen2@192.168.122.111:KV-replay/workloads/replay_template
# scp -r trace_workloads/replay_3 seen3@192.168.122.31:KV-replay/workloads/replay_template

# ./run-kv.sh
# ssh nadesh2@192.168.122.48 'cd KV-replay && bin/kv-replay run redis -P workloads/replay_template -p "redis.host=127.0.0.1" -p "redis.port=6379" -p ' > results/report_2.txt &


splitted_trace_file_name=kv_trace_$1.dat
# echo $splitted_trace_file_name
scp -r splitted_files/$splitted_trace_file_name $2@$3:$4/kv_trace.dat
var=$(wc -l splitted_files/$splitted_trace_file_name | awk '{print $1}')
# echo $var
splitted_trace_parameter_file_name=replay_$1
awk -v lines=${var} '{gsub("number_of_lines_in_trace",lines); print $0}' trace_workloads/replay_template > trace_workloads/$splitted_trace_parameter_file_name
scp -r trace_workloads/$splitted_trace_parameter_file_name $2@$3:$4/workload_template
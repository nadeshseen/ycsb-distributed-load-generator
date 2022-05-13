# splitted_trace_file_name=kv_trace_0$(($1-1)).dat
# # echo $splitted_trace_file_name
# scp -r splitted_files/$splitted_trace_file_name $2@$3:KV-replay/workloads/kv_trace.dat
# var=$(wc -l splitted_files/$splitted_trace_file_name | awk '{print $1}')
# # echo $var
parameter_file_name=parameter_$1
# awk -v lines=${var} '{gsub("number_of_lines_in_trace",lines); print $0}' workloads/parameter_template > workloads/$parameter_file_name
scp -r workloads/$parameter_file_name $2@$3:$4/workload_template

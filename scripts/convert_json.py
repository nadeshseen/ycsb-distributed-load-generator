# from os import read
# from tabulate import tabulate
import json

# overall_insert = { "Operations":0, "Return=0":0, "Return=1":0, "AvgLatency":0, "MinLatency":99999999, "MaxLatency":0}
# overall_read = { "Operations":0, "Return=0":0, "Return=1":0, "AvgLatency":0, "MinLatency":99999999, "MaxLatency":0}
# overall_update = { "Operations":0, "Return=0":0, "Return=1":0, "AvgLatency":0, "MinLatency":99999999, "MaxLatency":0}
# overall_runtime = 0
# count=1
# table_rows = ["Operations", "ActualOps", "ExtraOps", "AvgLatency(us)", "MinLatency(us)", "MaxLatency(us)" ]
# overall_rows = ["Operations", "ActualOps", "ExtraOps", "Runtime(ms)", "Throughput(ops/sec)"]
# for i in range(count):

file_name = 'report_'+ str(1) +'.txt'
print("----------",file_name,"----------")
run_file = open('results/zipfian/3inst/'+file_name,'r')


insert_dict = {"Name":"Insert", "Operations":0, "Return=0":0, "Return=1":0}
read_dict = {"Name":"Read", "Operations":0, "Return=0":0, "Return=1":0}
update_dict = {"Name":"Update", "Operations":0, "Return=0":0, "Return=1":0}

run_file = str(output)
for row in run_file:
    row = row.split(', ')
    print(row)
    if row[0]=="[OVERALL]":
        if row[1]=="RunTime(ms)":
            per_vm_runtime = int(float(row[2][:-1]))
            # overall_runtime = max(overall_runtime, per_vm_runtime)
    
    if row[0]=="[READ]":
        if row[1]=="AverageLatency(us)":
            read_dict["AvgLatency"] = int(float(row[2][:-1]))
            # overall_read["AvgLatency"] += int(float(row[2][:-1]))
        
        if row[1]=="MinLatency(us)":
            read_dict["MinLatency"] = int(float(row[2][:-1]))
            # overall_read["MinLatency"] = min(overall_read["MinLatency"], int(float(row[2][:-1])))
        
        if row[1]=="MaxLatency(us)":
            read_dict["MaxLatency"] = int(float(row[2][:-1]))
            # overall_read["MaxLatency"] = max(overall_read["MaxLatency"], int(float(row[2][:-1])))
        
        if row[1]=="95thPercentileLatency(ms)":
            # read_dict["95thPercentileLatency"] = int(float(row[2][:-1]))
            pass
        
        if row[1]=="99thPercentileLatency(ms)":
            # read_dict["99thPercentileLatency"] = int(float(row[2][:-1]))
            pass
        
        if row[1]=="Operations":
            read_dict["Operations"] = int(float(row[2][:-1]))
            # overall_read["Operations"] += int(float(row[2][:-1]))
                    
        if row[1]=="Return=0":
            read_dict["Return=0"] = int(float(row[2][:-1]))
            # overall_read["Return=0"] += int(float(row[2][:-1]))                        
        
        if row[1]=="Return=1":
            read_dict["Return=1"] = int(float(row[2][:-1]))
            # overall_read["Return=1"] += int(float(row[2][:-1]))

    if row[0]=="[INSERT]":
        if row[1]=="AverageLatency(us)":
            insert_dict["AvgLatency"] = int(float(row[2][:-1]))
            # overall_insert["AvgLatency"] += int(float(row[2][:-1]))
        
        if row[1]=="MinLatency(us)":
            insert_dict["MinLatency"] = int(float(row[2][:-1]))
            # overall_insert["MinLatency"] = min(overall_insert["MinLatency"], int(float(row[2][:-1])))
        
        if row[1]=="MaxLatency(us)":
            insert_dict["MaxLatency"] = int(float(row[2][:-1]))
            # overall_insert["MaxLatency"] = max(overall_insert["MaxLatency"], int(float(row[2][:-1])))
        
        if row[1]=="95thPercentileLatency(ms)":
            # insert_dict["95thPercentileLatency"] = int(float(row[2][:-1]))
            # overall_insert["95thPercentileLatency"] = int(float(row[2][:-1]))
            pass
        
        if row[1]=="99thPercentileLatency(ms)":
            # insert_dict["99thPercentileLatency"] = int(float(row[2][:-1]))
            # overall_insert["99thPercentileLatency"] = int(float(row[2][:-1]))
            pass
        
        if row[1]=="Operations":
            insert_dict["Operations"] = int(float(row[2][:-1]))
            # overall_insert["Operations"] += int(float(row[2][:-1]))
                    
        if row[1]=="Return=0":
            insert_dict["Return=0"] = int(float(row[2][:-1]))
            # overall_insert["Return=0"] += int(float(row[2][:-1]))
                        
        if row[1]=="Return=1":
            insert_dict["Return=1"] = int(float(row[2][:-1]))
            # overall_insert["Return=1"] += int(float(row[2][:-1]))
    
    if row[0]=="[UPDATE]":
        if row[1]=="AverageLatency(us)":
            update_dict["AvgLatency"] = int(float(row[2][:-1]))
            # overall_update["AvgLatency"] += int(float(row[2][:-1]))
        
        if row[1]=="MinLatency(us)":
            update_dict["MinLatency"] = int(float(row[2][:-1]))
            # overall_update["MinLatency"] = min(overall_update["MinLatency"], int(float(row[2][:-1])))
        
        if row[1]=="MaxLatency(us)":
            update_dict["MaxLatency"] = int(float(row[2][:-1]))
            # overall_update["MaxLatency"] = max(overall_update["MaxLatency"], int(float(row[2][:-1])))
        
        if row[1]=="95thPercentileLatency(ms)":
            # update_dict["95thPercentileLatency"] = int(float(row[2][:-1]))
            # overall_update["95thPercentileLatency"] = int(float(row[2][:-1]))
            pass
        
        if row[1]=="99thPercentileLatency(ms)":
            # update_dict["99thPercentileLatency"] = int(float(row[2][:-1]))
            # overall_update["99thPercentileLatency"] = int(float(row[2][:-1]))
            pass
        
        if row[1]=="Operations":
            update_dict["Operations"] = int(float(row[2][:-1]))
            # overall_update["Operations"] += int(float(row[2][:-1]))
                    
        if row[1]=="Return=0":
            update_dict["Return=0"] = int(float(row[2][:-1]))
            # overall_update["Return=0"] += int(float(row[2][:-1]))
                        
        if row[1]=="Return=1":
            update_dict["Return=1"] = int(float(row[2][:-1]))
            # overall_update["Return=1"] += int(float(row[2][:-1]))


output_dict = {"Overall":per_vm_runtime,"Read":read_dict, "Insert":insert_dict, "Update":update_dict}
output_json = json.dumps(output_dict, indent=4)
print(output_json)

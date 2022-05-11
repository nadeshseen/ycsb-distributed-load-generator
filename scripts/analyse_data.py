# from os import read
from distutils.command.config import config
from tabulate import tabulate
import json
def analyse(config_filename, final_report_path):

    json_data_file =  open(config_filename)
    data = json.load(json_data_file)
    overall_insert = { "Operations":0, "Return=0":0, "Return=1":0, "AvgLatency":0, "MinLatency":99999999, "MaxLatency":0}
    overall_read = { "Operations":0, "Return=0":0, "Return=1":0, "AvgLatency":0, "MinLatency":99999999, "MaxLatency":0}
    overall_update = { "Operations":0, "Return=0":0, "Return=1":0, "AvgLatency":0, "MinLatency":99999999, "MaxLatency":0}
    overall_runtime = 0
    count = 0
    for machines in data["machines"]:
        if machines["status"]=="active":
            count+=1
    file_report = open(final_report_path, "w")
    table_rows = ["Operations", "ActualOps", "ExtraOps", "AvgLatency(us)", "MinLatency(us)", "MaxLatency(us)" ]
    overall_rows = ["Operations", "ActualOps", "ExtraOps", "Runtime(ms)", "Throughput(ops/sec)"]
    for machines in data["machines"]:
        if machines["status"]=="active":
            insert_dict = {"Operations":0, "Return=0":0, "Return=1":0}
            read_dict = {"Operations":0, "Return=0":0, "Return=1":0}
            update_dict = {"Operations":0, "Return=0":0, "Return=1":0}
            table_read = []
            table_insert = []
            table_update = []
            file_name = 'report_'+ str(machines["name"]) +'.txt'
            file_path = '../results/'
            # print("----------",file_name,"----------")
            val = "\n---------- "+file_name+" ----------\n"
            file_report.write(val)
            run_file = open(file_path+file_name,'r')
            for row in run_file:
                row = row.split(', ')
                # print(row)
                if row[0]=="[OVERALL]":
                    if row[1]=="RunTime(ms)":
                        per_vm_runtime = int(float(row[2][:-1]))
                        overall_runtime = max(overall_runtime, per_vm_runtime)
                
                if row[0]=="[READ]":
                    if row[1]=="AverageLatency(us)":
                        read_dict["AvgLatency"] = int(float(row[2][:-1]))
                        overall_read["AvgLatency"] += int(float(row[2][:-1]))
                    
                    if row[1]=="MinLatency(us)":
                        read_dict["MinLatency"] = int(float(row[2][:-1]))
                        overall_read["MinLatency"] = min(overall_read["MinLatency"], int(float(row[2][:-1])))
                    
                    if row[1]=="MaxLatency(us)":
                        read_dict["MaxLatency"] = int(float(row[2][:-1]))
                        overall_read["MaxLatency"] = max(overall_read["MaxLatency"], int(float(row[2][:-1])))
                    
                    if row[1]=="95thPercentileLatency(ms)":
                        # read_dict["95thPercentileLatency"] = int(float(row[2][:-1]))
                        pass
                    
                    if row[1]=="99thPercentileLatency(ms)":
                        # read_dict["99thPercentileLatency"] = int(float(row[2][:-1]))
                        pass
                    
                    if row[1]=="Operations":
                        read_dict["Operations"] = int(float(row[2][:-1]))
                        overall_read["Operations"] += int(float(row[2][:-1]))
                                
                    if row[1]=="Return=0":
                        read_dict["Return=0"] = int(float(row[2][:-1]))
                        overall_read["Return=0"] += int(float(row[2][:-1]))                        
                    
                    if row[1]=="Return=1":
                        read_dict["Return=1"] = int(float(row[2][:-1]))
                        overall_read["Return=1"] += int(float(row[2][:-1]))

                if row[0]=="[INSERT]":
                    if row[1]=="AverageLatency(us)":
                        insert_dict["AvgLatency"] = int(float(row[2][:-1]))
                        overall_insert["AvgLatency"] += int(float(row[2][:-1]))
                    
                    if row[1]=="MinLatency(us)":
                        insert_dict["MinLatency"] = int(float(row[2][:-1]))
                        overall_insert["MinLatency"] = min(overall_insert["MinLatency"], int(float(row[2][:-1])))
                    
                    if row[1]=="MaxLatency(us)":
                        insert_dict["MaxLatency"] = int(float(row[2][:-1]))
                        overall_insert["MaxLatency"] = max(overall_insert["MaxLatency"], int(float(row[2][:-1])))
                    
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
                        overall_insert["Operations"] += int(float(row[2][:-1]))
                                
                    if row[1]=="Return=0":
                        insert_dict["Return=0"] = int(float(row[2][:-1]))
                        overall_insert["Return=0"] += int(float(row[2][:-1]))
                                    
                    if row[1]=="Return=1":
                        insert_dict["Return=1"] = int(float(row[2][:-1]))
                        overall_insert["Return=1"] += int(float(row[2][:-1]))
                
                if row[0]=="[UPDATE]":
                    if row[1]=="AverageLatency(us)":
                        update_dict["AvgLatency"] = int(float(row[2][:-1]))
                        overall_update["AvgLatency"] += int(float(row[2][:-1]))
                    
                    if row[1]=="MinLatency(us)":
                        update_dict["MinLatency"] = int(float(row[2][:-1]))
                        overall_update["MinLatency"] = min(overall_update["MinLatency"], int(float(row[2][:-1])))
                    
                    if row[1]=="MaxLatency(us)":
                        update_dict["MaxLatency"] = int(float(row[2][:-1]))
                        overall_update["MaxLatency"] = max(overall_update["MaxLatency"], int(float(row[2][:-1])))
                    
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
                        overall_update["Operations"] += int(float(row[2][:-1]))
                                
                    if row[1]=="Return=0":
                        update_dict["Return=0"] = int(float(row[2][:-1]))
                        overall_update["Return=0"] += int(float(row[2][:-1]))
                                    
                    if row[1]=="Return=1":
                        update_dict["Return=1"] = int(float(row[2][:-1]))
                        overall_update["Return=1"] += int(float(row[2][:-1]))
                if row[0]=="[CPU_USAGE]":
                    # print("Average CPU Usage :", row[1])
                    val = "\nAverage CPU Usage :"+ row[1][:-1]+"%\n"
                    file_report.write(val)
                
                if row[0]=="[RAM_USAGE]":
                    # print("Average RAM Usage :", row[1])
                    val = "Average RAM Usage :"+ row[1]+"%\n"
                    file_report.write(val)
            
            if read_dict["Operations"]:
                # print("Read")
                for var in read_dict:
                    # print(var + " - "+ str(read_dict[var]))
                    table_read.append(str(read_dict[var]))
                # print()
            if insert_dict["Operations"]:
                # print("Insert")
                for var in insert_dict:
                    # print(var + " - "+ str(insert_dict[var])) 
                    table_insert.append(str(insert_dict[var]))
                # print()
            if update_dict["Operations"]:
                # print("Update")
                for var in update_dict:
                    # print(var + " - "+ str(update_dict[var])) 
                    table_update.append(str(update_dict[var]))
                # print()
            
            table = {file_name:table_rows, "Read":table_read, "Insert":table_insert, "Update":table_update}
            # print(tabulate(table, headers='keys', tablefmt='fancy_grid', disable_numparse=True))
            val = tabulate(table, headers='keys', tablefmt='fancy_grid', disable_numparse=True)+"\n"
            file_report.write(val)
            overall_values = []
            per_vm_ops=0
            per_vm_ops+=read_dict["Operations"]
            per_vm_ops+=insert_dict["Operations"]
            per_vm_ops+=update_dict["Operations"]
            overall_values.append(per_vm_ops)

            per_vm_actual_ops=0
            per_vm_actual_ops+=read_dict["Return=0"]
            per_vm_actual_ops+=insert_dict["Return=0"]
            per_vm_actual_ops+=update_dict["Return=0"]
            
            overall_values.append(per_vm_actual_ops)
            per_vm_extra_ops=0
            per_vm_extra_ops+=read_dict["Return=1"]
            per_vm_extra_ops+=insert_dict["Return=1"]
            per_vm_extra_ops+=update_dict["Return=1"]
            overall_values.append(per_vm_extra_ops)
            # print("Runtime(ms) : ", per_vm_runtime)

            overall_values.append(per_vm_runtime)
            per_vm_throughput = round(per_vm_ops*1000/per_vm_runtime, 2)
            # print("Throughput(ops/sec) : ", per_vm_throughput)
            
            overall_values.append(per_vm_throughput)
            overall_table = {file_name:overall_rows, "Overall":overall_values}
            # print(tabulate(overall_table, headers='keys', tablefmt='fancy_grid', disable_numparse=True))
            # print()
            # print("-------------ends-------------")
            # print()
            # print()
            
            val = tabulate(overall_table, headers='keys', tablefmt='fancy_grid', disable_numparse=True)+"\n"
            val += ("\n")
            val += ("\n-------------ends-------------\n")
            val += ("\n")
            val += ("\n")
            file_report.write(val)

    overall_read["AvgLatency"] = round(overall_read["AvgLatency"]/count, 2)
    overall_insert["AvgLatency"] = round(overall_insert["AvgLatency"]/count, 2)
    overall_update["AvgLatency"] = round(overall_update["AvgLatency"]/count, 2)

    table_read = []
    table_insert = []
    table_update = []

    if overall_read["Operations"]:
        flag=1
        for var in overall_read:
            if flag==1:
                # print("Total Read")
                flag=0
            # print(var + " - "+ str(overall_read[var]))
            table_read.append(str(overall_read[var]))
        # print()

    if overall_insert["Operations"]:
        flag=1
        for var in overall_insert:
            if flag==1:
                # print("Total Insert")
                flag=0
            # print(var + " - "+ str(overall_insert[var])) 
            table_insert.append(str(overall_insert[var]))
        # print()

    if overall_update["Operations"]:
        flag=1
        for var in overall_update:
            if flag==1:
                # print("Total Update")
                flag=0
            # print(var + " - "+ str(overall_update[var])) 
            table_update.append(str(overall_update[var]))
        # print()

    table = {"Combined":table_rows, "Read":table_read, "Insert":table_insert, "Update":table_update}
    # print(tabulate(table, headers='keys', tablefmt='fancy_grid', disable_numparse=True))

    val = tabulate(table, headers='keys', tablefmt='fancy_grid', disable_numparse=True)+"\n"
    file_report.write(val)
    overall_values = []
    total_ops=0
    total_ops+=overall_read["Operations"]
    total_ops+=overall_insert["Operations"]
    total_ops+=overall_update["Operations"]

    total_return_0=0
    total_return_0+=overall_read["Return=0"]
    total_return_0+=overall_insert["Return=0"]
    total_return_0+=overall_update["Return=0"]

    total_return_1=0
    total_return_1+=overall_read["Return=1"]
    total_return_1+=overall_insert["Return=1"]
    total_return_1+=overall_update["Return=1"]

    # print("Total Operations : ", total_ops)
    overall_values.append(total_ops)
    # print("Total Return=0 : ", total_return_0)
    overall_values.append(total_return_0)
    # print("Extra insert operations needed : ", total_return_1)
    overall_values.append(total_return_1)
    # print("Total Runtime(ms) : ", overall_runtime)
    overall_values.append(overall_runtime)
    # print("Total Throughput(ops/sec) : ", round(total_return_0*1000/overall_runtime, 2))
    overall_values.append(round(total_ops*1000/overall_runtime, 2))
    overall_table = {"Combined":overall_rows, "Overall":overall_values}
    # print(tabulate(overall_table, headers='keys', tablefmt='fancy_grid', disable_numparse=True))
    val = tabulate(overall_table, headers='keys', tablefmt='fancy_grid', disable_numparse=True)+"\n"
    file_report.write(val)
    print("Analysis Complete")


if __name__=="__main__":
    analyse()
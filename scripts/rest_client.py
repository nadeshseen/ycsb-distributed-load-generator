import requests
import json
from analyse_data import analyse
from generate_config_files import split_files
import subprocess
import threading
import time
import sys

config_filename = "dlg_config.json"
redis_config_filename = "redis_config.json"
kv_redis_config_filename = "kv_redis_config.json"

json_data_file =  open(config_filename)
data = json.load(json_data_file)
final_report_path = data["output_file"]


def call_split():

	print("Do you want to generate config files?(Y/N)")
	val = input()
	if val=="Y" or val=="y":
		print()
		print("Splitting Trace Files")
		split_files(config_filename)
		print()

def node_heartbeat(machines):
	while(1):
		try:
			worker_url = "http://" + machines["worker_node_ip"] + ":5000/heartbeat/"
			host_name = machines["worker_node_ip"]
			requests.get(url = worker_url)
			# print(host_name, "Working")
		except requests.exceptions.RequestException as e:
			print(host_name, "Not working")
			# print("Worker Node not working. Stopping Testing")
		time.sleep(2)

def heartbeat():
	# Iterate over list of machines
	# Get heartbeat for each machine via http/tcp or some communication protocol
	# Set the status of machine in machine_heartbeat_status dict
	heartbeat_threads = []
	for machines in data["machines"]:
		if machines["status"]=="active":
			# print(machines)
			heartbeat_threads.append(threading.Thread(target = node_heartbeat, args = [machines["command_parameters"]]))

	for host_thread in heartbeat_threads:
		host_thread.daemon = True
		host_thread.start()



def call_send_files():

	print("Do you want to send the files?(Y/N)")
	val = input()
	if val=="Y" or val=="y":

		for machines in data["machines"]:


			if machines["status"]=="active":
				parameters = machines["command_parameters"]
				command = "./send_cluster_info.sh"+" "+str(parameters["worker_node_username"]+" "+str(parameters["worker_node_ip"]+" "+config_filename))
				subprocess.run([command], shell=True)
				if machines["send_trace_file"]=="true":
					command = "./send_trace_files.sh"+" "+str(machines["name"])+ " "+ str(parameters["worker_node_username"]+" "+str(parameters["worker_node_ip"]))
					subprocess.run([command], shell=True)
				else:
					command = "./send_parameter_files.sh "+str(machines["name"])+ " "+ str(parameters["worker_node_username"]+" "+str(parameters["worker_node_ip"]))
					subprocess.run([command], shell=True)

def send_request(name, machines):
	worker_url = "http://" + machines["worker_node_ip"] + ":5000/workload"
	machines["phase"]="run"
	reply = requests.post(url = worker_url, json = machines)
	reply = reply.json()
		# Writing all reports to files
	file_lines = reply["data"].split("\\n")
	file_name = 'report_'+ str(name) +'.txt'
	file_path = '../results/'
	report = open(file_path+file_name, "w")
	for line in file_lines:
		report.writelines(line+"\n")
	report.writelines("[CPU_USAGE], "+reply["avg_cpu_usage"]+"\n")
	report.writelines("[RAM_USAGE], "+reply["avg_ram_usage"])
	report.close()

def call_send_run_request():
	print("Do you want to run the benchmark?(Y/N)")
	val = input()
	if val=="Y" or val=="y":
		request_threads = []
		for machines in data["machines"]:
			if machines["status"]=="active":
				# print(machines)
				request_threads.append(threading.Thread(target = send_request, args = [machines["name"], machines["command_parameters"]]))

		for host_thread in request_threads:
			host_thread.start()

		for host_thread in request_threads:
			host_thread.join()

		print("Run Phase Complete")

	
def load_request(name, machines):
	worker_url = "http://" + machines["worker_node_ip"] + ":5000/workload"
	machines["phase"]="load"
	reply = requests.post(url = worker_url, json = machines)
	reply = reply.json()
	# Writing all reports to files
	file_lines = reply["data"].split("\\n")
	file_name = 'load_report_'+ str(name) +'.txt'
	file_path = '../results/'
	report = open(file_path+file_name, "w")
	for line in file_lines:
		report.writelines(line+"\n")
	report.close()

def call_send_load_request():
	print("Do you want to load the data?(Y/N)")
	val = input()
	if val=="Y" or val=="y":
		request_threads = []
		for machines in data["machines"]:
			if machines["status"]=="active":
				if machines["command_parameters"]["phase"]=="load":
					request_threads.append(threading.Thread(target = load_request, args = [machines["name"], machines["command_parameters"]]))
					machines["command_parameters"]["phase"]="run"

		for host_thread in request_threads:
			host_thread.start()

		for host_thread in request_threads:
			host_thread.join()
		print("Load Phase Complete")

	

def call_analysis():
	print("Do you want a report of all the data?(Y/N)")
	val = input()
	if val=="Y" or val=="y":
		analyse(config_filename, final_report_path)

def clear_redis():
	print("Do you want to clear all data?(Y/N)")
	val = input()
	if val=="Y" or val=="y":
		print("Cleaing data from worker nodes redis instances")
		json_data_file =  open(kv_redis_config_filename)
		redis_data = json.load(json_data_file)
		# print(redis_data)
		for redis_machines in redis_data["redis_machines"]:
			
			if redis_machines["status"] == "master":
				# print(redis_machines)
				worker_url = "http://" + redis_machines["target_host"] + ":5000/clear_redis_nodes/"
				reply = requests.post(url = worker_url, json = redis_machines)
				reply = reply.json()
				print("Status : "+reply["status"])		

		print("Cleaning data from Target System")
		json_data_file =  open(redis_config_filename)
		redis_data = json.load(json_data_file)
		# print(redis_data)
		for redis_machines in redis_data["redis_machines"]:
			
			if redis_machines["status"] == "master":
				# print(redis_machines)
				worker_url = "http://" + redis_machines["target_host"] + ":5000/clear_redis_nodes/"
				reply = requests.post(url = worker_url, json = redis_machines)
				reply = reply.json()
				print("Status : "+reply["status"])

def testing():
	json_data_file =  open(kv_redis_config_filename)
	redis_data = json.load(json_data_file)
	redis_machines = redis_data["redis_machines"]
	# worker_url = "http://192.168.122.114:5000/insert/"
	# reply = requests.post(url = worker_url, json = redis_machines[0])
	# reply = reply.json()
	# print("Status : "+reply["status"])	
	worker_url = "http://192.168.122.111:5000/down/"
	json_post = {"key":"Aasdfasdf", "start_signal_sender_ip":"192.168.122.114"}
	# json_post = json.dumps(json_post)
	reply = requests.post(url = worker_url, json = json_post)
	reply = reply.json()
	print("Status : "+reply["status"])
	pass

if __name__ == "__main__":
	#start the heartbeat thread
	#Start the workload genereator
	#Check if heartbeat status is ok
	# heartbeat()
	clear_redis()
	# testing()
	
	call_split()
	call_send_files()
	# call_send_load_request()
	call_send_run_request()
	call_analysis()

	# time.sleep(10)
	sys.exit()
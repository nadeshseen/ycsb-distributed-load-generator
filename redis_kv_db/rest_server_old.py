from flask import Flask, request
import subprocess
import json
import requests
import time
import socket
from rediscluster import RedisCluster

app = Flask(__name__)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/insert/', methods=['GET', 'POST'])
def insert():
    # print("This is the response", request.json)
    print(request.json)
    startup_nodes = [{"host": "127.0.0.1", "port": "7000"}, {"host": "127.0.0.1", "port": "7001"}, {"host": "127.0.0.1", "port": "7002"}, {"host": "127.0.0.1", "port": "7003"}, {"host": "127.0.0.1", "port": "7004"}, {"host": "127.0.0.1", "port": "7005"}]
    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    rc.set("key","value1")
    str_val = "Redis "+request.json["target_host"]+" "+request.json["target_port"]+" inserted with key"
    response = {"status": str_val}
    output_json = json.dumps(response)
    return output_json

@app.route('/get/', methods=['GET', 'POST'])
def get():

    startup_nodes = [{"host": "127.0.0.1", "port": "7000"}, {"host": "127.0.0.1", "port": "7001"}, {"host": "127.0.0.1", "port": "7002"}, {"host": "127.0.0.1", "port": "7003"}, {"host": "127.0.0.1", "port": "7004"}, {"host": "127.0.0.1", "port": "7005"}]
    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    value = rc.get("key")
    str_val = "Redis "+request.json["target_host"]+" "+request.json["target_port"]+" got "+value+"for key"
    response = {"status": str_val}
    output_json = json.dumps(response)
    return output_json


@app.route('/clear_redis_nodes/', methods=['GET', 'POST'])
def clear_redis_nodes():
    # print("This is the response", request.json)

    output = subprocess.check_output("redis-cli -p "+request.json["target_port"]+" flushall", shell=True)
    output = output.decode("utf-8")
    str_val = "Redis "+request.json["target_host"]+" "+request.json["target_port"]+" cleared : "+output[:-1]
    response = {"status": str_val}
    output_json = json.dumps(response)
    return output_json

@app.route('/workload/', methods=['GET', 'POST'])
def run_workload():
    # print("This is the response", request.json)
    command = "./bin/kv-replay "+\
    request.json["phase"]+" "+ \
    request.json["target_system"]+" -P workloads/workload_template \
    -p '"+request.json["target_system"]+".host="+request.json["target_host"]+"' \
    -p '"+request.json["target_system"]+".port="+request.json["target_port"]+"' \
    -p '"+request.json["target_system"]+".cluster=true'"
    # print(command)
    # subprocess.Popen("python3 cpu_usage.py", shell=True)
    redis_url = "http://" +request.json["target_host"]+ ":5000/cpu_usage/"
    avg_cpu_usage = requests.get(url = redis_url)

    output = subprocess.check_output(command, shell = True)
    # print("asdfasdfsadfasdf")
    redis_url = "http://" +request.json["target_host"]+ ":5000/collect_data/"
    avg_cpu_usage = requests.get(url = redis_url)
    avg_cpu_usage = avg_cpu_usage.json()
    print(avg_cpu_usage)
    response = {}
    response["data"] = str(output)
    # print(str(output))
    response["avg_cpu_usage"] = avg_cpu_usage["avg_cpu_usage"]
    output_json = json.dumps(response)
    return output_json

@app.route('/heartbeat/', methods=['GET', 'POST'])
def run_heartbeat():
    # print(get_ip())
    response = {}
    response["Status"] = "Working"
    output_json = json.dumps(response)
    return output_json

@app.route('/same_worker_node/', methods=['GET', 'POST'])
def inter_process():
    request.json["sender_machine_ip"]=str(get_ip())
    print(request.json)

    if request.json["operation"] == "START_SIGNAL":
        print("Sending START_SIGNAL to", request.json["send_here"])
        worker_url = "http://" + request.json["send_here"] + ":5000/other_worker_node/"
        reply = requests.post(url = worker_url, json = request.json)
        reply = reply.json()
        print(reply)
        output_json = json.dumps(reply)
        time.sleep(10)
        return output_json
    elif request.json["operation"] == "WAIT_SIGNAL":
        file = open("cluster_info/coordination_"+ request.json["start_signal_sender_ip"] +".txt", "r")
        count=int(file.read())
        count-=1
        file.close()

        file = open("cluster_info/coordination_"+ request.json["start_signal_sender_ip"] +".txt", "w")
        file.write(str(count))
        file.close()
        print("Waiting for Start Signal from", request.json["start_signal_sender_ip"])
        # file.write(str(count))
        # file.close()
        while count!=0:
            file = open("cluster_info/coordination_"+ request.json["start_signal_sender_ip"] +".txt", "r")
            count=int(file.read())
            file.close()
            time.sleep(2)
        
        response = {}
        response["response_data"] = "Continue the trace"
        output_json = json.dumps(response)
        return output_json

@app.route('/other_worker_node/', methods=['GET', 'POST'])
def inter_machine():
    print(request.json)
    file = open("cluster_info/coordination_"+ request.json["sender_machine_ip"] +".txt", "r")
    count=int(file.read())
    count+=1
    file.close()
    file = open("cluster_info/coordination_"+ request.json["sender_machine_ip"] +".txt", "w")
    file.write(str(count))
    file.close()
    print(count)
    
    response = {}
    response["response_data"] = "Signal Sent"
    output_json = json.dumps(response)
    return output_json

if __name__ == '__main__':
    config_path = "cluster_info/"
    config_filename = "dlg_config.json"
    json_data_file =  open(config_path+config_filename)
    data = json.load(json_data_file)
    
    for machines in data["machines"]:
        file = open("cluster_info/coordination_"+ machines["command_parameters"]["worker_node_ip"] +".txt", "w")
        file.write(str(0))
        file.close()
    app.run(host='0.0.0.0', port=5000)

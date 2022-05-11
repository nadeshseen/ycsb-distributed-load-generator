from flask import Flask, request
import subprocess
import json
import requests
import time
import socket
from rediscluster import RedisCluster
import redis
from threading import Event
import logging

# logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = Flask(__name__)
event = Event()


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

@app.route('/event_wait/', methods=['GET', 'POST'])
def event_wait():
    event.wait()
    event.clear()
    print("Hello")
    response = {"status": "yuhuuu"}
    output_json = json.dumps(response)
    return output_json

@app.route('/event_set/', methods=['GET', 'POST'])
def event_set():
    event.set()
    print("Sent")
    response = {"status": "Informed the process waiting that i have made the changes"}
    output_json = json.dumps(response)
    return output_json

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
    does_exist = rc.exists("key")
    if does_exist:
        value = rc.get("key")
    else:
        value = "None"
    str_val = "Redis "+request.json["target_host"]+" "+request.json["target_port"]+" got "+value+"for key"
    response = {"status": str_val}
    output_json = json.dumps(response)
    return output_json


@app.route('/clear_redis_nodes/', methods=['GET', 'POST'])
def clear_redis_nodes():
    # print("This is the response", request.json)

    output = subprocess.check_output("redis-cli flushall", shell=True)
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
    redis_url = "http://" +request.json["target_host"]+ ":5000/resource_usage/"
    avg_cpu_usage = requests.get(url = redis_url)

    output = subprocess.check_output(command, shell = True)
    # print("asdfasdfsadfasdf")
    redis_url = "http://" +request.json["target_host"]+ ":5000/collect_data/"
    avg_resource_usage = requests.get(url = redis_url)
    avg_resource_usage = avg_resource_usage.json()
    print(avg_resource_usage)
    response = {}
    response["data"] = str(output)
    # print(str(output))
    response["avg_cpu_usage"] = avg_resource_usage["avg_cpu_usage"]
    response["avg_ram_usage"] = avg_resource_usage["avg_ram_usage"]
    output_json = json.dumps(response)
    return output_json
    # return avg_resource_usage

@app.route('/heartbeat/', methods=['GET', 'POST'])
def run_heartbeat():
    # print(get_ip())
    response = {}
    response["Status"] = "Working"
    output_json = json.dumps(response)
    return output_json

@app.route('/up/', methods=['GET', 'POST'])
def up():
    print(request.json)
    my_ip = str(get_ip())
    key = request.json["key"]
    send_here = request.json["send_here"]
    transaction = {}
    transaction["value"] = my_ip+"_"+key+"_"+send_here
    redis_up = "http://" +send_here+ ":5000/send_up/"
    # print(transaction)
    response_some = requests.post(url = redis_up, json=transaction)
    
    # print(response_some)
    # print(response_some.json())
    # response ={"tmp": "val"}
    # response = json.dumps(response)
    # print(response)
    return response_some.json()

@app.route('/send_up/', methods=['GET', 'POST'])
def send_up():
    rc = redis.Redis(host="localhost", port="6379", decode_responses=True)
    print(request.json)
    new_key = request.json["value"]

    does_exist = rc.exists(new_key)
    if does_exist:
        value = int(rc.get(new_key))
        rc.set(new_key, value+1)
    else:
        rc.set(new_key, 1)

    send_here_url = "http://localhost:5000/event_set/"
    event_set_res = requests.get(url = send_here_url)

    response = {"status": new_key+" "+rc.get(new_key)}
    response = json.dumps(response)
    return response

@app.route('/down/', methods=['GET', 'POST'])
def down():
    # startup_nodes = [{"host": "127.0.0.1", "port": "7000"}, {"host": "127.0.0.1", "port": "7001"}, {"host": "127.0.0.1", "port": "7002"}, {"host": "127.0.0.1", "port": "7003"}, {"host": "127.0.0.1", "port": "7004"}, {"host": "127.0.0.1", "port": "7005"}]
    rc = redis.Redis(host="localhost", port="6379", decode_responses=True)
    print(request.json)

    sent_from = request.json["start_signal_sender_ip"]
    key = request.json["key"]
    my_ip = str(get_ip())
    new_key = sent_from+"_"+key+"_"+my_ip
    does_exist = rc.exists(new_key)
    if does_exist:
        value = int(rc.get(new_key))
        rc.set(new_key, value-1)
    else:
        rc.set(new_key, -1)
    
    while rc.get(new_key)!="0":
        print("waiting")
        event.wait()
        event.clear()

    response = {"status": new_key+" "+rc.get(new_key)}
    response = json.dumps(response)
    return response

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
    app.run(host='0.0.0.0', port=5000)

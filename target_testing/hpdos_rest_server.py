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

    command = "./bin/ycsb run hpdos -P workloads/workloada"
    # print(command)
    # subprocess.Popen("python3 cpu_usage.py", shell=True)
    target_url = "http://" +request.json["target_host"]+ ":5002/resource_usage/"
    avg_cpu_usage = requests.get(url = target_url)

    output = subprocess.check_output(command, shell = True)
    # print("asdfasdfsadfasdf")
    target_url = "http://" +request.json["target_host"]+ ":5002/collect_data/"
    avg_resource_usage = requests.get(url = target_url)
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
    redis_up = "http://" +send_here+ ":5002/send_up/"
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

    send_here_url = "http://localhost:5002/event_set/"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

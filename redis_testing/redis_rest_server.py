from flask import Flask, request
import subprocess
import json

app = Flask(__name__)

@app.route('/clear_redis_nodes/', methods=['GET', 'POST'])
def clear_redis_nodes():
    # print("This is the response", request.json)

    output = subprocess.check_output("redis-cli -p "+request.json["target_port"]+" flushall", shell=True)
    output = output.decode("utf-8")
    str_val = "Redis "+request.json["target_host"]+" "+request.json["target_port"]+" cleared : "+output[:-1]
    response = {"status": str_val}
    output_json = json.dumps(response)
    return output_json

@app.route('/resource_usage/', methods=['GET', 'POST'])
def run_resource_usage():
    # print("This is the response", request.json)
    subprocess.Popen("python3 resource_usage.py", shell=True)
    response = {"status":"Resource Usage started"}
    output_json = json.dumps(response)
    return output_json

@app.route('/collect_data/', methods=['GET', 'POST'])
def run_collect_data():
    # print("This is the response", request.json)
    subprocess.run("pkill -f resource_usage.py", shell=True)
    avg_cpu = subprocess.check_output("awk '{s+=$1}END{print (NR?s/NR:\"NaN\")}' cpu_usage.txt", shell=True)
    avg_cpu = avg_cpu.decode("utf-8")
    avg_cpu = str(avg_cpu[:-1])
    avg_ram = subprocess.check_output("awk '{s+=$1}END{print (NR?s/NR:\"NaN\")}' ram_usage.txt", shell=True)
    avg_ram = avg_ram.decode("utf-8")
    avg_ram = str(avg_ram[:-1])
    print(avg_ram)
    print(avg_cpu)
    response = {}
    response["avg_cpu_usage"] = avg_cpu
    response["avg_ram_usage"] = avg_ram
    output_json = json.dumps(response)
    return output_json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

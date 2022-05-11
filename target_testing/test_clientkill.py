import requests

worker_url = "http://192.168.122.77:5000/collect_data/"
reply = requests.get(url = worker_url)
reply = reply.json()
print(reply)

worker_url = "http://192.168.122.57:5000/collect_data/"
reply = requests.get(url = worker_url)
reply = reply.json()
print(reply)

worker_url = "http://192.168.122.16:5000/collect_data/"
reply = requests.get(url = worker_url)
reply = reply.json()
print(reply)
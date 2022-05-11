import requests
redis_url = "http://192.168.122.77:5000/cpu_usage/"
reply = requests.get(url = redis_url)

redis_url = "http://192.168.122.57:5000/cpu_usage/"
reply = requests.get(url = redis_url)

redis_url = "http://192.168.122.16:5000/cpu_usage/"
reply = requests.get(url = redis_url)
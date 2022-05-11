import psutil
import time 

cpu_file = open("cpu_usage.txt", "w")
cpu_file.truncate(0)
cpu_file.close()
file = open("ram_usage.txt", "w")
file.truncate(0)
file.close()
while True:
    cpu_file = open("cpu_usage.txt", "a")
    ram_file = open("ram_usage.txt", "a")
    CPU_Pct=str(psutil.cpu_percent(0))
    RAM_Pct=str(psutil.virtual_memory().percent)
    
    cpu_file.write(CPU_Pct + "\n")
    cpu_file.close()
    ram_file.write(RAM_Pct + "\n")
    ram_file.close()
    time.sleep(1)

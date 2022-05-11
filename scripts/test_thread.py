import threading
import time
import sys

def heartbeat(a,b):
    print(a,b)
    # while 1:
    print("hey")
    time.sleep(0.5)

if __name__=="__main__":
    a="nad"
    b="seen"
    threads = []
    for i in range(2):
        threads.append(threading.Thread(target=heartbeat, args=["nad", "s"]))
    
    for i in range(2):
        threads[i].start()


    # t1.daemon = True
    # t1.start()
    print("hello")
    # time.sleep(10)
    # sys.exit()
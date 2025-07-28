import requests, time, threading, random

def termometer(id): 
    while True:
        time.sleep(5)
        requests.post('http://receiver:3000/data', json={"value": random.randint(18, 25), "timestamp": time.time(), "device_id": id})

t1 = threading.Thread(None, termometer, args='1') # target e funkciq args sa argumenti koito pra6tame a funkciqta
t2 = threading.Thread(None, termometer, args='2')
t3 = threading.Thread(None, termometer, args='3')

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
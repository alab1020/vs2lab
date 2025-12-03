import zmq
import time
import pickle
import constPipe
import random 

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind(f"tcp://127.0.0.1:{constPipe.SPLITTER_OUT_PORT}")

sentences = [
    "Hello world",
    "This is a test",
    "ZeroMQ is great",
    "Python is awesome",
    "Distributed systems are fun",
    "Concurrency is key",
    "Network programming is interesting",
    "Data processing is important",
    "Load balancing is essential",
    "Scalability matters",
    "Fault tolerance is crucial",
    "Performance optimization is necessary",
    "Security is vital",
    "APIs are useful",
    "Microservices are popular",
    "Cloud computing is the future",
    "Labor Abgabe ist spannend",
    
]

print("Splitter started...")  
time.sleep(1)  

for i in range(25):  
    msg = random.choice(sentences)
    print(f"Splitter sent: {i+1}:{msg}")  
    time.sleep(0.5)
    socket.send(pickle.dumps(msg))

socket.close()

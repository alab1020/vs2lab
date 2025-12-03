import zmq
import sys
import pickle
import constPipe

me = sys.argv[1] 
port = constPipe.REDUCER1_PORT if me == "1" else constPipe.REDUCER2_PORT 

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind(f"tcp://*:{port}") 

counts = {}  # normales dict statt defaultdict

print(f"Reducer {me} started on port {port}...")

while True:
    try:
        msg = socket.recv()
        word = pickle.loads(msg)
        
        # Prüfe: existiert das Wort schon?
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
        
        print(f"Reducer {me}: {word} : {counts[word]}")
    except Exception as e:
        print(f"Error in Reducer {me}: {e}")
        break


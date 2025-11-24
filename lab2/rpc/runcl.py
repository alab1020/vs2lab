import rpc
import logging
import time

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

def cb(result_list):
    print("Result: {}".format(result_list.value))

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, cb)

print("Waiting for response")
i = 0
while i < 15:
    print(i)
    time.sleep(1)
    i += 1

cl.stop()

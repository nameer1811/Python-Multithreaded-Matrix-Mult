import sys, threading
from producer import producer
from consumer import consumer
from shared_buffer import shared_buffer
from random import randint
import time
from math import floor
import numpy as np

# default settings
settings = {"M" : 10,
            "N" : 10,
            "P" : 10,
            "MaxBuffSize" : 5,
            "SplitSize" : 3,
            "NumConsumer" : 2,
            "MaxProducerSleepTime" : 20,
            "MaxConsumerSleepTime" : 80 }

# load in file
try:
    for l in open(sys.argv[1],"r"):
        flag_pos = [i for i, c in enumerate(l) if c == "<" or c == ">"]
        key = l[flag_pos[0]+1:flag_pos[1]]
        val = l[flag_pos[2]+1:flag_pos[3]]

        settings[key] = int(val)
except:
    print("Invalid File, using default variables")

# setting all default variables after loading
M = settings["M"]
N = settings["N"]
P = settings["P"]
MaxBuffSize = settings["MaxBuffSize"]
SplitSize = settings["SplitSize"]
NumConsumer = settings["NumConsumer"]
MaxProducerSleepTime = settings["MaxProducerSleepTime"]
MaxConsumerSleepTime = settings["MaxConsumerSleepTime"]

# generate random integer matrices
# A = MxN, B = NxP
A = [[randint(0,9) for n in range(N)] for m in range(M)]
B = [[randint(0,9) for p in range(P)] for n in range(N)]

# Keep track of execution time
start_time = time.time()

# create one producer and one consumer thread
buffer = shared_buffer(MaxBuffSize)
prod = producer(SplitSize,MaxProducerSleepTime,A,B,buffer)
consumers = [consumer(MaxConsumerSleepTime,buffer) for _ in range(NumConsumer)]
consumer_threads = [threading.Thread(target=cons.run) for cons in consumers]
producer_thread = threading.Thread(target=prod.run)

for con_thread in consumer_threads:
    con_thread.start()
producer_thread.start()

# put main thread to sleep until the product/consumer thread is complete
producer_thread.join()

# consumer thread no longer has to loop since we finished the product thread, still sleep until all of them are finished processing their inputs though
for id, con_thread in enumerate(consumer_threads):
    consumers[id].done = True
    con_thread.join()

# print the final result
print("--------------------------------------------------------------------------------")
print("Result of Program")
result = prod.matrix_c
print(np.array(result))

# verify it
matrix_mul = enumerate(np.matmul(A,B))
verification = all([all([val == result[y][x] for x, val in enumerate(row)]) for y, row in matrix_mul])
print("result verified" if verification else "incorrect result")

# print statistics
sleep_times = sum([cons.sleep_times for cons in consumers],[])+prod.sleep_times
avg_time = floor(sum(sleep_times)/len(sleep_times))
max_time = max(sleep_times)

print("--------------------------------------------------------------------------------")
print("PRODUCER / CONSUMER SIMULATION RESULT")
print("Simulation Time: ".ljust(35), (str(floor((time.time()-start_time)*1000)))+"ms")
print("Average Thread Sleep Time: ".ljust(35), (str(avg_time)+"ms"))
print("Maximum Thread Sleep Time: ".ljust(35), (str(max_time)+"ms"))
print("Number of Producer Threads: ".ljust(35),"1")
print(f"Number of Consumer Threads: ".ljust(35),len(consumers))
print("Size of Buffer: ".ljust(35),MaxBuffSize)
print("Total Number of Items Produced: ".ljust(35),prod.work_items_count)
print("Total Number of Items Consumed: ".ljust(35),sum([cons.consumed_items for cons in consumers]))
print("Number Of Times Buffer Was Full: ".ljust(35),buffer.full_count)
print("Number Of Times Buffer Was Empty: ".ljust(35),buffer.empty_count)
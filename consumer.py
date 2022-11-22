import numpy as np
from random import randint
import time
from functools import reduce

# ensures that printing in parallel doesn't overlap
def custom_print(*args):
    print(reduce(lambda x, y : str(x)+"\n"+str(y),args))

class consumer:
    def __init__(self,MaxConsumerSleepTime,shared_buffer):
        # receives shared buffer and max consumer sleep time paramter
        self.MaxConsumerSleepTime = MaxConsumerSleepTime
        self.shared_buffer = shared_buffer
        self.consumed_items = 0 # counter
        self.sleep_times = []
        self.done = False
    
    def run(self):
        while not self.done:
            # calculate the matrix mulitplication of the subrows and subrows of A and B respectively
            item = self.shared_buffer.get()

            # log that the consumer has gotten an item and is going to start processing it
            custom_print("--------------------------------------------------------------------------------", 
            f"Consumer gets row {item.low_a}-{item.high_a} of matrix A and column {item.low_b}-{item.high_b} of B from the buffer", 
            f"Consumer finishes calculating")

            # get the actual product of the item and store it
            product = np.dot(item.sub_a,item.sub_b)
            item.sub_c = product
            item.done = True

            # output a message of completion
            custom_print("--------------------------------------------------------------------------------",
            np.array(item.sub_a),"x",np.array(item.sub_b),f"= {product}")
            
            # keep track of stats and make the thread sleep 
            self.consumed_items += 1
            sleep_time = randint(0,self.MaxConsumerSleepTime)
            time.sleep(sleep_time/1000)
            self.sleep_times.append(sleep_time)
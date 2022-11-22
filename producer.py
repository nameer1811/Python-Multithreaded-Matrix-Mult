from random import randint
from work_item import work_item
from math import ceil
import time

# A = MxN, B = NxP
# split matrices into sub-rows and sub-columns, put into shared queue

class producer:
    # receives shared buffer and the two matrices
    def __init__(self,SplitSize,MaxProducerSleepTime,matrix_a,matrix_b,shared_buffer):
        self.SplitSize = SplitSize
        self.MaxProducerSleepTime = MaxProducerSleepTime
        self.matrix_a = matrix_a
        self.matrix_b = matrix_b
        
        # the resulting matrix is MxP
        self.matrix_c = [[0 for p in range(len(matrix_b[0]))] for m in range(len(matrix_a))]
        self.shared_buffer = shared_buffer
        self.work_items_count = 0
        self.working_items = []
        self.sleep_times = []

    def run(self):
        # split the m rows of matrix a and split the p columns of matrix b using the split size parameter
        for sub1 in range(ceil(len(self.matrix_a)/self.SplitSize)):
            # generating subsets of the rows in matrix a
            low_a  = sub1*self.SplitSize
            high_a = min(len(self.matrix_a),(sub1+1)*self.SplitSize)
            a_subset = self.matrix_a[low_a:high_a]

            for sub2 in range(ceil(len(self.matrix_b[0])/self.SplitSize)):
                # grabbin of the columns in matrix b
                low_b  = sub2*self.SplitSize
                high_b = min(len(self.matrix_b[0]),(sub2+1)*self.SplitSize)
                b_subset = [[self.matrix_b[r][c] for c in range(low_b,high_b)] for r in range(len(self.matrix_b))]

                # put a new work item into the shared buffer
                print("--------------------------------------------------------------------------------")
                print(f"Producer puts row {low_a}-{high_a} of matrix A and column {low_b}-{high_b} of B to buffer")
                item = work_item(a_subset,b_subset,low_a,high_a,low_b,high_b)
                self.working_items.append(item)
                self.shared_buffer.put(item)

                # Make the thread sleep
                sleep_time = randint(0,self.MaxProducerSleepTime)
                time.sleep(sleep_time/1000)

                # keep track of stats
                self.sleep_times.append(sleep_time)
                self.work_items_count += 1

        # for each completed work item, add its subc to the final result matrix c
        while len(self.working_items) > 0:
            for item in self.working_items:
                if item.done:
                    self.working_items.remove(item)
                    
                    # subbing in for its location based on the subset the item received
                    for y, row in enumerate(item.sub_c):
                        for x, value in enumerate(row):
                            self.matrix_c[y+item.low_a][x+item.low_b] = value

        # producer thread done, exit and print stats
        self.shared_buffer.complete()
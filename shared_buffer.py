import threading

class shared_buffer:
# Thread sychronization methods here
    def __init__(self,max_buffer_size):
        self.max_buffer_size = max_buffer_size

        # array the size of max buffer size
        self.workitem_array = []
        self.full_count  = 0
        self.empty_count = 0
        
        # for sychronization and mutex implementation
        self.condition = threading.Condition()
    
    # producer thread uses this to put a new workitem into the shared buffer
    def put(self,item):
        # keep track of how many times the internal buffer is full or empty
        self.full_count  += (len(self.workitem_array) == self.max_buffer_size)
        self.condition.acquire()

        # wait until the workitem array isn't full so we can put an item in it
        if (len(self.workitem_array) == self.max_buffer_size):
            self.condition.wait()
        
        self.workitem_array.append(item)

        # tell the get thread there's now an element in the list to use
        self.condition.notify()
        self.condition.release()

    # used by consumer to get a workitem from the shared buffer
    def get(self):
        # keep track of how many times the internal buffer is full or empty
        self.empty_count += (len(self.workitem_array) == 0)
        self.condition.acquire()

        # wait until the workitem array isn't empty
        if (len(self.workitem_array) == 0):
            self.condition.wait()

        # tell the put thread that it doesn't have to wait anymore for a work item
        self.condition.notify()
        self.condition.release()

        return self.workitem_array.pop()
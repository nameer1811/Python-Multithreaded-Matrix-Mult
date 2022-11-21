
class work_item:
    def __init__(self,sub_a,sub_b,low_a,high_a,low_b,high_b):
        self.sub_a = sub_a 
        self.sub_b = sub_b
        self.sub_c = [] # result of sub_axsub_b

        # The low and high row indexes of the sub-rows copied from matrix _a and _b
        self.low_a, self.low_b   = low_a, low_b
        self.high_a, self.high_b = high_a, high_b

        self.done = False


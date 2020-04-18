from heapq import *
# from traffic import *
import random
import math
import time

debug = True #flag to debug

class Event:
    def __init__(self, timestamp, data):
        self.timestamp = timestamp
        self.type = data['type']
        self.data = data


# Interval between arrivals averaging mean seconds (5)
def random_exp(mean):
    return random.expovariate(1/mean)


def schedule(queue, time, event):
    heappush(queue, (time,event))




def run_sim(q):
    print "running"
    while(q):
        curr = heappop(q)
        global now
        now = curr[0]
        curr_event = curr[1]
        if curr_event.type == "arrival":
            arrival(curr_event, q)
        elif curr_event.type == "through":
            cross(curr_event, q)
        elif curr_event.type == "departure":
            departure(curr_event)

        #call event handler relative to curr_event

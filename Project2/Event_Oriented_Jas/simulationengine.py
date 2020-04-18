from heapq import *
# from traffic import *
import random
import math
import time
import csv

debug = False #flag to debug
#northbound signal timings
#G LT, Y LT, R LT, G TR, Y TR, R TR/LT

signal_time_NB = {10:(34.7,3.6,49.3),
                11: (41.5, 3.2,55.4),
                12: (60.9,3.2,35.7),
                13: (0,0,0),
                14:(34.6,3.2,46.1)}

intersection_x_times = {10: 3.49,
                      11:4.54,
                      12:2.58,
                      13:2.34,
                      14: 4.12}

section_traverse_times = {(10,11): 15.45,
                      (11,12):14.42,
                      (12,14):24.42}

class Event:
    def __init__(self, timestamp, data):
        self.timestamp = timestamp
        self.id = data['vehicle_id']
        self.type = data['type']
        self.to_cross = data['next'] #intersection that needs to be crossed next (starts of as 10th)
        self.start = data['start']
        self.data = data
        self.latest = timestamp



#State variables  and other global information

# Simulation constants; all times in seconds
# A = mean interarrival time (in seconds, between cars)


A = 12.0
filename = "{0} OutputData.csv".format(int(A))

Cutoff = 1000 #number of cars to simulate
#State Variables of Simulation
waiting_counts = {10:0, 11:0, 12:0, 13:0, 14:0} #pre_X
waiting_time = {10:0, 11:0, 12:0, 13:0, 14:0}
# pre_X = 0	            # cars waiting to use intersection

#Eventually, there will be a variable per lane per intersection
ArrivalCount=0	        #number of arrivals simulated; used for termination

# State variables used for statistics

LastEventTime = 0 # time of last event processed
TotalTravel = 0


# Interval between arrivals averaging mean seconds (5)
#R.N.G. for providing vehicle arrivals based on exponential distrbution
def random_exp(mean):
    return random.expovariate(1/mean)
# Type of events: arrival, through, departure


arrivalCounts = {10:0, 11:0, 12:0, 13:0, 14:0}
crossCounts = {10:0, 11:0, 12:0, 13:0, 14:0}
depCounts = {10:0, 11:0, 12:0, 13:0, 14:0}

now = 0.0  #clock simulator

intersectionFree = True

def schedule(queue, time, event):
    heappush(queue, (time,event))



#Event Handlers:

def arrival(event, q): #to some intersection
    global now
    global LastEventTime
    global pre_X
    global ArrivalCount
    global intersectionFree

    if debug:
        print "Arrival Event: time = {0}".format(now)
        print "Vehicle ID: {0}".format(event.data['vehicle_id'])
    #if interesection is free, car will enter, else it will wait
    curr_vehicle = event.id
    curr_inter = event.to_cross
    og = event.start

    #if light at 10th street intersection is green, car will enter, else it will wait
    g,y,r = signal_time_NB[curr_inter] #signal times for 10th st light
    signal_cycle = g+y+r


    arrivalCounts[curr_inter] += 1

    wait =  0
    if ((now % signal_cycle) > (g+y)): #arrived when red light
        wait = r - ((now % signal_cycle) - (g+y) )
        waiting_counts[curr_inter] = waiting_counts[curr_inter] + 1



    if curr_inter == 10:
        ArrivalCount = ArrivalCount + 1
        if ArrivalCount < Cutoff:
            next_id = curr_vehicle + 1
            ts = now + random_exp(A)
            data = {
                "type" : "arrival",
                "vehicle_id" : next_id,
                "next": 10,
                "start": ts,
                "latest": ts
            }
            new_event = Event(ts, data)
            schedule(q, ts, new_event)



    add = 0
    if waiting_counts[curr_inter] > 1: #if more than one car
        add = intersection_x_times[curr_inter]/2 #wait till previous car is halfway through intersection
    next_ts = now + wait + add
    data = {
        "type" : "cross",
        "vehicle_id" : curr_vehicle,
        "next": curr_inter,
        "start": og,
        "latest": next_ts
    }
    #still need to cross the same intersection
    new_event = Event(next_ts, data)
    schedule(q, next_ts, new_event)




def cross(event, q):

    global LastEventTime
    global pre_X
    global now

    if debug:
        print "Crossing Event: time = {0}".format(now)
        print "Vehicle ID: {0}".format(event.data['vehicle_id'])

    curr_vehicle = event.id
    curr_inter = event.to_cross
    og = event.start
    crossCounts[curr_inter] += 1
    if waiting_counts[curr_inter] > 0:
        waiting_counts[curr_inter] = waiting_counts[curr_inter] - 1

    #Schedule departure event


    ts = now + intersection_x_times[curr_inter]
    data = {
        "type" : "departure",
        "vehicle_id" : curr_vehicle,
        "next": curr_inter,
        "start": og,
        "latest": ts
    }
    new_event = Event(ts, data)
    schedule(q, ts, new_event)





def departure(event,q):
    global LastEventTime
    global now
    global TotalTravel

    if debug:
        print "Departure Event: time = {0}".format(now)
        print "Vehicle ID: {0}".format(event.data['vehicle_id'])

    curr_vehicle = event.id
    curr_inter = event.to_cross
    og = event.start
    depCounts[curr_inter] += 1
    if curr_inter < 13: #schedule arrival to next intersection
        next_inter = curr_inter + 1
        if curr_inter == 12:
            next_inter = next_inter + 1
        next_ts = now + section_traverse_times[(curr_inter, next_inter)]
        data = {
                "type" : "arrival",
                "vehicle_id" : curr_vehicle,
                "next": next_inter,
                "start" : og,
                "latest": next_ts
            }
        new_event = Event(next_ts, data)
        schedule(q, next_ts, new_event)
    else: #end of all scheduling

        vehicle_travel = event.latest - event.start
        TotalTravel = TotalTravel + vehicle_travel
        with open(filename, 'a') as f:
            wr = csv.writer(f)
            wr.writerow([curr_vehicle,vehicle_travel])


def run_sim(q):
    print "running"
    while(q):
        curr = heappop(q)
        global now
        now = curr[0]
        curr_event = curr[1]
        if curr_event.type == "arrival":
            arrival(curr_event, q)
        elif curr_event.type == "cross":
            cross(curr_event, q)
        elif curr_event.type == "departure":
            departure(curr_event,q)

        #call event handler relative to curr_event


def main():
    global A
    global TotalTravel
    global ArrivalCount


    TotalTravel = 0
    waiting_counts = {10:0, 11:0, 12:0, 13:0, 14:0}
    waiting_time = {10:0, 11:0, 12:0, 13:0, 14:0}
    pq = [] #priority queue fo FEL
    ts = random_exp(A)
    data = {"vehicle_id": 0,  "type": "arrival", "next":10, "start":ts, "latest":ts} #Needs to have previous intersection
    new_event = Event(ts, data)
    schedule(pq, ts, new_event)
    start = time.time()
    run_sim(pq)
    end = time.time()
    print "==Statistics=="
    print A
    print "Total Travel Time = {0}".format(TotalTravel)
    print "Average Travel Time = {0}".format(TotalTravel/Cutoff)



main()
# print arrivalCounts
# print crossCounts
# print depCounts

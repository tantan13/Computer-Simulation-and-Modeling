from heapq import *
# from traffic import *
import random
import math
import time

debug = True #flag to debug
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
        self.type = data['type']
        self.to_cross = data['next'] #intersection that needs to be crossed next (starts of as 10th)
        self.data = data


#State variables  and other global information

# Simulation constants; all times in seconds
# A = mean interarrival time (in seconds, between cars)
# crosstime = time in interestion when crossing

A = 2.0


Cutoff = 10  #number of cars to simulate

#State Variables of Simulation
pre_X = 0	            # cars waiting to use intersection
cars_x = 0              # cars in intersection
intersectionFree = 1	#boolean: 1 if intersection is free, 0 otherwise
#Eventually, there will be a variable per lane per intersection
ArrivalCount=0	        #number of arrivals simulated; used for termination

# State variables used for statistics
TotalWaitingTime = 0 #total time waiting to use intersection
LastEventTime = 0 # time of last event processed

# Interval between arrivals averaging mean seconds (5)
def random_exp(mean):
    return random.expovariate(1/mean)

# Type of events: arrival, cross, departure




now = 0.0  #clock simulator

intersectionFree = True

def schedule(queue, time, event):
    heappush(queue, (time,event))




#Event Handlers:

def arrival(event, q): #to corridor- computation for crossing 10th streer intersection
    global now #global time
    global TotalWaitingTime
    global LastEventTime
    global pre_X
    global ArrivalCount
    global intersectionFree

    if debug:
        print "Arrival Event: time = {0}".format(now)
        print "Vehicle ID: {0}".format(event.data['vehicle_id'])
    curr_vehicle = event.data["vehicle_id"]
    curr_inter = event.to_cross



    #if light at 10th street intersection is green, car will enter, else it will wait
    g,y,r = signal_time_NB[curr_inter] #signal times for 10th st light
    signal_cycle = g+y+r

    wait_time = 0
    if ((now % signal_cycle) > (g+y)): #arrived when red light
        wait_time = r - ((now % signal_cycle) - (g+y) )

    #TODO: FIX this for global waiting time
    # #if first intersection is not free
    # if (pre_X > 1): # if there are waiting cars, update total waiting time
    #     TotalWaitingTime += ((pre_X-1) * (now - LastEventTime))


    #pre_X = pre_X + 1 #add one to the count of that intersection



    #Schedule(11th street intersection) after waiting for 10th signal, crossing 10th, and crossing section between 10th and 11th
    next_ts = now + wait_time + intersection_x_times[curr_inter] + section_traverse_times[(curr_inter, curr_inter+1)]
    data = {
            "type" : "cross",
            "vehicle_id" : curr_vehicle,
            "next": 11
        }
    new_event = Event(next_ts, data)
    schedule(q, next_ts, new_event)

    ArrivalCount = ArrivalCount + 1 #number of cars that arrived
    if ArrivalCount < Cutoff: #schedule a new arrival event
        next_id = curr_vehicle + 1
        data = {
            "type" : "arrival",
            "vehicle_id" : next_id,
            "next": 10
        }
        ts = now + random_exp(A)
        new_event = Event(ts, data)
        schedule(q, ts, new_event)
    #
    # if intersectionFree:
    #     #schedule crossing through intersection event
    #
    #     intersectionFree = False
    #     data = {
    #         "type" : "through",
    #         "vehicle_id" : curr_vehicle
    #     }
    #     ts = now + stop
    #     new_event = Event(ts, data)
    #     schedule(q, ts, new_event)
    LastEventTime = now


def cross(event, q): #cross a specific intersection: either 11th or 12th.
    global TotalWaitingTime
    global LastEventTime
    global pre_X
    global now

    if debug:
        print "Crossing Event: time = {0}".format(now)
        print "Vehicle ID: {0}".format(event.data['vehicle_id'])

    curr_vehicle = event.data["vehicle_id"]
    curr_inter = event.to_cross

    #if light at that street intersection is green, car will enter, else it will wait
    g,y,r = signal_time_NB[curr_inter] #signal times for that street light
    signal_cycle = g+y+r


    wait_time = 0
    if ((now % signal_cycle) > (g+y)): #arrived when red light
        wait_time = r - ((now % signal_cycle) - (g+y) )

    #TODO: FIX this for global waiting time
    # #if first intersection is not free
    # if (pre_X > 1): # if there are waiting cars, update total waiting time
    #     TotalWaitingTime += ((pre_X-1) * (now - LastEventTime))

    # pre_X = pre_X - 1


    if curr_inter == 11: #11th schedules 12th
        #Schedule(12th street intersection) after waiting for 11th signal, crossing 11th, and crossing section between 11th and 12th
        next_inter = curr_inter + 1
        next_ts = now + wait_time + intersection_x_times[curr_inter] + section_traverse_times[(curr_inter, next_inter)]
        data = {
                "type" : "cross",
                "vehicle_id" : curr_vehicle,
                "next": next_inter
            }
        new_event = Event(next_ts, data)
        schedule(q, next_ts, new_event)

    else:   #12th schedules depart
        #Schedule(14th street intersection) after waiting for
        #12h signal, crossing 12th, and crossing section between 12th and 14th
        next_inter = curr_inter + 2
        next_ts = now + wait_time + intersection_x_times[curr_inter] + section_traverse_times[(curr_inter, next_inter)]
        data = {
                "type" : "depart",
                "vehicle_id" : curr_vehicle,
                "next": next_inter
            }
        new_event = Event(next_ts, data)
        schedule(q, next_ts, new_event)


    #
    #
    # if pre_X > 0: #schedule crossing event for next car
    #     next_id = curr_vehicle + 1
    #     data = {
    #         "type" : "through",
    #         "vehicle_id" : next_id
    #     }
    #     ts = now + stop  + crosstime/2#next car can start going when current car is halfway through the intersection
    #     new_event = Event(ts, data)
    #     schedule(q, ts, new_event)
    # else:
    #     intersectionFree = True
    LastEventTime = now



def departure(event): #cross 14th street
    global TotalWaitingTime
    global LastEventTime
    global now

    #waiting time update based on 14th street intersection
    # intersection signal time: ist = red_time + green_time_yellow_time
    # if global_time % (ist) < (green_time_yellow_time):
        #travel time = time to cross intersection
    #else:

    if debug:
        print "Departure Event: time = {0}".format(now)
        print "Vehicle ID: {0}".format(event.data['vehicle_id'])

    curr_vehicle = event.data["vehicle_id"]
    curr_inter = event.to_cross

    #if light at that street intersection is green, car will enter, else it will wait
    g,y,r = signal_time_NB[curr_inter] #signal times for that street light
    signal_cycle = g+y+r


    wait_time = 0
    if ((now % signal_cycle) > (g+y)): #arrived when red light
        wait_time = r - ((now % signal_cycle) - (g+y) )



    # if pre_X > 1: #waiting cars
    #     TotalWaitingTime += ((pre_X-1)* (now - LastEventTime))
    LastEventTime = now




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


def main():

    pq = []
    data = {"vehicle_id": 0,  "type": "arrival", "next":10} #Needs to have previous intersection
    ts = random_exp(A)
    new_event = Event(ts, data)
    schedule(pq, ts, new_event)
    #prev_intersection = 0, new event

    start = time.time()
    run_sim(pq)
    end = time.time()

    print "Total Waiting Time = {0}".format(TotalWaitingTime)
    print "Average Waiting Time = {0}".format(TotalWaitingTime/Cutoff)

main()

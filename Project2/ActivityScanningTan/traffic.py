#Event hanlders: arrival, enter, depature, side_enter
import random
from engine import *
# Type of events: arrival, through, departure


#State variables  and other global information

# Simulation constants; all times in seconds
# A = mean interarrival time (in seconds, between cars)
# crosstime = time in interestion when crossing

A = 2.0
crosstime = 20 #time to cross the intersection

#stop wait time at stop sign, per car, in seconds
stop = 2

Cutoff = 10  #number of cars to simulate
#State Variables of Simulation
pre_X = 0	            # cars waiting to use intersection
cars_x = 0              # cars in intersection
intersectionFree = 1	#boolean: 1 if intersection is free, 0 otherwise
ArrivalCount=0	        #number of arrivals simulated; used for termination

# State variables used for statistics
TotalWaitingTime = 0 #total time waiting to use intersection
LastEventTime = 0 # time of last event processed


now = 0.0  #clock simulator

intersectionFree = True
#Event Handlers
def arrival(event, q):
    global now
    global TotalWaitingTime
    global LastEventTime
    global pre_X
    global ArrivalCount
    global intersectionFree

    if debug:
        print "Arrival Event: time = {}".format(now)
        print "Vehicle ID: {}".format(event.data['vehicle_id'])
    #if interesection is free, car will enter, else it will wait



    if (pre_X > 1): # if there are waiting cars, update total waiting time
        TotalWaitingTime += ((pre_X-1) * (now - LastEventTime))


    pre_X = pre_X + 1
    curr_vehicle = event.data["vehicle_id"]


    ArrivalCount = ArrivalCount + 1
    if ArrivalCount < Cutoff:
        next_id = curr_vehicle + 1
        data = {
            "type" : "arrival",
            "vehicle_id" : next_id
        }
        ts = now + random_exp(A)
        new_event = Event(ts, data)
        schedule(q, ts, new_event)
        new_event_c = Event(ts,data)
        new_event_c.scheduler(self, self.timestamp, "redLight", self.data) # put car event into queue 

    if intersectionFree:
        #schedule crossing through intersection event

        intersectionFree = False
        data = {
            "type" : "through",
            "vehicle_id" : curr_vehicle
        }
        ts = now + stop
        new_event = Event(ts, data)
        schedule(q, ts, new_event)
        new_event_c = Event(ts,data)
        new_event_c.scheduler(self, self.timestamp, "greenLight", self.data) # put car event into queue 
        LastEventTime = now

def cross(event, q):
    global TotalWaitingTime
    global LastEventTime
    global pre_X
    global now

    if debug:
        print "Crossing Event: time = {}".format(now)
        print "Vehicle ID: {}".format(event.data['vehicle_id'])


    if (pre_X > 1): # if there are waiting cars, update total waiting time
        TotalWaitingTime += ((pre_X-1) * (now - LastEventTime))

    pre_X = pre_X - 1
    #Schedule departure event
    curr_vehicle = event.data["vehicle_id"]
    data = {
        "type" : "departure",
        "vehicle_id" : curr_vehicle
    }
    ts = now + crosstime
    new_event = Event(ts, data)
    schedule(q, ts, new_event)

    if pre_X > 0: #schedule crossing event for next car
        next_id = curr_vehicle + 1
        data = {
            "type" : "through",
            "vehicle_id" : next_id
        }
        ts = now + stop  + crosstime/2#next car can start going when current car is halfway through the intersection
        new_event = Event(ts, data)
        schedule(q, ts, new_event)
    else:
        intersectionFree = True
    LastEventTime = now



def departure(event):
    global TotalWaitingTime
    global LastEventTime
    global now

    if debug:
        print "Departure Event: time = {}".format(now)
        print "Vehicle ID: {}".format(event.data['vehicle_id'])


    if pre_X > 1: #waiting cars
        TotalWaitingTime += ((pre_X-1)* (now - LastEventTime))
    LastEventTime = now

def main():

    pq = []
    data = {"vehicle_id": 0,  "type": "arrival"} #Needs to have previous intersection
    ts = random_exp(A)
    new_event = Event(ts, data)
    schedule(pq, ts, new_event)
    #prev_intersection = 0, new event

    start = time.time()
    run_sim(pq)
    run()
    end = time.time()

    print "Total Waiting Time = {}".format(TotalWaitingTime)
    print "Average Waiting Time = {}".format(TotalWaitingTime/Cutoff)

main()

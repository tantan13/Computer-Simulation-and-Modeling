import random
from random import expovariate as epv
#import csv
#import matplotlib.pyplot as plt
#import matplotlib as mpl

#average interarrival time for cars, in half-seconds
trafficInputTime = 6
maxSpeed = 14
count = 1
time = 0
class Car:
    count = 1

    def __init__(self, length, lane, x, speed, maxspeed, counter=count, newC = False):
        global time
        time += 1
        if newC:
            global count
            count += 1
            self.count = count
        else:
            self.count = counter
        self.length = length
        self.lane = lane
        self.x = x
        self.speed = speed
        self.maxspeed = maxspeed
        self.entryTime = time
        time -= 1
        
    def __eq__(self, other): 
        if not isinstance(other, Car):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.lane == other.lane
    
    def dist(self, other):
        return self.x - other.x
    
    def collide(self, other, speed):
        return (other.x - other.length >= self.x) and (other.lane == self.lane) and ((other.x - other.length - self.x) <= dist)

def checkRange(low, high, cars, carID):
    ret = True
    for car in cars:
        if (car.x > high and car.x - car.length < high) or (car.x > low and car.x - car.length < low):
            if (car.count != carID):
                ret = False
    return ret

global cars
#List of lights with [color(1=red,0=green), location, time left until changing color, street name,green cycle time, red cycle time]
lights = [[0,0,70, "10th", 70,98],[1,441,110, "11th",84,110],[0,983,122, "12th",122,72],[1,1819,92, "14th",70,92]]
newCarChance = 0.5


#used to find distribution of interarrival times for cars travelling all the way through
#commented out to remove any dependency on 'csv'

#def getCars():
#    lowest = 9999999999
#    carsEnter = []
#    carsExit = []
#    with open('../NGSIM-Data/entrance_data.csv', newline='') as csvfile:
#        carreader = csv.DictReader(csvfile)
#        cars = []
#        for row in carreader:
#            newCar = {}
#            newCar['Vehicle_ID'] = int(row['Vehicle_ID'])
#            newCar['Epoch_ms'] = int(row['Epoch_ms'])
#            newCar['Veh_len'] = float(row['Veh_Len'])
#            newCar['Veh_velocity'] = float(row['Veh_Velocity'])
#            newCar['Lane_id'] = int(row['Lane_ID'])
#            if int(row['Epoch_ms']) < lowest:
#                lowest = int(row['Epoch_ms'])
#            cars.append(newCar)
#        
#        for row in cars:
#            row['Epoch_ms'] = row['Epoch_ms'] - lowest
#        carsEnter = cars
#            
#    with open('../NGSIM-Data/exit_data.csv', newline='') as csvfile:
#        carreader = csv.DictReader(csvfile)
#        cars = []
#        for row in carreader:
#            newCar = {}
#            newCar['Vehicle_ID'] = int(row['Vehicle_ID'])
#            newCar['Epoch_ms'] = int(row['Epoch_ms'])
#            newCar['Veh_len'] = float(row['Veh_Len'])
#            newCar['Veh_velocity'] = float(row['Veh_Velocity'])
#            newCar['Lane_id'] = int(row['Lane_ID'])
#            cars.append(newCar)
#        
#        for row in cars:
#            row['Epoch_ms'] = row['Epoch_ms'] - lowest
#            
#        carsExit = cars
#        
#    for enter in carsEnter:
#        enter['Travel_Time'] = 0
#        for cExit in carsExit:
#            if enter['Vehicle_ID'] == cExit['Vehicle_ID']:
#                enter['Travel_Time'] = cExit['Epoch_ms'] - enter['Epoch_ms']
#        if enter['Travel_Time'] == 0:
#            carsEnter.remove(enter)
#    return carsEnter

#def tester():
#    with open('averages.csv', 'w') as csvfile:
#        average _writer = csv.writer(csvfile)
#        for i in range(20):
#            

def main():
    addCar = 0
    global time
    cars = [Car(15, random.randint(0,1), 15, 5, maxSpeed)]
    exited = []
    while len(exited) < 1000:
        #print(addCar)
        time += 1
        #for car in cars:
        #    print("car" + str(car.count) + " at " + str(car.x) )
        if addCar <= 0:
            cars = newCar(cars)
            addCar = epv(1.0/float(trafficInputTime))
        else:
            addCar -= 1
        updateLights()
        cars, exited = step(cars, exited)
        
    totTravel = 0
    for car in exited:
        totTravel += car[2]
    print("Average travel time is " + str(totTravel / 1000))
#    with open('high_traffic.csv', 'w', newline='') as csvfile:
#        traffic_writer = csv.writer(csvfile)
#        for row in exited:
#            traffic_writer.writerow(row)
    return totTravel/len(exited)

def step(cars, exited):
    #sideways()
    cars, exited = updatePos(cars, exited)

    
    choice = random.random()
    global lights
    if choice < newCarChance and lights[0][0] == 0:
        cars = newCar(cars)
    return cars, exited

def sideways():
    for car in cars:
        randomChange = random.random() < 0.1
        if randomChange and not collision(car,0):
            car.lane = (car.lane + 1) % 2

def updatePos(cars, exited):
    global time
    time += 1
    newCars = []
    for car in cars:
        newCar = Car(car.length, car.lane, car.x, car.speed, car.maxspeed, car.count)
        newCar.entryTime = car.entryTime
        if car.speed != car.maxspeed:
            newCar.speed += 1
        
        dist = collision(newCar, cars)
        if dist < newCar.speed:
            newCar.speed = max(0, dist - 5)

        #if newCar.speed > 0 and random.random() < 0.2:
        #    newCar.speed -= 1
        #print(str(newCar.x) + str(newCar.speed))

        #check if car is going through an intersetion, and if so, is it green
        newCar.speed = intersection(newCar)
        newCar.x = newCar.x + newCar.speed
        #print(str(newCar.x))
        if newCar.x > 1819:
            exitTime = (time - 1 - car.entryTime) / 2
            #print("Car " + str(car.count) + " in lane " + str(car.lane) + " exited with speed " + str(car.speed))
            exited.append([car.count, time, exitTime])
        else:
            #print("HERE" + str(newCar.x))
            newCars.append(newCar)
    #print(newCars)
    time -= 1
    #print(str(time) + ' ' + str(newCars))
    return newCars, exited

def newCar(cars):
    newCar = Car(15, random.randint(0,1), 15, 5, maxSpeed, newC=True)
    if (checkRange(0, 15, cars, newCar.count)):
        cars.append(newCar)
    else:
        newCar.lane = (newCar.lane + 1) % 2
        if (checkRange(0, 15, cars, newCar.count)):
            cars.append(newCar)
    return cars

def collision(car, cars):
    dist = car.speed
    for other in cars:
        if not car == other:
            if (other.x - other.length >= car.x) and (other.lane == car.lane) and ((other.x - other.length - car.x) <= dist):
                dist == other.x - other.length - car.x
    return dist

def intersection(car):
    global lights
    for light in lights:
        #if the car is crossing the intersection
        if car.x <= light[1] and car.x + car.speed >= light[1]:
            #if the light is red
            if light[0] == 1:
                #print("Stuck at light")
                return 0 #light[1] - car.x

    return car.speed

def updateLights():
    global lights
    for light in lights:
        if light[2] == 0:
            light[0] = (light[0] + 1) % 2
            light[2] = light[light[0] + 4]
            #print ("Light at " + light[3] + " is now " + str(light[0]))
        else:
            light[2] -= 1

main()

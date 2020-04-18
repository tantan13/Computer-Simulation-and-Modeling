#This takes in all of the cars from the entrance and exit data files in the NGSIM_Data folder and converts the csv to dictionaries.
#The end result is every car that enters at 10th and exits at 14th, including the travel time for that car
import csv

lowest = 9999999999
carsEnter = []
carsExit = []
with open('../NGSIM-Data/entrance_data.csv', newline='') as csvfile:
    carreader = csv.DictReader(csvfile)
    cars = []
    for row in carreader:
        newCar = {}
        newCar['Vehicle_ID'] = int(row['Vehicle_ID'])
        newCar['Epoch_ms'] = int(row['Epoch_ms'])
        newCar['Veh_len'] = float(row['Veh_Len'])
        newCar['Veh_velocity'] = float(row['Veh_Velocity'])
        newCar['Lane_id'] = int(row['Lane_ID'])
        if int(row['Epoch_ms']) < lowest:
            lowest = int(row['Epoch_ms'])
        cars.append(newCar)
    
    for row in cars:
        row['Epoch_ms'] = row['Epoch_ms'] - lowest
    carsEnter = cars
        
with open('../NGSIM-Data/exit_data.csv', newline='') as csvfile:
    carreader = csv.DictReader(csvfile)
    cars = []
    for row in carreader:
        newCar = {}
        newCar['Vehicle_ID'] = int(row['Vehicle_ID'])
        newCar['Epoch_ms'] = int(row['Epoch_ms'])
        newCar['Veh_len'] = float(row['Veh_Len'])
        newCar['Veh_velocity'] = float(row['Veh_Velocity'])
        newCar['Lane_id'] = int(row['Lane_ID'])
        cars.append(newCar)
    
    for row in cars:
        row['Epoch_ms'] = row['Epoch_ms'] - lowest
        
    carsExit = cars
        
for enter in carsEnter:
    enter['Travel_Time'] = 0
    for cExit in carsExit:
        if enter['Vehicle_ID'] == cExit['Vehicle_ID']:
            enter['Travel_Time'] = cExit['Epoch_ms'] - enter['Epoch_ms']
    if enter['Travel_Time'] == 0:
        carsEnter.remove(enter)
laneCt = [0,0,0,0]
    
for car in carsEnter:
    print(car['Travel_Time'])
    laneCt[car['Lane_id']] += 1


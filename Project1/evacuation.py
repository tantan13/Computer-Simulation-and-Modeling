import matplotlib
matplotlib.use("qt4agg")
import pylab as PL
import random as RD
import numpy as NP
from numpy import linalg as LA
from scipy.spatial import distance as dist
from Agent import Agent
from math import sqrt

RD.seed()

populationSize = 64
noiseLevel = 5
avoidanceRadius = 50
flockRadius = 100
boardDimension = 1000

#strengths are proportion of new weight vs proportion of old weight (0-1)
avoidanceStrength = 0.8
approachStrength = 0.5
alignStrength = 0.3
obstacleStrength = 1
goalStrength = 1
totalStrength = 0.1

flag = [False]

def populationSizeF (val=populationSize):
    """Population size.
    The parameter change is effective only when model is reset.
    """
    global populationSize
    populationSize = int(val)
    return val

def noiseLevelF (val=noiseLevel):
    """Random walk noise level.
    
    The parameter can be changed in a running model.
    """
    global noiseLevel
    noiseLevel = val
    return val

def init():
    global time, agents, walls, goalPos

    time = 0

    scenario1()

def scenario1():
    global agents, walls, goalPos, goals
    agents = []
    for i in range(populationSize):
        row = i % 8
        col = i / 8
        newAgent = Agent(row*50+300, col*50+300, RD.gauss(0, noiseLevel), RD.gauss(0, noiseLevel), 0, 0)
        agents.append(newAgent)
        
    walls = []
    for i in range(60):
        newWall = [i*5+100, 100]
        walls.append(newWall)
    for i in range(61):
        newWall = [i*5+600, 100]
        walls.append(newWall)
    for i in range(160):
        newWall = [i*5+100, 900]
        walls.append(newWall)
    for i in range(160):
        newWall = [100, i*5+100]
        walls.append(newWall)
    for i in range(160):
        newWall = [900, i*5+100]
        walls.append(newWall)
        
    goals = 1
    goalPos = [500,100]
    
def scenario2():
    global agents, walls, goalPos, goalPos2, goals
    agents = []
    for i in range(populationSize):
        row = i % 8.0
        col = i / 8.0
        newAgent = Agent(row*50+300, col*50+300, RD.gauss(0, noiseLevel), RD.gauss(0, noiseLevel), 0, 0)
        agents.append(newAgent)
        
    walls = []
    for i in range(60):
        newWall = [i*5+100, 100]
        walls.append(newWall)
    for i in range(61):
        newWall = [i*5+600, 100]
        walls.append(newWall)
    for i in range(60):
        newWall = [i*5+100, 900]
        walls.append(newWall)
    for i in range(61):
        newWall = [i*5+600, 900]
        walls.append(newWall)
    for i in range(160):
        newWall = [100, i*5+100]
        walls.append(newWall)
    for i in range(160):
        newWall = [900, i*5+100]
        walls.append(newWall)
        
    goals = 2
    goalPos = [500, 100]
    goalPos2 = [500, 900]

def draw():
    PL.cla()
    PL.plot([wall[0] for wall in walls], [wall[1] for wall in walls], 'ro')
    x = [ag.posX for ag in agents]
    y = [ag.posY for ag in agents]
    PL.plot(x, y, 'bo')
    
    PL.axis('scaled')
    PL.axis([0, boardDimension, 0, boardDimension])
    PL.title('t = ' + str(time))
    PL.pause(0.01)
    
def step():
    """Update positions of each agent each time step"""
    global time, agents, walls, goalPos, flag

    time += 1
    
    for ag in agents:
#        print(ag.oldVelX, ag.oldVelY)
        colVect = ag.collisions(ag, avoidanceRadius, agents)
        avgLoc, avgVel = ag.getFlock(agents, flockRadius)
        alignVect = ag.align(avgVel, populationSize)
        apprVect = ag.approach(avgLoc)
        avoidVect = ag.avoidObstacles(walls, avoidanceRadius, flag)
        goalVect = ag.goal(goalPos)
#        avoidVect = ag.collisions(ag, avoidanceRadius, walls)
        
        # Works perfectly without these two vectors...but wouldn't that practically eliminate the boids incorporation?
        #apprVect = [0,0]
        #alignVect = [0,0]
        
        # Put a max limit on the velocity?
        limit = 50
        if ag.oldVelX > limit:
            ag.oldVelX = sqrt(ag.oldVelX - limit) + 0.8 * limit
        if ag.oldVelY > limit:
            ag.oldVelY = sqrt(ag.oldVelY - limit) + 0.8 * limit
        
        # If there are multiple exits, agents should move to the closest one
        if goals == 2:
            d1 = dist.euclidean([ag.posX, ag.posY], goalPos)
            d2 = dist.euclidean([ag.posX, ag.posY], goalPos2)
            if d1 < d2:
                goalVect = ag.goal(goalPos)
            else:
                goalVect = ag.goal(goalPos2)
            
            escape(goalPos2)
        escape(goalPos)
        
        # If there is a collision, completely ignore other vectors? Only focus on collision? (don't think this is necessary)
        if False:
#        if flag[0] == True:
            print(flag[0])
            weightTot = obstacleStrength
            weights = [1]
            ag.newVelX = (1 - totalStrength) * ag.oldVelX + totalStrength * (avoidVect[0])
            ag.newVelY = (1 - totalStrength) * ag.oldVelY + totalStrength * (avoidVect[1])
        else:
            weightTot = avoidanceStrength + alignStrength + approachStrength + obstacleStrength + goalStrength
            weights = [avoidanceStrength / weightTot, alignStrength / weightTot, approachStrength / weightTot, obstacleStrength / weightTot, goalStrength / weightTot]
            
            ag.newVelX = (1 - totalStrength) * ag.oldVelX + totalStrength * (colVect[0] * weights[0] + alignVect[0] * weights[1] + apprVect[0] * weights[2] + avoidVect[0] * weights[3] + goalVect[0] * weights[4])       
            ag.newVelY = (1 - totalStrength) * ag.oldVelY + totalStrength * (colVect[1] * weights[0] + alignVect[1] * weights[1] + apprVect[1] * weights[2] + avoidVect[1] * weights[3] + goalVect[1] * weights[4])
        
        # Update positions using new velocities
        # Last number changes speed on screen
        ag.posX += ag.newVelX * 0.1
        ag.posY += ag.newVelY * 0.1
        
        # Wraps agents around when they leave the screen
        # And shifts new weights to old weight position
        for ag in agents:
            ag.posX = ag.posX % boardDimension
            ag.posY = ag.posY % boardDimension
            ag.oldVelX = ag.newVelX
            ag.oldVelY = ag.newVelY

#    for ag in agents:
#        colVect = ag.collisions(ag, avoidanceRadius, agents)
#        avgLoc, avgVel = ag.getFlock(agents, flockRadius)
#        alignVect = ag.align(avgVel, populationSize)
#        apprVect = ag.approach(avgLoc)
#        avoidVect = ag.avoidObstacles(walls, avoidanceRadius)

#        colVect = normalize(colVect[0], colVect[1])
#        alignVect = normalize(alignVect[0], alignVect[1])
#        apprVect = normalize(apprVect[0], apprVect[1])
        
#        ag.newVelX = ag.oldVelX + colVect[0] + alignVect[0] + apprVect[0] + avoidVect[0]
#        ag.newVelY = ag.oldVelY + colVect[1] + alignVect[1] + apprVect[1] + avoidVect[1]

# Agents should disappear after reaching target position
def escape(goalPos):
    global agents
    for ag in agents:
        #if dist.euclidean([ag.posX, ag.posY], goalPos) < 10:
        #    agents.remove(ag)
        
        #Removes agents when they leave
        if ag.posX < 100 or ag.posX > 900 or ag.posY < 100 or ag.posY > 900:
            agents.remove(ag)
    

def normalize(x, y):
    mag = float(NP.sqrt(x*x + y*y))
    newX = x/mag
    newY = y/mag
    return [newX, newY]

import pycxsimulator
pSetters = [populationSizeF, noiseLevelF]
pycxsimulator.GUI(parameterSetters=pSetters).start(func=[init,draw,step])
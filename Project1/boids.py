import matplotlib
matplotlib.use("qt4agg")
import pylab as PL
import random as RD
import numpy as NP
from scipy.spatial import distance as dist
from Agent import Agent

RD.seed()

populationSize = 64
noiseLevel = 1
avoidanceRadius = 30
flockRadius = 100
boardDimension = 1000

#strengths are proportion of new weight vs proportion of old weight (0-1)
avoidanceStrength = 0.2
approachStrength = 0.6
alignStrength = 0.8
totalStrength = 0.2

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
    global time, agents

    time = 0
        
    agents = []
    for i in range(populationSize):
        row = i % 8.0
        col = i / 8.0
        newAgent = Agent(row*50.0+50.0, col*50.0+50.0, RD.gauss(0, noiseLevel), RD.gauss(0, noiseLevel), 0, 0)
        agents.append(newAgent)

def draw():
    PL.cla()
    x = [ag.posX for ag in agents]
    y = [ag.posY for ag in agents]
    PL.plot(x, y, 'bo')
    PL.axis('scaled')
    PL.axis([0, boardDimension, 0, boardDimension])
    PL.title('t = ' + str(time))
    PL.pause(0.03)

def step():
    """Update positions of each agent each time step"""
    global time, agents

    time += 1

#    d = dist.euclidean([agents[0].posX, agents[0].posY], [agents[1].posX, agents[1].posY])
#    print(d)

    for ag in agents:
        colVect = ag.collisions(ag, avoidanceRadius, agents)
        avgLoc, avgVel = ag.getFlock(agents, flockRadius)
        alignVect = ag.align(avgVel, populationSize)
        apprVect = ag.approach(avgLoc)
        
        weightTot = avoidanceStrength + alignStrength + approachStrength
        weights = [avoidanceStrength / weightTot, alignStrength / weightTot, approachStrength / weightTot]
        ag.newVelX = (1 - totalStrength) * ag.oldVelX + totalStrength * (colVect[0] * weights[0] + alignVect[0] * weights[1] + apprVect[0] * weights[2])       
        ag.newVelY = (1 - totalStrength) * ag.oldVelY + totalStrength * (colVect[1] * weights[0] + alignVect[1] * weights[1] + apprVect[1] * weights[2])
        
        # Update positions using new velocities
        # Last number changes speed on screen
        ag.posX += ag.newVelX * 0.2
        ag.posY += ag.newVelY * 0.2
        
        # Wraps agents around when they leave the screen
        # And shifts new weights to old weight position
        for ag in agents:
            ag.posX = ag.posX % boardDimension
            ag.posY = ag.posY % boardDimension
            ag.oldVelX = ag.newVelX
            ag.oldVelY = ag.newVelY

import pycxsimulator
pSetters = [populationSizeF, noiseLevelF]
pycxsimulator.GUI(parameterSetters=pSetters).start(func=[init,draw,step])
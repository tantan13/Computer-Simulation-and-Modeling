import matplotlib
matplotlib.use("qt4agg")
import pylab as PL
import random as RD
import numpy as NP
from scipy.spatial import distance as dist
from sklearn import preprocessing
#import evacuation

class Agent:
    
    posX = 0.0
    poxY = 0.0
    oldVelX = 0.0
    oldVelY = 0.0
    newVelX = 0.0
    newVelY = 0.0
    flock = []
    
    def __init__(self, posx, posy, oldvelx, oldvely, newvelx, newvely):
        self.posX = posx
        self.posY = posy
        self.oldVelX = oldvelx
        self.oldVelY = oldvely
        self.newVelX = newvelx
        self.newVelY = newvely
    
    def approach(self, flock):
        """Get average position of the flock"""
        distX = flock[0] / len(flock) - self.posX
        distY = flock[1] / len(flock) - self.posY    
        return [distX * 0.1, distY * 0.1]
#        avgPos = [self.posX, self.posY]
#        for other in flock:
#            d = dist.euclidean([self.posX, self.posY], [other.posX, other.posY])
#            if d > 0:
#                avgPos[0] += other.posX
#                avgPos[1] += other.posY
#        avgPos[0] /= len(flock)
#        avgPos[1] /= len(flock)
##        avgPos = self.normalize(avgPos[0], avgPos[1])
#        vect = [avgPos[0] - self.posX, avgPos[1] - self.posY]
##        if vect[0] != 0 and vect[1] != 0:
##            vect = self.normalize(vect[0], vect[1])
#        factor = 0.5
#        vect = [vect[0]*factor, vect[1]*factor]
#        return vect
        
    def align(self, avgVel, populationSize):
        """Get average direction of flock"""
        alignX = avgVel[0] / populationSize
        alignY = avgVel[1] / populationSize
        #alignX = 1 / populationSize * ag[2] + (1 - (1/populationSize)) * flock[0]
        #alignY = 1 / populationSize * ag[3] + (1 - (1/populationSize)) * flock[1]
        return [alignX, alignY]
#        avgDir = [self.velX, self.velY]
#        for other in flock:
#            d = dist.euclidean([self.posX, self.posY], [other.posX, other.posY])
#            if d > 0:
##                temp = self.normalize(other.oldVelX, other.oldVelY)
##                avgDir[0] += temp[0]/d
##                avgDir[1] += temp[1]/d
#                avgDir[0] += other.velX
#                avgDir[1] += other.velY
#        avgDir[0] /= len(flock)
#        avgDir[1] /= len(flock)
##        if avgDir[0] != 0 and avgDir[1] != 0:
##            avgDir = self.normalize(avgDir[0], avgDir[1])
#        return avgDir
    
    #returns the proxVect of the closest other agent if one is within the avoidance radius     
    def collisions(self, ag, avoidanceRadius, agents):
        closestRad = avoidanceRadius
        proxVect = [self.oldVelX, self.oldVelY]
        for other in agents:
            if other.posX != self.posX and other.posY != self.posY:
                distBtw = dist.euclidean([self.posX, self.posY], [other.posX, other.posY])
                if distBtw < closestRad:
                    #avoid that one
                    closestRad = distBtw
                    proxVect = [(self.posX - other.posX) * (avoidanceRadius - distBtw),
                                (self.posY - other.posY)  * (avoidanceRadius - distBtw)]
        return proxVect
#        avoidOb = [0,0]
#        for other in flock:
#            d = dist.euclidean([self.posX, self.posY], [other.posX, other.posY])
#            if d < avoidanceRadius and d > 0:
#                avoidVect = [self.posX-other.posX, self.posY-other.posY]
##                avoidVect = self.normalize(avoidVect[0], avoidVect[1])
##                print(avoidVect)
##                avoidVect[0] /= d
##                avoidVect[1] /= d
#                avoidOb[0] += avoidVect[0]
#                avoidOb[1] += avoidVect[1]
##                print(d)
##        print(avoidOb)
#        return avoidOb
    
    def getFlock(self, agents, flockRadius):
        """Get average location and velocity of nearby agents"""
        """Get agents nearby current agent - we only care about these ones"""
        avgLoc = [0,0]
        avgVel = [0,0]
        for other in agents:
            if dist.euclidean([self.posX, self.posY], [other.posX, other.posY]) < flockRadius:
                avgLoc[0] += other.posX
                avgLoc[1] += other.posY
                avgVel[0] += other.oldVelX
                avgVel[1] += other.oldVelY
                
        return [avgLoc, avgVel]
#        flock = []
#        for other in agents:
#            if dist.euclidean([self.posX, self.posY], [other.posX, other.posY]) < flockRadius:
##                avgLoc[0] += other.posX
##                avgLoc[1] += other.posY
##                avgVel[0] += other.oldVelX
##                avgVel[1] += other.oldVelY
#                flock.append(other)     # this other agent is one that we care about
##        return [avgLoc, avgVel]
#        return flock
    
    def avoidObstacles(self, obstacles, avoidanceRadius, flag):
#        avoidObstacle = [0,0]
#        for obstacle in obstacles:
#            d = dist.euclidean([self.posX, self.posY], [obstacle[0], obstacle[1]])
#            if d < avoidanceRadius and d > 0:
#                avoidVect = [self.posX-obstacle[0], self.posY-obstacle[1]]
#                avoidVect[0] /= d
#                avoidVect[1] /= d
#                avoidObstacle += avoidVect
#        return avoidObstacle
#        flag[0] = True
        closestRad = avoidanceRadius
        proxVect = [self.oldVelX, self.oldVelY]
        for other in obstacles:
            if other[0] != self.posX and other[1] != self.posY:
                distBtw = dist.euclidean([self.posX, self.posY], [other[0], other[1]])
#                distBtw = NP.sqrt((self.posX-other[0])**2 + (self.posY-other[1])**2)
#                print(self.posX, self.posY)
                # BUG: below isn't getting triggered b/c distbtw is always too large for some reason
                if distBtw < closestRad:
                    #avoid that one
                    closestRad = distBtw
#                    proxVect = [(other[0] - self.posX) * (avoidanceRadius - distBtw),
#                                (other[1] - self.posY)  * (avoidanceRadius - distBtw)]
                    proxVect = [(self.posX - other[0]) * (avoidanceRadius - distBtw),
                                (self.posY - other[1])  * (avoidanceRadius - distBtw)]
#                    proxVect = [self.posX-other[0], self.posY-other[1]]
                    # set flag to indicate that collision is occurring
                    flag[0] = True
#                    print("hellooooo")
        return proxVect
    
    def goal(self, goalPos):
        #print(goalPos)
        goalVect = [0,0]
        goalVect = self.normalize(goalPos[0]-self.posX, goalPos[1]-self.posY)
        #print(goalVect)

        strength = 50000/dist.euclidean([self.posX, self.posY], [goalPos[0], goalPos[1]])
        goalVect = [strength * goalVect[0], strength * goalVect[1]]
        return goalVect
    
    def normalize(self, x, y):
        mag = float(NP.sqrt(x*x + y*y))
        newX = x/mag
        newY = y/mag
        return [newX, newY]
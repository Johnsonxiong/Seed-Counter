from random import randint
import time

#class MySeed:
class MySeed:
    tracks = []
    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None
    def getRGB(self):
        return (self.R,self.G,self.B)
        #return (0,255,0) #use green to show the notation of the seeds
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.i
    def getState(self):
        return self.state
    def getDir(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
 #       print("The coords of the seeds is xn:",xn," yn：",yn)
 #       print("The coords of the seeds is self.x:",self.x," self.y：",self.y)
        self.x = xn
        self.y = yn
    def setDone(self):
        self.done = True
    def timeOut(self):
        return self.done
    def going_UP(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end: #pass by the line
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False
    def going_DOWN(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
           # print("The length of self.tracks is ",len(self.tracks))
            if self.state == '0':
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start: #pass by the line
 #                   print("The self.tracks[-1][1] is ",self.tracks[-1][1])
 #                   print("The self.tracks[-2][1] is ",self.tracks[-2][1])
 #                   print("The self.tracks is ",self.tracks)
 #                   print("The mid_start is ",mid_start)
                    state = '1'
                    self.dir = 'down'
 #                   self.done = True
                    return True
            else:
                return False
        else:
            return False
    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
#class MultiPerson:
class MultiSeed:
#    def __init__(self, persons, xi, yi):
    def __init__(self, seeds, xi, yi):
        self.persons = persons
        self.seeds = seeds
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        

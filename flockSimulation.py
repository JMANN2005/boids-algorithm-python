import pygame
import math
import random

black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)

pygame.init()
win = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("flocking simulation")


##settings
flockSize = 30
##multiplyers
coodination = 0.03
grouping = 0.05
separation = 0.00005
selfVision = 300
centerOfScreen = 0.05
speed = 0.5
speedTowardsAverage = 0.2
preditorEnabled = True
preditorVision = 300
fear = 0.001
preditorSpeed = 2
preditorTurning = 0.05


class Bird:
    def __init__(self,num):
        self.num = num
        self.x = random.randint(200,1000)
        self.y = random.randint(100,500)
        self.w = 20
        self.h = 20
        self.angle = random.randint(0,360)
        self.bird = pygame.Rect(self.x,self.y,self.w,self.h)
        self.speed = 1
        self.color = green

    def draw(self):
        self.bird = pygame.Rect(self.x,self.y,self.w,self.h)
        pygame.draw.rect(win,self.color,self.bird)
    def update(self):
        
        ##angle align
        angleDiff = (averageAngle - self.angle) % 360
        if angleDiff > 180:
            angleDiff -= 360
        self.angle += angleDiff * coodination
        
        #towards centre of group
        xdiff = self.x - averageX
        ydiff = self.y - averageY
        midAngle = (math.atan2(ydiff,xdiff) * 180/math.pi - 90) % 360
        
        angleDiff = (midAngle - self.angle) % 360
        if angleDiff > 180:
            angleDiff -= 360

        self.angle += angleDiff * grouping

        ##separation
        for bird in flock:
            if bird.num != self.num:
                distance = calcdistance(self.x,self.y,bird.x,bird.y)
                if distance < selfVision:
                    xdiff = self.x - bird.x
                    ydiff = self.y - bird.y
                    angletoclose = (math.atan2(ydiff,xdiff) * 180/math.pi - 90) % 360
                    angleDifference = (angletoclose - (self.angle)) % 360
                    if angleDifference > 180:
                        angleDifference -= 360
                    self.angle -= separation * angleDifference * (selfVision-distance)
    
        ##toward centre of screen
        xdiff = self.x - 600
        ydiff = self.y - 300
        midAngle = (math.atan2(ydiff,xdiff) * 180/math.pi - 90) % 360
        
        angleDiff = (midAngle - self.angle) % 360
        if angleDiff > 180:
            angleDiff -= 360
        self.angle += angleDiff * centerOfScreen
        
        ##speed up far from centre
        self.speed -= (self.speed - (calcdistance(self.x,self.y,averageX,averageY)/50)) * speed
        ##speed towards average
        self.speed -= (self.speed - averageSpeed) * speedTowardsAverage
        
        if preditorEnabled:
            ##avoid preditor
            distance = calcdistance(self.x,self.y,preditor.x,preditor.y)
            if distance < preditorVision:
                xdiff = self.x - preditor.x
                ydiff = self.y - preditor.y
                angletoclose = (math.atan2(ydiff,xdiff) * 180/math.pi - 90) % 360
                angleDifference = (angletoclose - (self.angle)) % 360
                if angleDifference > 180:
                    angleDifference -= 360
                self.angle -= fear * angleDifference * (preditorVision-distance)
        ##movement
        self.x += self.speed*math.sin(self.angle * math.pi/180)
        self.y -= self.speed*math.cos(self.angle * math.pi/180)
    def updatePreditor(self):
        self.speed = preditorSpeed
        self.color = red
        #towards centre of group
        xdiff = self.x - averageX
        ydiff = self.y - averageY
        midAngle = (math.atan2(ydiff,xdiff) * 180/math.pi - 90) % 360
        
        angleDiff = (midAngle - self.angle) % 360
        if angleDiff > 180:
            angleDiff -= 360

        self.angle += angleDiff * preditorTurning
        
        ##movement
        self.x += self.speed*math.sin(self.angle * math.pi/180)
        self.y -= self.speed*math.cos(self.angle * math.pi/180)
        
def calcdistance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))


flock = []
for i in range(0,flockSize):
    flock.append(Bird(i))

if preditorEnabled:
    preditor = Bird(flockSize+1)

averageX = 0
averageY = 0
averageAngle = 0
averageSpeed = 0
totalX = 0
totalY = 0
totalAngle = 0
totalSpeed = 0

run = True
while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    win.fill(black)
    for bird in flock:
        bird.update()
        bird.draw()
        totalX += bird.x
        totalY += bird.y
        totalAngle += bird.angle
        totalSpeed += bird.speed
    averageX = totalX / flockSize
    averageY = totalY / flockSize
    averageAngle = totalAngle / flockSize
    averageSpeed = totalSpeed / flockSize
    totalX = 0
    totalY = 0
    totalAngle = 0
    totalSpeed = 0
    if preditorEnabled:
        preditor.updatePreditor()
        preditor.draw()
    pygame.display.update()
pygame.quit()
    

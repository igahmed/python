#MODULES
from cgitb import text
from re import X
from tkinter import Y
from turtle import distance
import pygame
import sys
import math
import numpy
import random
from pygame import mixer


#INITIALIZING PYGAME
pygame.init()

#SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(X,Y):
    score= font.render("Score :" + str(score_value),True,(255,255,255))
    screen.blit(score,(X,Y))
#HIGHSCORE
highscore = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
def highscore(X,Y):
    if 'high_score' >= str(score_value):
            high_score = font.render("Highscore:"+str(score_value),True,(255,255,255))
    screen.blit(high_score,(10,50))
#gameover
#SCORE
game_over_text = 0
font = pygame.font.Font('freesansbold.ttf', 62)
textX = 10
textY = 10
#restarttext
restart = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
def gameover():
    gameovertext= font.render("GAME OVER" ,True,(255,255,255))
    screen.blit(gameovertext,(300,250))
    
def restart_text(X,Y):
    if game_over_text == True:
        restart1= font.render("PRESS 1 FOR RESTART GAME" ,True,(255,255,255))
        screen.blit(restart1,(200,350))

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
#DISPLAY
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("ROCKET")
icon = pygame.image.load('rocket.png')
icon= pygame.display.set_icon((icon))
#BACKGROUND
background = pygame.image.load('background.png')


#PLAYER
playerImg = pygame.image.load('player.png')
playerX = 360
playerY = 480
playerX_change = 0
def player(X,Y):
    screen.blit(playerImg,(X,Y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(2)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

#FOR BULLET
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))
#collision
def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#MAIN LOOP 
running = True
while running:                                      #FOR RUNNING
    screen.fill((0,0,0))                            # DISPLAY COLOR 
    screen.blit(background,(0,0)) 
    
               #BACKGROUND IMAG
    enemy(enemyX[i],enemyY[i],i)
    enemyY[i] += enemyY_change[i]                                                # fire_bullet(playerX,bulletY)
    
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
       
    if bullet_state is "fire":
       
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    bulletY-=bulletY_change
    
    playerX+=playerX_change#FOR PLAYER  
    for i in range(num_of_enemies):
        
        
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                    enemyY[j] = 2000
            gameover()
            break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
                             
    # #for collision
    collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
    if collision:
        collision_Sound =mixer.Sound("explosion.wav")
        collision_Sound.play()
        bulletY= 480
        bullet_state = "ready"
        
        score_value+=1
        show_score(textX,textY)
        
        enemyX[i] = random.randint(10,735)
        enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i], i)

    if playerX <=0:
        playerX = 8
    elif playerX>= 736:
        playerX = 8
    player(playerX,playerY)
    show_score(textX,textY)
    highscore(600,200)
    pygame.display.flip()                                 #FOR RUNNING
    for event in pygame.event.get():                      #EVENT
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:                  #FOR CONTROL KEYBOARD KEYS
            if event.key == pygame.K_LEFT:
                playerX_change =-5
            if event.type == pygame.K_DOWN:
                print("kdkh")
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                        bulletSound = mixer.Sound("awm.wav.mp3")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                       

            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
     
#FOR CALLING FUNCTION    
    

#FOR UPDATING DISPLAY AND THIS IS IMPORTANT SYNTEX
    # show_score(textX,textY)
pygame.display.update()     
#FOR QUIT PYGAME       
pygame.quit()  

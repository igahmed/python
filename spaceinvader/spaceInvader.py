import pygame
import sys
import math
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("ROCKET")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Load Background
background = pygame.image.load('background.png')

# Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Fonts
score_font = pygame.font.Font('freesansbold.ttf', 32)
gameover_font = pygame.font.Font('freesansbold.ttf', 62)

# Score
score_value = 0
high_score_value = 0

def show_score(x, y):
    score = score_font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_high_score(x, y):
    high_score = score_font.render(f"Highscore: {max(score_value, high_score_value)}", True, (255, 255, 255))
    screen.blit(high_score, (x, y))

# Game Over Text
def show_game_over():
    over_text = gameover_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))

def show_restart_text():
    restart = score_font.render("PRESS 1 TO RESTART", True, (255, 255, 255))
    screen.blit(restart, (250, 350))

# Player
playerImg = pygame.image.load('player.png')
playerX = 360
playerY = 480
playerX_change = 0

def draw_player(x, y):
    screen.blit(playerImg, (x, y))

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

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

def draw_enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Collision Detection
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    return distance < 27

# Game Loop
running = True
game_over = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    playerX = max(0, min(playerX, 736))  # keep player within screen

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Enemy movement and collision
    for i in range(num_of_enemies):
        if enemyY[i] > 600:
            game_over = True
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        # Check collision
        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        draw_enemy(enemyX[i], enemyY[i], i)

    draw_player(playerX, playerY)
    show_score(10, 10)
    show_high_score(600, 10)

    if game_over:
        show_game_over()
        show_restart_text()

    pygame.display.update()

pygame.quit()

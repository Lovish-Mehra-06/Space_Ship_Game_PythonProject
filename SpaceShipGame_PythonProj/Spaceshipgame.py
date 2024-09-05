################ # Space Ship Game By Lovish Mehra With Help of freeCodeCamp.org



































import pygame
import random
import math
from pygame import mixer

# Intialize the pygame
pygame.init()

# Create the Screen
screen = pygame.display.set_mode((800, 600))
# Create Background Screen
background = pygame.image.load("BackgroundSpace_Spaceshipgame.png")

# Background Sound
mixer.music.load("backgroundsound_Spaceshipgame.wav")
mixer.music.play(-1)

# Title & Icon
pygame.display.set_caption("Space Ship Game")
Icon = pygame.image.load("Icon_Spaceshipgame.png")
pygame.display.set_icon(Icon)

# Player Resource & Position
PlayerImg = pygame.image.load("Player_Spaceshipgame.png")
Playerx = 368  # Not more than 800 - 64 =736
Playerx_change = 0  # Only X Axis i.e Coordinates to be Changed i.e. Left or Right
Playery = 500  # Not more than 600 - 64 =536

# EnemyArrayList
EnemyImg = []
Enemyx = []
Enemyy = []
Enemyx_change = []
Enemyy_change = []
num_of_enemies = 5 #### No./Number of Enemies ------------------------------------
for i in range(num_of_enemies):
    # Enemy Resource & Position
    EnemyImg.append(pygame.image.load("Enemyship_Spaceshipgame.png"))
    Enemyx.append(random.randint(0, 736))
    Enemyy.append(random.randint(50, 150))
    Enemyx_change.append(3)
    Enemyy_change.append(40)

# Bullet Resource & Position
BulletImg = pygame.image.load("Bullet_Spaceshipgame.png")
Bulletx = 0
Bullety = 500
Bulletx_change = 0
Bullety_change = 15  # # --> Also speed Of Bullet
Bullet_state = "ready"  # 'ready' - you can't see bullet & 'fire' - bullet currently moving

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# Game Over
game_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(Sx, Sy):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (Sx, Sy))


def game_over_text(x, y):
    game_font_varible2 = game_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_font_varible2, (x, y))


def Player(Px, Py):
    screen.blit(PlayerImg, (Px, Py))


def Enemy(Ex, Ey, i):
    screen.blit(EnemyImg[i], (Ex, Ey))


def fire_bullet(Bx, By):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (Bx + 16, By + 10))


def iscollidenemybullet(Ex, Ey, Bx, By):  # Distance b/w Enemy & Bullet
    disbw_ship_bullet = math.sqrt((math.pow(Ex - Bx, 2) + math.pow(Ey - By, 2)))
    if disbw_ship_bullet < 27:
        return True
    else:
        return False


# Game Loop
running = True

while running:

    # Background RGB Colour ...
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Playerx_change = -7  # # --> Also speed Of Player
            if event.key == pygame.K_RIGHT:
                Playerx_change = 7  # # --> Also speed Of Player
            if event.key == pygame.K_SPACE:
                if Bullet_state == "ready":
                    Bullet_sound = mixer.Sound("laser_Spaceshipgame.wav")
                    Bullet_sound.play()
                    Bulletx = Playerx
                    fire_bullet(Bulletx, Bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Playerx_change = 0

    Playerx += Playerx_change  # Player movement
    ### Give The Restriction/Boarders for the SpaceShip to Move ###
    if Playerx <= 0:
        Playerx = 0
    elif Playerx >= 736:
        Playerx = 736

    for i in range(num_of_enemies):
 
        # Game Over
        if Enemyy[i] > 440:  # #######------> Distance to get Game Over
            for j in range(num_of_enemies):
                Enemyy[j] = 2000  # Moving Enemies out of Screen
            game_over_text(200, 300)
            break

        Enemyx[i] += Enemyx_change[i]  # Enemy movement
        ### Movement of EnemyShip ###
        if Enemyx[i] <= 0:
            Enemyx_change[i] = 5  # # --> Also speed Of Enemy
            Enemyy[i] += Enemyy_change[i]
        elif Enemyx[i] >= 736:
            Enemyx_change[i] = -5  # # --> Also speed Of Enemy
            Enemyy[i] += Enemyy_change[i]

        # Check collision
        coollision = iscollidenemybullet(Enemyx[i], Enemyy[i], Bulletx, Bullety)
        if coollision:
            coollision_sound = mixer.Sound("explosion_Spaceshipgame.wav")
            coollision_sound.play()
            Bullety = 500
            Bullet_state = "ready"
            score_value += 1
            Enemyx[i] = random.randint(0, 736)
            Enemyy[i] = random.randint(50, 150)

        Enemy(Enemyx[i], Enemyy[i], i)

    # Bullet Movement Multiple times
    if Bullety <= 0:
        Bullety = 500
        Bullet_state = "ready"

    # Bullet Movement
    if Bullet_state == "fire":
        fire_bullet(Bulletx, Bullety)
        Bullety -= Bullety_change

    Player(Playerx, Playery)
    show_score(textx, texty)
    pygame.display.update()  # Imp--> Update the display

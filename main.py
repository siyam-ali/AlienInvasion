# Alien Invaders! is a two-player game that allows Player 1 to use the WASD keys and Player 2 to use
# the UP, DOWN, LEFT, and RIGHT arrow keys to control their respective Aliens in order to invade Earth.
# Players can increase their score by navigating through asteroid objects and reaching the Earth.

import pygame
import random

pygame.init()
pygame.mixer.init()

# Here we will initialize some global variables and game assets

screenWidth = 800
screenHeight = 800

initialYPosition = 650 # the initial Y coordinate for both players
speed = 3 # this is the constant speed used for both x and y velocity

windowIcon = pygame.image.load('gameAssets/icon.png')
background = pygame.image.load('gameAssets/spaceBackground.png')
asteroid = pygame.image.load('gameAssets/asteroid.png')
alien = pygame.image.load('gameAssets/alien.png')
music = pygame.mixer.music.load('gameAssets/spaceMusic.mp3')
pygame.mixer.music.play(-1)

gameClock = pygame.time.Clock()
gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Alien Invasion!')
pygame.display.set_icon(windowIcon)

# Collision class is a parent class of the classes Player and Asteroid since we want to use this class
# to check if there is a collision at any given time

class Collision():

    # collide function will check for a possible collision between players and asteroids

    def collide(self, a):
        if self.x < (a.x + a.width) and self.x + self.width > (a.x + a.width):
            if self.y < (a.y + a.height) and self.y + self.height > (a.y + a.height):
                return True

        if self.x + self.width > a.x and self.x < a.x:
            if self.y < (a.y + a.height) and self.y + self.height > a.y:
                return True

        return False

class Player(Collision):

    # init method initializes player's x and y position, and dimension of player

    def __init__(self, x):
        self.x = x
        self.y = initialYPosition
        self.width = 50
        self.height = 100
        self.yVelocity = 0
        self.xVelocity = 0
        self.score = 0
        self.image = alien

    # draw function ensures that the program constantly displays images in the game window during every single frame

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def update_speed(self):
        self.y = self.y + self.yVelocity
        self.x = self.x + self.xVelocity

    def increaseScore(self):
        if self.y <= 100 and 350 <= self.x <= 450:
            self.score = self.score + 1
            self.y = initialYPosition

# The Asteroid class is responsible for generating random asteroids to come across the game window, from left or right
# Players must avoid the asteroids accordingly

class Asteroid(Collision):
    def __init__(self):
        self.width = 28
        self.height = 28
        self.image = asteroid
        self.y = random.randint(120, screenHeight - 200 - self.height)

        asteroidOrigin = random.choice([0,1]) # depending on the random number chosen, asteroids will appear from left or right
        if asteroidOrigin == 0:
            self.x = -50 - self.width
            self.xVelocity = 2
        else:
            self.x = 50 + screenWidth
            self.xVelocity = -2

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = self.x + self.xVelocity

# main function for opening and keeping the game window active

def drawGame():
    gameWindow.blit(background, (0,0))
    player1.draw(gameWindow)
    player2.draw(gameWindow)
    for a in asteroids:
        a.draw(gameWindow)

    scoreFont = pygame.font.SysFont('geneva', 50)
    player1Score = scoreFont.render(str(player1.score), 1, (0, 128, 0))
    player2Score = scoreFont.render(str(player2.score), 1, (0, 128, 0))
    gameWindow.blit(player1Score, (184 - player1Score.get_width()/2, 730))
    gameWindow.blit(player2Score, (600 - player2Score.get_width()/2, 730))

    pygame.display.update()



player1 = Player(160)
player2 = Player(575)
asteroids = []
count = 0

# the main while loop of our program, game continues to run until user closes the game tab
run = True
while run:
    gameClock.tick(75)
    player1.update_speed()
    player2.update_speed()

    player1.increaseScore()
    player2.increaseScore()

    count += 1
    if count % 30 == 0:
        asteroids.append(Asteroid())

    for a in asteroids:
        a.move()
        if a.xVelocity > 0 and a.x > screenWidth:
            asteroids.pop(asteroids.index(a))
        elif a.xVelocity < 0 and a.x < -a.width:
            asteroids.pop(asteroids.index(a))

        # check for collisions with aliens here, and resets the corresponding player position to the default positions

        if player1.collide(a):
            asteroids.pop(asteroids.index(a))
            player1.y = initialYPosition
            player1.x = 160

        if player2.collide(a):
            asteroids.pop(asteroids.index(a))
            player2.y = initialYPosition
            player2.x = 575

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # depending on which key player 1 or player 2 presses, vertical and horizontal velocity will be calculated accordingly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player1.yVelocity = speed
            if event.key == pygame.K_w:
                player1.yVelocity = speed * -1
            if event.key == pygame.K_a:
                player1.xVelocity = speed * -1
            if event.key == pygame.K_d:
                player1.xVelocity = speed
            if event.key == pygame.K_DOWN:
                player2.yVelocity = speed
            if event.key == pygame.K_UP:
                player2.yVelocity = speed * -1
            if event.key == pygame.K_LEFT:
                player2.xVelocity = speed * -1
            if event.key == pygame.K_RIGHT:
                player2.xVelocity = speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player1.yVelocity = 0
            if event.key == pygame.K_w:
                player1.yVelocity = 0
            if event.key == pygame.K_a:
                player1.xVelocity = 0
            if event.key == pygame.K_d:
                player1.xVelocity = 0
            if event.key == pygame.K_DOWN:
                player2.yVelocity = 0
            if event.key == pygame.K_UP:
                player2.yVelocity = 0
            if event.key == pygame.K_LEFT:
                player2.xVelocity = 0
            if event.key == pygame.K_RIGHT:
                player2.xVelocity = 0

    drawGame()

pygame.quit()







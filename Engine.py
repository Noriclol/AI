import time
import Clock
import pygame
from AllLocations import *
from pygame.color import Color
from Actors import *

from Location import*

BLUE = Color("blue")
START_TIME = time.monotonic()


class Engine:
    gameClock = 0.0
    deltaTime = 0.0

    def __init__(self):
        pygame.init()
        self.logo = pygame.image.load("Assets/Sprites/gem.png")
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Coomer Game")
        self.screen = pygame.display.set_mode((1000, 700))

    def run(self):
        #
        speed = 100.0
        currentTime = 0.0
        lastTime = 0.0
        # init
        gameClock = Clock.Clock()


        Joe = Person(houseJoe, Factory, "joe", "Mama")
        #Jeff = Person(houseJeff, Office, "Jeff", "Bezos")

        personlist = [Joe]
        recreationalList = [Pub]

        for person in personlist:
            person.PersonInit()

        running = True
        while running:
            gameClock.Tick()
            gameClock.Time()
            for person in personlist:
                person.PersonUpdate()
                person.stateMachine.GetStats()

            # clock
            Engine.gameClock = time.monotonic() - START_TIME
            # EventHandler
            for event in pygame.event.get():
                # on Quit
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            # movement
            if keys[pygame.K_LEFT]:
                X = X - Engine.deltaTime * speed
            if keys[pygame.K_RIGHT]:
                X = X + Engine.deltaTime * speed
            if keys[pygame.K_UP]:
                Y = Y - Engine.deltaTime * speed
            if keys[pygame.K_DOWN]:
                Y = Y + Engine.deltaTime * speed
            # icon Switch
            if keys[pygame.K_1]:
                self.logo = pygame.image.load("Assets/Sprites/gem.png")
                pygame.display.set_icon(self.logo)
            if keys[pygame.K_2]:
                self.logo = pygame.image.load("Assets/Sprites/gem2.png")
                pygame.display.set_icon(self.logo)
            if keys[pygame.K_3]:
                self.logo = pygame.image.load("Assets/Sprites/gem3.png")
                pygame.display.set_icon(self.logo)
            if keys[pygame.K_4]:
                self.logo = pygame.image.load("Assets/Sprites/gem4.png")
                pygame.display.set_icon(self.logo)

            # Draw
            self.screen.fill(BLUE)
            #self.screen.blit(self.logo, (X, Y))
            pygame.display.flip()
            pygame.display.update()
            # clock
            currentTime = time.monotonic()
            Engine.deltaTime = currentTime - lastTime
            lastTime = currentTime


        
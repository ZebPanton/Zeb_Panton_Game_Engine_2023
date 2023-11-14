# This file was created by: Zeb Panton
# 
# content from kids can code: http://kidscancode.org/blog/

'''
############ Game Ideas ############
Doodle Jump
google dino 
Jetpack Joyride
Top down maze

############## To Do ##############
at random intervals mobs come in from the right
when mobs touch player --> player dies
    after player dies they can restart game from beginning
        game pauses on frame they died on
maybe seperate mobs so that more "cacti" show up then "pterodactyls"
    "cacti" = mobs that touch floor
    "pterodactyls" = mobs that fly and possibly have enough space to duck under
add ducking
point system: goes up as player goes on
**create spawning system**
    mob randomly spawns from 45 - 60 seconds
        !different from having a 1/60 chance to spawn every tick!
        genuinely have no idea how to do this rn so this is important
    better system to have a mob spawn like 1-2 seconds after another goes off screen probably
mob gets deleted after going off screen
    im under the assumption that would just keep going after leaving the screen
make game speed up the longer you go on
'''

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math


vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        # dont even know if this is the right place to put a mobspawner
        # basically put variable here so i can add to it every time the game loops
        self.mobspawner = 0
        # same thing here, i want it to randomize once and not a billion times so put it in init
        self.spawnrandomizer = randint(0,60)
        self.running = True
    
    def new(self):
        # create a group for all sprites
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        # for m in MOB_LIST:
        #     m = Mob(*m)
        #     self.all_sprites.add(m)
        #     self.all_mobs.add(m)

        # for m in range(0,10):
        #     m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "moving")
        #     self.all_sprites.add(m)
        #     self.all_mobs.add(m)

        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            

    def update(self):
        self.all_sprites.update()

        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5

                    
        # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.acc.y = 0
                print("ouch")
                self.score -= 1
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                    self.player.vel.y = -self.player.vel.y  

        # after a certain amount of loops this will spawn a mob and reset the timer
        if self.mobspawner == 60 + self.spawnrandomizer:
            m = Mob(WIDTH, HEIGHT - 40 - 60, 60, 60, "cactus")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
            self.mobspawner = 0 
            self.spawnrandomizer = randint(0,60)
            print("[SPAWNING MOB]")
            
        # print(self.spawnrandomizer)
        self.mobspawner += 1

                   

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.player.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()


pg.quit()

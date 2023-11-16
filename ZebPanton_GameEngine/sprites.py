import pygame as pg
from pygame.sprite import Sprite

from pygame.math import Vector2 as vec
import os
from settings import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((100, 100))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'Dino.png')).convert()
        # self.image.set_colorkey(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH / 6, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.score = 0
        self.alive
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_s]:
            self.image = pg.image.load(os.path.join(img_folder, 'DinoDuck.png')).convert()
            self.rect = self.image.get_rect()
        else:
            self.rect.center = (0,1)
            self.image = pg.image.load(os.path.join(img_folder, 'Dino.png')).convert()
            self.rect = self.image.get_rect()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        # CHECKING FOR COLLISION WITH MOBS HERE >>>>>
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        if mhits:
            print("u stink")
            # self.score -= 1 
            self.game.playing = False
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

class Mob(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.spawntimer = 0
        self.speed = 0
        if self.kind == "cactus":
            self.speed = 5
        elif self.kind == "moving":
            self.speed = 5

    def update(self):
        if self.kind == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
                self.rect.y += self.rect.h
        if self.kind == "cactus":
            self.rect.x -= self.speed
            # save this code for if i find out how to kill sprites
            if self.rect.x < 0 - self.rect.w:
                self.kill()
            
# just copied and pasted the mobs so
# credit: Chris Cozort for making whole thing basically
class Objective(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.spawntimer = 0
        self.speed = 0
        # self.playertouch = pg.sprite.spritecollide(self, self.game.player, False)
        if self.kind == "coin":
            self.speed = 10
    def update(self):
        if self.kind == "coin":
            self.rect.x -= self.speed
            if self.rect.x < 0 - self.rect.w: 
                self.kill()

class Button(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'RestartButton.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
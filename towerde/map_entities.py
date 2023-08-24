import pygame as pg
from copy import deepcopy
import random
from pygame.math import Vector2
from groups_towerde import WeaponsEquipped
from towerde_items import *
from groups_towerde import BossBullets


class Tower(pg.sprite.Sprite):

    def __init__(self, image, height, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = speed
        self.height = height
        self.pos = image.get_rect()
        self.hp = 15000000000
        self.max_hp = 1500
        self.level = 0
        self.skill_points = 10
        self.xp = 0
        self.xp_to_level = 100
        self.gold = 0

        # SKILLS
        self.enlightenment = 0

    def move(self):

        self.pos = self.pos.move(self.speed)
        if self.pos.right > 600:
            self.pos.left = 0
        if self.pos.right > 480:
            self.pos.right = 0

    def level_up(self):

        while self.xp >= self.xp_to_level:
            self.xp -= self.xp_to_level
            self.level += 1
            self.skill_points += 1
            self.xp_to_level += self.level * 100


class Goblin(pg.sprite.Sprite):

    def __init__(self, image, height, speed, map_width, map_height, level, tower_pos):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.pos = image.get_rect()
        self.map_width = map_width
        self.height = height
        self.speed = speed
        self.map_height = map_height
        self.level = level
        self.xp = 1 + level * 2
        self.hp = 15 + level * 15
        self.damage = 1 + 5 * level
        self.drop_chance = 0.02 + 0.01*level
        self.tower_pos = tower_pos
        self.bounty = 1
        self.velocity = [0, 0]
        self.direction = [0, 0]


        if level == 1:
            self.drop = Cannon(self.tower_pos,attack_speed=400)
        elif level ==2:
            self.drop = SniperRifle(self.tower_pos,attack_speed=800)
        else:
            self.drop = SniperRifle(self.tower_pos)

    def move(self):

        self.direction = [self.tower_pos.centerx - self.pos.x, self.tower_pos.centery - self.pos.y]

        if Vector2(self.direction).length() > 0:

            if random.random() > 0.1:

                self.direction = [self.tower_pos.centerx - self.pos.x, self.tower_pos.centery - self.pos.y]
                self.velocity = Vector2(self.direction).normalize()

                self.pos.x += self.velocity[0]
                self.pos.y += self.velocity[1]

            else:

                self.pos.x += random.choice(list(range(0, 3)))
                self.pos.y += random.choice(list(range(0, 3)))

        elif self.pos.collidepoint(self.tower_pos[0], self.tower_pos[1]):

            return True


class Boss1(pg.sprite.Sprite):

    def __init__(self, tower: Tower, screen: pg.surface.Surface):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("boss_1.png").convert_alpha(screen)
        self.pos = self.image.get_rect()
        self.pos.x, self.pos.y = self.pos.center
        self.tower = tower
        self.move_rect = pg.Rect(self.tower.pos.x, self.tower.pos.y, 300, 300)
        self.move_rect.center = self.tower.pos.x, self.tower.pos.y
        self.screen = screen
        self.hp = 1000
        self.damage = 30
        self.bullets = BossBullets()
        self.time = 0
        self.time_stamp = pg.time.Clock()

        self.drop = Cannon(tower_pos=self.tower.pos)
        self.drop_chance = 0.9
        self.xp = 100
        self.bounty = 1000

        self.atdir = None

    def move(self):

        if self.move_rect.colliderect(self.pos):

            if self.atdir == "Left":
                self.pos.x += 1
            if self.atdir == "Right":
                self.pos.x -= 1
            if self.atdir == "Up":
                self.pos.y -= 1
            if self.atdir == "Down":
                self.pos.y += 1

        else:

            self.atdir = random.choice(["Left", "Right", "Up", "Down"])

            self.direction = [self.tower.pos.centerx - self.pos.x, self.tower.pos.centery - self.pos.y]

            if Vector2(self.direction).length() > 0:

                if random.random() > 0.1:
                    self.direction = [self.tower.pos.centerx - self.pos.x, self.tower.pos.centery - self.pos.y]
                    self.velocity = Vector2(self.direction).normalize()

                    self.pos.x += self.velocity[0]
                    self.pos.y += self.velocity[1]



    def attack(self):

        # MELEE
        if self.pos.colliderect(self.tower.pos):

            self.tower.hp -= self.damage

        # RANGED
        if not self.pos.colliderect(self.tower.pos) and (abs(self.pos.x - self.tower.pos.x) + abs(self.pos.y - self.tower.pos.y)) < 400:

            bullet = self.create_bullet()
            bullet.add(self.bullets)
            self.time = 0

        else:
            self.time += self.time_stamp.get_time()

    def create_bullet(self):

        bullet = Boss1_bullet(tower=self.tower, boss_pos=self.pos)
        return bullet

    def update(self, screen):

        self.attack()
        self.move()




class Boss1_bullet(pg.sprite.Sprite):

    def __init__(self, tower: Tower, boss_pos):
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.bullet_image = pg.image.load("items_stuff/boss_bulley.png")
        self.bullet_pos = self.bullet_image.get_rect()
        self.bullet_pos.x, self.bullet_pos.y = boss_pos.x, boss_pos.y
        self.bullet_rect = (0, 0)
        self.damage = 10

    def update(self, screen: pg.surface.Surface):

        direction = [self.tower.pos.x - self.bullet_pos.centerx, self.tower.pos.centery - self.bullet_pos.y]
        if Vector2(direction).length() > 0:

            self.bullet_velocity = Vector2(direction).normalize() * 10
            self.bullet_pos.x += self.bullet_velocity[0]
            self.bullet_pos.y += self.bullet_velocity[1]
            self.bullet_pos.center = (self.bullet_pos.x, self.bullet_pos.y)
            screen.blit(self.bullet_image, self.bullet_pos)

        if self.bullet_pos.colliderect(self.tower.pos):
            self.tower.hp -= self.damage
            self.kill()


if __name__ == '__main__':

    pass

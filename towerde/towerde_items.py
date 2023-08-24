import pygame as pg
from copy import deepcopy
from pygame import Vector2
import random


class Cannon(pg.sprite.Sprite):

    def __init__(self, tower_pos=None, attack_speed = 150, damage = 10):
        pg.sprite.Sprite.__init__(self)
        self.bullet_image = pg.image.load("items_stuff/ctverec.png")
        self.image = pg.image.load("items_stuff/cannon.png")
        self.pos = self.image.get_rect()
        self.drop_image = pg.image.load("items_stuff/cannon_drop.png")
        self.drop_pos = self.drop_image.get_rect()
        if tower_pos:
            self.bullet_pos = pg.rect
            self.bullet_pos.x = deepcopy(tower_pos.center[0])
            self.bullet_pos.y = deepcopy(tower_pos.center[1])
        # NAME
        self.name = "Cannon"
        # STATS
        self.attack_speed = attack_speed
        self.base_attack_speed = attack_speed
        self.range = 150
        self.base_rage = 150
        self.damage = damage
        self.base_damage = damage
        self.time = 0
        self.cost = 100

    def create_bullet(self, enemy_target, enemy_group):

        current_bullet = BulletCannon(self.damage, enemy_target, self.bullet_pos, enemy_group)
        return current_bullet

    def drop(self, enemy):

        self.drop_pos = self.image.get_rect(center = (enemy.pos.x, enemy.pos.y))
        return self.drop_image, self.drop_pos

class SniperRifle(pg.sprite.Sprite):

    def __init__(self, tower_pos=None, attack_speed = 600, damage = 100):
        pg.sprite.Sprite.__init__(self)
        self.bullet_image = pg.image.load("items_stuff/sniper_bullet.png")
        self.image = pg.image.load("items_stuff/sniper.png")
        self.pos = self.image.get_rect()
        self.drop_image = pg.image.load("items_stuff/cannon_drop.png")
        self.drop_pos = self.drop_image.get_rect()
        self.tower_pos = tower_pos
        if tower_pos:
            self.bullet_pos = pg.rect
            self.bullet_pos.x = deepcopy(tower_pos.center[0])
            self.bullet_pos.y = deepcopy(tower_pos.center[1])
        # NAME
        self.name = "Cannon_2"
        # STATS
        self.attack_speed = attack_speed
        self.base_attack_speed = attack_speed
        self.range = 1500
        self.base_rage = 1500
        self.min_range = 100
        self.damage = damage
        self.base_damage = damage
        self.time = 0
        self.cost = 100

    def predict(self, enemy_target):

        enemx = deepcopy(enemy_target.pos.x)
        enemy = deepcopy(enemy_target.pos.y)
        direction_og = [self.tower_pos.centerx - enemy_target.pos.x, self.tower_pos.centery - enemy_target.pos.y]
        vector_len = Vector2(direction_og).length()
        coords = [enemx, enemy]
        enemy_move = 0
        bullet_move = 0
        control = 0

        while True:

            control += 1
            direction = [self.tower_pos.centerx - enemx, self.tower_pos.centery - enemy]
            velocity = Vector2(direction).normalize()

            enemx += velocity[0]
            enemy += velocity[1]
            coords = [enemx, enemy]

            enemy_move += vector_len
            bullet_move += 25

            if bullet_move >= vector_len - enemy_move:

                return coords
            if control > 5:

                return None

    def create_bullet(self, enemy_target, enemy_group):

        prediction = self.predict(enemy_target)
        current_bullet = SniperRifleBullet(self.damage, enemy_target, self.bullet_pos, enemy_group, prediction=prediction)

        return current_bullet

    def drop(self, enemy):

        self.drop_pos = self.image.get_rect(center = (enemy.pos.x, enemy.pos.y))
        return self.drop_image, self.drop_pos


class BulletCannon(pg.sprite.Sprite):

    def __init__(self, damage, enemy_target, pos, enemy_group):
        pg.sprite.Sprite.__init__(self)
        self.bullet_image = pg.image.load("items_stuff/ctverec.png")
        self.bullet_pos = self.bullet_image.get_rect()
        self.bullet_pos.x, self.bullet_pos.y = pos.x, pos.y
        self.bullet_rect = (0, 0)
        self.bullet_velocity = (0, 0)
        self.damage = damage
        self.enemy_target = enemy_target
        self.enemy_group = enemy_group

    def update(self, screen_rect):

        direction = [self.enemy_target.pos.x - self.bullet_pos.x, self.enemy_target.pos.y - self.bullet_pos.y]
        if Vector2(direction).length() > 0:
            self.bullet_velocity = Vector2(direction).normalize() * 10

            self.bullet_pos.x += self.bullet_velocity[0]
            self.bullet_pos.y += self.bullet_velocity[1]
            self.bullet_pos.center = (self.bullet_pos.x, self.bullet_pos.y)
            screen_rect.blit(self.bullet_image, self.bullet_pos)

        if self.bullet_pos.colliderect(self.enemy_target.pos):

            self.enemy_target.hp -= self.damage

        if not self.enemy_target.alive():

            self.kill()


class SniperRifleBullet(pg.sprite.Sprite):

    def __init__(self, damage, enemy_target, pos, enemy_group, prediction=None):
        pg.sprite.Sprite.__init__(self)
        self.bullet_image = pg.image.load("items_stuff/sniper_bullet.png")
        self.bullet_pos = self.bullet_image.get_rect()
        self.bullet_pos.x, self.bullet_pos.y = pos.x, pos.y
        self.bullet_rect = (0, 0)
        self.damage = damage
        self.enemy_target = enemy_target
        self.enemy_group = enemy_group
        if not prediction:
            self.direction = [self.enemy_target.pos.x - self.bullet_pos.x, self.enemy_target.pos.y - self.bullet_pos.y]
        else:
            self.direction = [prediction[0] - self.bullet_pos.x, prediction[1] - self.bullet_pos.y]
        self.bullet_velocity = Vector2(self.direction).normalize() * 25

    def update(self, screen_rect):

        x = deepcopy(self.bullet_pos.x)
        y = deepcopy(self.bullet_pos.y)
        self.bullet_pos.x += self.bullet_velocity[0]
        self.bullet_pos.y += self.bullet_velocity[1]
        self.bullet_pos.center = (self.bullet_pos.x, self.bullet_pos.y)
        screen_rect.blit(self.bullet_image, self.bullet_pos)

        for enemy in self.enemy_group.sprites():

            if self.bullet_pos.colliderect(enemy.pos):

                enemy.hp -= self.damage
                self.kill()
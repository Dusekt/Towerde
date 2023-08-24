import pygame as pg
from map_entities import Tower
from copy import deepcopy
from Hud import Inventory


class SkinOfSteel(pg.sprite.Sprite):
    # DONE
    def __init__(self, tower: Tower):
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.level = 0
        self.image = pg.image.load("./skill_stuff/skin_of_steel.png")
        self.pos = self.image.get_rect(center=(1,1))
        self.effect = False
        self.cost = 1
        self.base_cost = 1
        self.max_level = 5

    def level_up(self):
        self.level += 1
        self.tower.skill_points -= self.cost
        self.effect = True

    def do_effect(self):

        if self.effect:

            hp_save = deepcopy(self.tower.max_hp)
            self.tower.max_hp = int(self.tower.max_hp * (self.level * 0.2 + 1))
            self.tower.hp += abs(hp_save - self.tower.max_hp)
            self.effect = False
            print(self.__class__)


class Eclipse(pg.sprite.Sprite):
    # DONE
    def __init__(self,tower: Tower, inventory: Inventory):
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.inventory = inventory
        self.level = 0
        self.image = pg.image.load("./skill_stuff/eclipse.png")
        self.pos = self.image.get_rect(center=(1,1))
        self.effect = False
        self.cost = 1
        self.base_cost = 1
        self.max_level = 5

    def level_up(self):
        self.level = self.level + 1
        self.tower.skill_points -= self.cost
        self.effect = True

    def do_effect(self):

        if self.effect:

            self.inventory.eclipse = self.level
            self.effect = False
            print(self.__class__)


class Bash(pg.sprite.Sprite):
    # DONE
    def __init__(self, tower: Tower):
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.level = 0
        self.image = pg.image.load("./skill_stuff/bash.png")
        self.pos = self.image.get_rect(center=(1,1))
        self.effect = False
        self.base_chance = 1
        self.chance = 1
        self.cost = 1
        self.base_cost = 1
        self.max_level = 5


    def level_up(self):
        self.level += 1
        self.tower.skill_points -= self.cost
        self.effect = True

    def do_effect(self):

        if self.effect:
            print(self.__class__)
            self.chance = self.base_chance * (1 - self.level * 0.1)
            self.effect = False


class Surge(pg.sprite.Sprite):
    # DONE
    def __init__(self, tower: Tower, inventory: Inventory):
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.inventory = inventory
        self.level = 0
        self.image = pg.image.load("./skill_stuff/surge.png")
        self.pos = self.image.get_rect(center=(1, 1))
        self.effect = False
        self.cost = 1
        self.base_cost = 1
        self.max_level = 5


    def level_up(self):
        self.level += 1
        self.tower.skill_points -= self.cost
        self.effect = True

    def do_effect(self):

        if self.effect:
            self.inventory.surge = self.level
            print(self.__class__)
            self.effect = False


class Enlightenment(pg.sprite.Sprite):
    # DONE
    def __init__(self, tower: Tower):
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.level = 0
        self.image = pg.image.load("./skill_stuff/enlightenment.png")
        self.pos = self.image.get_rect(center=(1,1))
        self.effect = False
        self.cost = 1
        self.base_cost = 1
        self.max_level = 5

    def level_up(self):
        self.level += 1
        self.tower.skill_points -= self.cost
        self.effect = True

    def do_effect(self):

        if self.effect:
            print(self.__class__)
            self.tower.enlightenment = 1 + 0.2 * self.level
            self.effect = False


class Efficiency(pg.sprite.Sprite):
    # DONE
    def __init__(self, tower: Tower):
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.level = 0
        self.image = pg.image.load("./skill_stuff/efficiency.png")
        self.pos = self.image.get_rect(center=(1,1))
        self.effect = False
        self.cost = 1
        self.base_cost = 1
        self.control_level = 1
        self.max_level = 3

    def level_up(self):
        self.level += 1
        self.tower.skill_points -= self.cost

    def do_effect(self, skills=None):

        if self.effect and isinstance(skills, list):
            for skill in skills:
                if hasattr(skill, "base_cost") and hasattr(skill, "cost"):
                    skill.cost = skill.base_cost * (1 - self.level*0.2)
                    print("cost reduced")

        self.effect = False

class Greed(pg.sprite.Sprite):
    # DONE
    def __init__(self, tower: Tower, enemies: list):
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.level = 0
        self.image = pg.image.load("./skill_stuff/greed.png")
        self.pos = self.image.get_rect(center=(1,1))
        self.effect = False
        self.cost = 1
        self.base_cost = 1
        self.max_level = 5
        self.enemies = enemies

    def level_up(self):
        self.level += 1
        self.tower.skill_points -= self.cost
        self.effect = True

    def do_effect(self):
        if self.effect:

            for enemy in self.enemies:
                if hasattr(enemy, "bounty"):
                    enemy.bounty = float(enemy.bounty * (self.level*0.2 + 1))

            self.effect = False
            print(self.__class__)


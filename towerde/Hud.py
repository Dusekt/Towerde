import pygame as pg
from map_entities import Tower
from groups_towerde import WeaponsEquipped


class Inventory(pg.sprite.Sprite):

    def __init__(self, screen:pg.surface.Surface):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("inventar.png")
        self.pos = self.image.get_rect()
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.pos.x, self.pos.y = 0, 480*self.height/680
        self.switch = False
        self.inventory = {"slot1": InventorySlot((55*(self.width/800), 499*(self.height/680))),
                          "slot2": InventorySlot((228*(self.width/800), 499*(self.height/680))),
                          "slot3": InventorySlot((400*(self.width/800), 499*(self.height/680))),
                          "slot4": InventorySlot((55*(self.width/800), 590*(self.height/680))),
                          "slot5": InventorySlot((228*(self.width/800), 590*(self.height/680))),
                          "slot6": InventorySlot((400*(self.width/800), 590*(self.height/680))),
                          }
        self.backpack = {"bslot1": InventorySlot((1, 2)),
                         "bslot2": InventorySlot((2, 1)),
                         "bslot3": InventorySlot((3, 4)),
                         }
        # BUFFS

        self.eclipse = 0
        self.surge = 0

    def toggle(self, screen):
        if not self.switch:
            self.switch = True
            screen.blit(self.image, self.pos)

            for slot, weapon in self.inventory.items():

                if isinstance(weapon.status, pg.sprite.Sprite):
                    weapon.status.pos.center = weapon.pos.center
                    screen.blit(weapon.status.image, weapon.status.pos)

        else:
            self.switch = False
            screen.fill("gray")

    def update(self, screen):

        screen.blit(self.image, self.pos)

        for slot, weapon in self.inventory.items():

            if isinstance(weapon.status, pg.sprite.Sprite):
                weapon.status.pos.center = weapon.pos.center
                screen.blit(weapon.status.image, weapon.status.pos)

        self.buff_weapons()

    def buff_weapons(self):

        if self.eclipse > 0:
            for item in self.inventory.values():
                if isinstance(item.status, pg.sprite.Sprite) \
                        and hasattr(item.status, "damage") \
                        and hasattr(item.status, "base_damage"):

                    # ENSURES THAT DMG CAN ONLY EFFECT WEAPON ONCE
                    # number on self.eclipse ect must be scaled with damage increase to have effect
                    while item.status.base_damage + self.eclipse > item.status.damage:
                        item.status.damage += 1

        if self.surge > 0:
            for item in self.inventory.values():
                if isinstance(item.status, pg.sprite.Sprite) \
                        and hasattr(item.status, "attack_speed") \
                        and hasattr(item.status, "base_attack_speed"):

                    # ENSURES THAT ATTACK SPEED CAN ONLY EFFECT WEAPON ONCE
                    while item.status.base_attack_speed - self.surge*10 < item.status.attack_speed:
                        item.status.attack_speed -= 10

    def rescale(self, new_screen):

        self.screen = new_screen
        self.width, self.height = self.screen.get_size()
        self.pos.x, self.pos.y = 0, 480*self.height/680
        self.image = pg.transform.scale(self.image, (600*self.width/800, 200*self.height/680))
        for slot, value in self.inventory.items():

            value.pos = pg.Rect(0, 0, 127 * self.width / 800, 67 * self.height / 680)
            if slot == "slot1":
                value.pos.x, value.pos.y = (55 * (self.width / 800), 499 * (self.height / 680))
            if slot == "slot2":
                value.pos.x, value.pos.y = (228 * (self.width / 800), 499 * (self.height / 680))
            if slot == "slot3":
                value.pos.x, value.pos.y = (400 * (self.width / 800), 499 * (self.height / 680))
            if slot == "slot4":
                value.pos.x, value.pos.y = (55 * (self.width / 800), 590 * (self.height / 680))
            if slot == "slot5":
                value.pos.x, value.pos.y = (228 * (self.width / 800), 590 * (self.height / 680))
            if slot == "slot6":
                value.pos.x, value.pos.y = (400 * (self.width / 800), 590 * (self.height / 680))

class InventorySlot(pg.sprite.Sprite):

    def __init__(self, pos: tuple):
        pg.sprite.Sprite.__init__(self)
        self.status = "Empty"
        self.pos = pg.Rect(pos[0], pos[1], 127, 67)
        self.pos.x = pos[0]
        self.pos.y = pos[1]


class Hud(pg.sprite.Sprite):

    def __init__(self, screen):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("hud3.png")
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.pos = self.image.get_rect()
        self.pos.x, self.pos.y = 600*self.width/800, 0
        self.hud = {"slot1": HudSlot((602*self.width/800, 7*self.height/680)),
                    "slot2": HudSlot((602*self.width/800, 142*self.height/680)),
                    "slot3": HudSlot((602*self.width/800, 280*self.height/680)),
                    "slot4": HudSlot((702*self.width/800, 7*self.height/680)),
                    "slot5": HudSlot((702*self.width/800, 142*self.height/680)),
                    "slot6": HudSlot((702*self.width/800, 280*self.height/680))}

    def update(self, screen):

        screen.blit(self.image, self.pos)
        for slot, skill in self.hud.items():

            if isinstance(skill.status, pg.sprite.Sprite):
                skill.status.x, skill.status.y = skill.pos.x, skill.pos.y
                skill.status.pos.center = skill.pos.center
                screen.blit(skill.status.image, skill.status.pos)

    def rescale(self, new_screen):

        self.screen = new_screen
        self.width, self.height = self.screen.get_size()
        self.pos.x, self.pos.y = 600*self.width/800, 0
        self.image = pg.transform.scale(self.image, (200 * self.width / 800, 680 * self.height / 680))
        for slot, value in self.hud.items():

            value.pos = pg.Rect(0, 0, 94 * self.width / 800, 128 * self.height / 680)
            if slot == "slot1":
                value.pos.x, value.pos.y = (602*self.width/800, 7*self.height/680)
            if slot == "slot2":
                value.pos.x, value.pos.y = (602*self.width/800, 142*self.height/680)
            if slot == "slot3":
                value.pos.x, value.pos.y = (602*self.width/800, 280*self.height/680)
            if slot == "slot4":
                value.pos.x, value.pos.y = (702*self.width/800, 7*self.height/680)
            if slot == "slot5":
                value.pos.x, value.pos.y = (702*self.width/800, 142*self.height/680)
            if slot == "slot6":
                value.pos.x, value.pos.y = (702*self.width/800, 280*self.height/680)

class HudSlot(pg.sprite.Sprite):

    def __init__(self, pos: tuple):
        pg.sprite.Sprite.__init__(self)
        self.status = "Empty"
        self.pos = pg.Rect(pos[0], pos[1], 94, 128)
        self.pos.x = pos[0]
        self.pos.y = pos[1]


class Stats(pg.sprite.Sprite):

    def __init__(self, tower: Tower, weapons: WeaponsEquipped):
        pg.sprite.Sprite.__init__(self)
        self.weapons = weapons
        self.tower = tower
        self.pos = pg.rect.Rect(600, 410, 200, 271)

    def make_texts(self):

        DPS = 0
        for weapon in self.weapons.sprites():
            DPS += weapon.damage/(weapon.attack_speed/1000)
        text_list = []
        stats_list = [
            f"Tower HP: {int(self.tower.hp)}/{int(self.tower.max_hp)}",
            f"Tower LVL: {int(self.tower.level)}",
            f"SKILL POINTS: {self.tower.skill_points:.1f}",
            f"Tower XP: {int(self.tower.xp)}/{int(self.tower.xp_to_level)}",
            f"GOLD: {self.tower.gold:.1f}",
            f"DPS: {DPS:.1f}"
        ]
        for index, t in enumerate(stats_list):
            font = pg.font.Font(None, 18)
            txt = t
            text = font.render(txt, True, "red")
            text_pos = text.get_rect(center=(self.pos.centerx, self.pos.y + 10 + index * 20))
            text_list.append((text, text_pos))

        return text_list

    def update(self, screen):

        texts = self.make_texts()
        for i in texts:
            screen.blit(i[0], i[1])

    def rescale(self, screen):

        width, height = screen.get_size()
        self.pos = pg.rect.Rect(600*width/800, 410*height/680, 200*width/800, 271*height/680)



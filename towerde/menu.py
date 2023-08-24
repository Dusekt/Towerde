import pygame as pg
import os
from groups_towerde import OtherItems, StoreItems, Texts
from random import choice
from map_entities import Cannon
from copy import copy, deepcopy
from towerde_player import TowerdePlayer


class StoreSlot(pg.sprite.Sprite):

    def __init__(self, screen: pg.surface.Surface, pos: tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("menu_stuff/inventory_slot_store.png").convert(screen)
        self.pos = self.image.get_rect()
        self.pos.center = pos
        self.hold = None


class PlayerSlot(pg.sprite.Sprite):

    def __init__(self, screen: pg.surface.Surface, pos: tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("menu_stuff/inventory_slot_player.png").convert(screen)
        self.pos = self.image.get_rect()
        self.pos.center = pos
        self.hold = None


class TowerdeStore(pg.sprite.Sprite):

    def __init__(self, screen: pg.surface.Surface = None):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("menu_stuff/shop_0.png")
        self.pos = self.image.get_rect()
        self.pos.x, self.pos.y = 0, 0

        # rect used to toggle store and menu + re roll the store

        self.back_rect = pg.Rect(0, 0, 400, 100)
        self.refresh_rect = pg.Rect(400, 0, 400, 100)

        # this is how info in the store will be visualized
        self.items_builder = {
            "name": {
                "cost": int,
                "required_level": int,
                "object": object,
                "attack_speed": int,
                "damage": int,
                "range": int
            }
        }
        # sprites of items currently in the store
        self.items = StoreItems()
        # sprites of all items in the game to make the store from
        self.all_items = ["Cannon", "Cannon"]
        self.items_to_store = []
        # holder of current slot hold
        self.items_dict = {}
        # used for holding item, blit ect...
        self.store_inventory = {"slot_1": StoreSlot(screen, pos=(self.pos.centerx * (1/3), 440 + 60)),
                                "slot_2": StoreSlot(screen, pos=(self.pos.centerx * (2/3), 440 + 60)),
                                "slot_3": StoreSlot(screen, pos=(self.pos.centerx, 440 + 60)),
                                "slot_4": StoreSlot(screen, pos=(self.pos.centerx * (4/3), 440 + 60)),
                                "slot_5": StoreSlot(screen, pos=(self.pos.centerx * (5/3), 440 + 60)),
                                "slot_6": StoreSlot(screen, pos=(self.pos.centerx * (1/3), 440 + 180)),
                                "slot_7": StoreSlot(screen, pos=(self.pos.centerx * (2/3), 440 + 180)),
                                "slot_8": StoreSlot(screen, pos=(self.pos.centerx, 440 + 180)),
                                "slot_9": StoreSlot(screen, pos=(self.pos.centerx * (4/3), 440 + 180)),
                                "slot_10": StoreSlot(screen, pos=(self.pos.centerx * (5/3), 440 + 180))
                                }

        self.player_store_inventory = \
            dict(slot_1=StoreSlot(screen, pos=(527 + ((800 - 527) / 2) * 1/2, 102 + (1 / 4) * (680 - 102) / 2)),
                 slot_2=StoreSlot(screen, pos=(527 + ((800 - 527) / 2) * 1/2, 102 + (2 / 4) * (680 - 102) / 2)),
                 slot_3=StoreSlot(screen, pos=(527 + ((800 - 527) / 2) * 1/2, 102 + (3 / 4) * (680 - 102) / 2)),
                 slot_4=StoreSlot(screen, pos=(527 + ((800 - 527) / 2) * 1/2, 102 + (4 / 4) * (680 - 102) / 2)),
                 slot_5=StoreSlot(screen, pos=(527 + ((800 - 527) / 2) * 3/2, 102 + (1 / 4) * (680 - 102) / 2)),
                 slot_6=StoreSlot(screen, pos=(527 + ((800 - 527) / 2) * 3/2, 102 + (2 / 4) * (680 - 102) / 2)),
                 slot_7=StoreSlot(screen, pos=(527 + ((800 - 527) / 2) * 3/2, 102 + (3 / 4) * (680 - 102) / 2)),
                 slot_8=StoreSlot(screen, pos=(527 + ((800 - 527) / 2) * 3/2, 102 + (4 / 4) * (680 - 102) / 2)))

        self.font = pg.font.SysFont("arial", 18)

    """
    randomly chooses items from the game and creates a dictionary of stats, places them in an empty slot
    """
    def build_store(self):
        name = ""
        for slot in self.store_inventory.values():
            #if slot.hold and isinstance(slot.hold, object):
                #del slot.hold
            slot.hold = None

        for text_item in self.all_items:

            klass = globals()[text_item]
            real_item = klass()
            self.items_to_store.append(real_item)

        for slot in self.store_inventory.values():

            if not slot.hold and len(self.items_to_store) > 0:
                slot.hold = choice(self.items_to_store)
                slot.hold.add(self.items)
                self.items_to_store.remove(slot.hold)
                slot.hold.pos.center = slot.pos.center

    def update(self, screen: pg.surface.Surface, player: TowerdePlayer):

        screen.blit(self.image, self.pos)

        # STORE INVENTORY
        for slot in self.store_inventory.values():

            if slot.hold:

                screen.blit(slot.image, slot.pos)
                screen.blit(slot.hold.image, slot.hold.pos)

            else:

                screen.blit(slot.image, slot.pos)
        # PLAYER INVENTORY
        for slot in self.player_store_inventory.values():

            if slot.hold:

                screen.blit(slot.image, slot.pos)
                screen.blit(slot.hold.image, slot.hold.pos)

            else:

                screen.blit(slot.image, slot.pos)

        gold_text = self.font.render(f"gold: {str(int(player.gold))}", True, "red")
        text_pos = gold_text.get_rect(center=(575, 110))

        screen.blit(gold_text, text_pos)

    def purchase_item(self, item, player: TowerdePlayer):

        for slot in self.store_inventory.values():

            if slot.hold == item and player.gold >= item.cost:

                slot.hold = None
                print("purchased")

                for slot in self.player_store_inventory.values():

                    if not slot.hold:

                        slot.hold = item
                        item.kill()
                        item.add(player.inventory_items)
                        item.pos.center = slot.pos.center
                        player.gold -= item.cost
                        player.items_names.append(item.name)
                        break

    def purchase_reset(self, player: TowerdePlayer):

        if player.gold < 10:
            return False

        player.gold -= 10
        self.build_store()

    def sell_item(self, item, player: TowerdePlayer):

        for slot in self.player_store_inventory.values():

            if slot.hold == item:

                item.kill()
                item.add(self.items)
                self.items_to_store.append(item)
                player.gold += item.cost * 0.75
                slot.hold = None
                break

        for slot in self.store_inventory.values():

            if not slot.hold and len(self.items_to_store) > 0:
                slot.hold = choice(self.items_to_store)
                self.items_to_store.remove(slot.hold)
                slot.hold.pos.center = slot.pos.center

    def load_items(self, player: TowerdePlayer):

        for item in player.inventory_items.sprites():

            for slot in self.player_store_inventory.values():
                if not slot.hold:
                    slot.hold = item
                    slot.hold.pos.center = slot.pos.center
                    break



class TowerdeMenu(pg.sprite.Sprite):

    def __init__(self, screen: pg.surface.Surface):
        pg.sprite.Sprite.__init__(self)

        # STORE BACKGROUND
        self.background_image = pg.image.load("menu_stuff/menu_backg.png").convert(screen)
        self.background = self.background_image.get_rect()
        self.background.x, self.background.y = 0, 0
        # LOAD
        self.load_button_image = pg.image.load("menu_stuff/load_save.png").convert(screen)
        self.load_button = self.load_button_image.get_rect()
        # NEW GAME
        self.new_button_image = pg.image.load("menu_stuff/new_game.png").convert(screen)
        self.new_button = self.new_button_image.get_rect()
        # QUIT
        self.quit_button_image = pg.image.load("menu_stuff/quit.png").convert(screen)
        self.quit_button = self.quit_button_image.get_rect()
        # CONTINUE
        self.continue_button_image = pg.image.load("menu_stuff/continue.png").convert(screen)
        self.continue_button = self.quit_button_image.get_rect()
        # SAVE
        self.save_button_image = pg.image.load("menu_stuff/save.png").convert(screen)
        self.save_button = self.quit_button_image.get_rect()
        # STORE
        self.store_button_image = pg.image.load("menu_stuff/store.png").convert(screen)
        self.store_button = self.store_button_image.get_rect()
        # STAGE SELLECTON
        self.stage_select_button_image = pg.image.load("menu_stuff/stage.png").convert(screen)
        self.stage_select_button = self.stage_select_button_image.get_rect()
        self.stage_button_image = pg.image.load("menu_stuff/stage_button.png").convert(screen)
        self.stage_button = self.stage_button_image.get_rect()
        self.locked_image = pg.image.load("menu_stuff/locked.png").convert(screen)
        # NEW PLAYER INPUT
        self.input_button_image = pg.image.load("menu_stuff/input.png").convert(screen)
        self.input_button = self.input_button_image.get_rect()
        self.input_button.center = (self.background.centerx, self.background.centery)
        self.input_rect = pg.rect.Rect(0, 0, 321, 51)
        self.input_rect.center = self.input_button.center
        self.base_font = pg.font.SysFont('comicsans', 32)
        self.user_text = ""
        self.inputting = False

        self.load_button.center = (self.background.centerx, self.background.centery)
        self.new_button.center = (self.background.centerx, self.background.centery*0.5)
        self.quit_button.center = (self.background.centerx, self.background.centery*1.5)
        self.continue_button.center = (self.background.centerx, self.background.centery)
        self.store_button.center = (self.save_button.centerx + 400, self.save_button.centery)
        self.stage_select_button.center = (self.background.centerx, self.background.centery*0.5)

        self.base_font = pg.font.SysFont("Arial", 36)
        self.save_rects = {}
        self.texts = []
        self.make_stage_numbers()

    def update(self, screen: pg.surface.Surface):

        screen.blit(self.background_image, self.background)
        screen.blit(self.load_button_image, self.load_button)
        screen.blit(self.new_button_image, self.new_button)
        screen.blit(self.quit_button_image, self.quit_button)

    # GAME IS GOING ON
    def continue_update(self, screen: pg.surface.Surface):

        screen.blit(self.background_image, self.background)
        screen.blit(self.continue_button_image, self.continue_button)
        screen.blit(self.save_button_image, self.save_button)
        screen.blit(self.stage_select_button_image, self.stage_select_button)
        screen.blit(self.quit_button_image, self.quit_button)
        screen.blit(self.store_button_image, self.store_button)

    def newgame_update(self, screen: pg.surface.Surface):

        screen.blit(self.background_image, self.background)
        screen.blit(self.input_button_image, self.input_button)
        pg.draw.rect(screen, (119, 73, 49), self.input_rect)
        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+5))

    def toggle_input(self):

        # used for toggle of the input box while clicked on
        self.inputting = not self.inputting

    """
    creates text and rect from a save file from towerde_save folder
    """
    def create_load(self):
        # all saves in the folder
        save_files = list(os.listdir("towerde_save"))

        for index, file in enumerate(save_files):
            font = pg.font.SysFont('comicsans', 25)
            txt = file
            text = font.render(txt, True, "red")
            text_pos = text.get_rect(center=(self.background.centerx, self.background.y + 50 + index * 50))
            self.save_rects[f"{txt}"] = (text, text_pos)
    """
    updates the loading menu with texts being blotted behind each other
    takes value from the text rect being created in the create load function
    """
    def load_menu_update(self, screen: pg.surface.Surface):

        # a and b refer to text, text_rect objects

        screen.blit(self.background_image, self.background)
        for value in self.save_rects.values():
            text, text_rect = value
            pg.draw.rect(screen, "black", ((text_rect.x-8, text_rect.y-8), (text_rect.w+16, text_rect.h+16)), width=5)
            screen.blit(text, text_rect)

    def make_stage_numbers(self):
        x = 0
        for i in range(5):
            for j in range(5):
                x += 1

                text = self.base_font.render(str(x), True, "red")
                text_pos = text.get_rect()
                text_pos.center = ((j/3) * self.background.centerx + 1.5*self.stage_button.width,
                                                      (i/3) * self.background.centery + 1.5*self.stage_button.height)
                self.texts.append([text, text_pos, str(x)])

    def stage_selection_update(self, screen: pg.surface.Surface, player: TowerdePlayer):

        screen.blit(self.background_image, self.background)
        x = 0

        for i in range(5):
            for j in range(5):
                x += 1
                screen.blit(self.stage_button_image, ((j/3) * self.background.centerx + self.stage_button.width,
                                                      (i/3) * self.background.centery + self.stage_button.height))
                if x > player.unlocked_level:
                    screen.blit(self.locked_image, ((j / 3) * self.background.centerx + self.stage_button.width,
                                                          (i / 3) * self.background.centery + self.stage_button.height))

        for text in self.texts:
            a, b = text[:2]
            screen.blit(a, b)


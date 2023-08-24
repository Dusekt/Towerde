import pygame as pg
from map import TowerdeMap
from menu import TowerdeMenu, TowerdeStore
from towerde_player import TowerdePlayer
import sys
from copy import deepcopy


# init pygame
pg.init()
# SCREEN CONSTRUCTOR
size = 600 + 200, 480 + 200
screen = pg.display.set_mode(size, pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
fake_screen = screen.copy()
pg.display.set_caption('TOWERDE')

# MENU CONSTRUCTOR, STORE
menu = TowerdeMenu(fake_screen)
store = TowerdeStore(fake_screen)
store.build_store()
# STAGE CONTROL VARIABLES
in_menu = True
in_store = False
in_stage_selection = False
in_game = False
is_player = None
x = 0

stager = None
loading = False

clock = pg.time.Clock()

while True:

    while in_menu:

        # PLAYER CHOOSES BETWEEN NEWGAME, LOAD ETC..
        # OR CAN CHOOSE STORE
        if not in_game and not is_player and not loading:

            menu.update(fake_screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused():

                    # NEW GAME, player true for control
                    if menu.new_button.collidepoint(pg.mouse.get_pos()):
                        is_player = True

                    # LOAD a game
                    if menu.load_button.collidepoint(pg.mouse.get_pos()):

                        # create directory with info about loading files
                        menu.create_load()
                        # loading control variable
                        loading = True

                    if menu.quit_button.collidepoint(pg.mouse.get_pos()):
                        sys.exit()

        # player is LOADING from a file
        elif loading:

            menu.load_menu_update(fake_screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused():

                    # dict in menu class containing info about the save files, created earlier with menu.create_load()
                    for text, font in menu.save_rects.items():

                        if font[1].collidepoint(pg.mouse.get_pos()):

                            # player chooses a file, then file is loaded
                            is_player = TowerdePlayer(name=menu.user_text)
                            is_player.load(text)
                            # create map, entities etc
                            mp = TowerdeMap(fake_screen, is_player)
                            mp.current_stage = None
                            store.load_items(is_player)
                            # close the menu
                            menu.inputting = False
                            in_game = True
                            in_menu = True
                            loading = False

        # PLAYER CHOSE NEW GAME
        elif not in_game and is_player:

            menu.newgame_update(fake_screen)
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused():

                    # player clicked the bar to write inside
                    if menu.input_button.collidepoint(pg.mouse.get_pos()):
                        menu.toggle_input()
                if event.type == pg.KEYDOWN and menu.inputting:

                    # with enter submit the name, player profile with the name is created (than can be saved)
                    if event.key == pg.K_RETURN and len(menu.user_text) > 0:

                        is_player = TowerdePlayer(name=menu.user_text)
                        # create map, entities etc
                        mp = TowerdeMap(fake_screen, is_player)
                        # close the menu
                        menu.inputting = False
                        in_game = False
                        in_menu = False
                        # INTO THE STAGE SELECTION, ONLY 1st stage will be available
                        in_stage_selection = True

                    elif event.key == pg.K_BACKSPACE and len(menu.user_text) < 21:

                        # get text input from 0 to -1 i.e. end.
                        menu.user_text = menu.user_text[:-1]

                    # Unicode standard is used for string
                    # formation
                    elif len(menu.user_text) < 21:
                        menu.user_text += event.unicode

        # GAME IS GOING ON
        elif in_game and in_menu:
            menu.continue_update(fake_screen)

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused():

                    if menu.stage_select_button.collidepoint(pg.mouse.get_pos()):

                        # NOT GAME TO ENTER THE STAGE SELECTION, CLOSE THE MENU
                        in_stage_selection = True
                        in_game = False
                        in_menu = False

                    if menu.continue_button.collidepoint(pg.mouse.get_pos()) and mp.current_stage:
                        in_menu = False

                    if menu.save_button.collidepoint(pg.mouse.get_pos()) and in_game:

                        # saves the info about the player in a dict with JSON, player class required as arg in map class
                        mp.player.save()
                        print("saved")
                        sys.exit()

                    if menu.store_button.collidepoint(pg.mouse.get_pos()):
                        in_store = True
                        in_menu = False

                    if menu.quit_button.collidepoint(pg.mouse.get_pos()):
                        sys.exit()

        clock.tick(100)
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
        pg.display.flip()

    # NOT IN MENU, IN STORE, CAN GO BACK INTO MENU (but main menu)

    while in_store and is_player:

        store.update(fake_screen, is_player)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused():

                # TOGGLE STORE MENU
                if store.back_rect.collidepoint(pg.mouse.get_pos()):
                    in_store = False
                    in_menu = True
                # REFRESH THE STORE
                if store.refresh_rect.collidepoint(pg.mouse.get_pos()):
                    store.purchase_reset(is_player)
                # PURCHASE AN ITEM, ITERATION THROUGH ALL ITEMS IN STORE
                for item in store.items.sprites():

                    if item.pos.collidepoint(pg.mouse.get_pos()):

                        store.purchase_item(item=item, player=is_player)
                # SELL AN ITEM
                for item in is_player.inventory_items.sprites():

                    if item.pos.collidepoint(pg.mouse.get_pos()):

                        store.sell_item(item=item, player=is_player)

        clock.tick(100)
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
        pg.display.flip()

    # ACTUAL GAME GOING ON NOT IN MENU
    while in_stage_selection and not in_game:

        menu.stage_selection_update(fake_screen, is_player)

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused():

                    for stage in menu.texts:

                        if stage[1].collidepoint(pg.mouse.get_pos()) and int(stage[2]) <= is_player.unlocked_level:

                            # MAP TAKES INT ARG
                            del mp
                            mp = TowerdeMap(fake_screen, is_player)
                            stager = None
                            mp.current_stage = int(stage[2])
                            # create level and stage of map
                            mp.current_level = 0
                            mp.next_level()
                            mp.roll_skills()
                            in_stage_selection = False
                            in_menu = False
                            in_game = True

                            for item in is_player.inventory_items.sprites():
                                item.bullet_pos = deepcopy(mp.tower.pos)
                                item.bullet_pos.x = deepcopy(mp.tower.pos.center[0])
                                item.bullet_pos.y = deepcopy(mp.tower.pos.center[1])
                                mp.equip(item)

        clock.tick(100)
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
        pg.display.flip()

    # GAMEEEE ONNNN
    while not in_menu and not in_stage_selection and not in_store and in_game:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    in_menu = True
                if event.key == pg.K_i:
                    mp.gold_enemies()
            if event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode(event.size, pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
                fake_screen = screen.copy()
                mp.rescale(fake_screen)

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused():
                for weapon in mp.weapons_eu:
                    if weapon.pos.collidepoint(pg.mouse.get_pos()) and mp.inventory.pos.colliderect(weapon.pos):
                        mp.un_equip(weapon)
                        mp.inventory.update(fake_screen)
                for weapon in mp.weapons_un:
                    if weapon.drop_pos.collidepoint(pg.mouse.get_pos()):
                        mp.equip(weapon)
                        mp.inventory.update(fake_screen)

                for skill in mp.skills.sprites():
                    if skill.pos.collidepoint(pg.mouse.get_pos()) and mp.tower.skill_points > skill.cost:
                        skill.level_up()
                        if skill not in mp.allocated_skills.sprites():
                            mp.allocate_skill(skill)
                        mp.roll_skills()
                        break

            for skill in mp.allocated_skills.sprites():
                skill.do_effect()

            if len(mp.enemy.sprites()) == 0 and not stager:
                x += clock.get_time()
                if x > 3000:
                    stager = mp.next_level()
                    x = 0
                if stager:
                    in_menu = True
                    is_player.unlocked_level += 1
                    is_player.gold += mp.tower.gold
                    print("You Won !")

            if mp.tower.xp >= mp.tower.xp_to_level:
                mp.tower.level_up()

        # MAP UPDATES
        mp.update(fake_screen)

        # TOWER ATTACK (different weapons, different attacks)
        mp.tower_attack(clock.get_time())
        mp.update_bullets(fake_screen)

        # ENTITY MOVEMENT
        mp.entity_move(fake_screen)

        if mp.tower.hp <= 0:
            print("You Died")
            in_menu = True
            in_game = False
            is_player = False

        clock.tick(60)
        # UPDATE POSITION EVERY ITERATION (UPDATE POS IN MAIN MODULE)
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
        pg.display.flip()

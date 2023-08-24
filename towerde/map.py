import random
from groups_towerde import Enemy, WeaponsEquipped, WeaponsUnequipped, BulletGroup, Skills, OtherItems, AllocatedSkills
from map_entities import *
from towerde_skills import *
from towerde_player import TowerdePlayer
from towerde_items import *
from Hud import *
from menu import TowerdeStore


class TowerdeMap(pg.sprite.Sprite):
    tower: Tower

    def __init__(self, screen: pg.surface.Surface, player: TowerdePlayer, theme="summer"):
        pg.sprite.Sprite.__init__(self)

        self.player = player
        self.screen = screen
        self.width = screen.get_size()[0] - 200
        self.height = screen.get_size()[1] - 200
        self.pos = pg.rect.Rect(50, 50, self.width - 100, self.height - 100)

        self.tower = Tower(image=pg.image.load("tower.png").convert(screen), height=10, speed=[0, 0])
        self.tower.pos.center = self.width // 2, self.height // 2

        self.inventory = Inventory(self.screen)
        self.inventory.image.convert(screen)

        self.hud = Hud(self.screen)
        self.hud.image.convert(screen)

        self.current_level = 0
        self.current_stage = 1

        self.stages = {
            1:
            {
                1: ["Boss_1"] + ["Goblin"] * 30,
                2: ["Goblin"] * 30,
                3: ["Goblin"] * 30,
                4: ["Goblin"] * 30,
                5: ["Goblin"] * 30,
                6: ["Goblin"] * 30,
                7: ["Goblin"] * 30,
                8: ["Goblin"] * 30,
                9: ["Goblin"] * 30,
                10: ["Goblin"] * 30
            },
            2:
            {
                1: ["Goblin"] * 3,
                2: ["Goblin"] * 30,
                3: ["Goblin"] * 30,
                4: ["Goblin"] * 30,
                5: ["Goblin"] * 30,
                6: ["Goblin"] * 30,
                7: ["Goblin"] * 30,
                8: ["Goblin"] * 30,
                9: ["Goblin"] * 30,
                10: ["Goblin"] * 30
            },
            3:
                {
                    1: ["Goblin"] * 1,
                    2: ["Goblin"] * 30,
                    3: ["Goblin"] * 30,
                    4: ["Goblin"] * 30,
                    5: ["Goblin"] * 30,
                    6: ["Goblin"] * 30,
                    7: ["Goblin"] * 30,
                    8: ["Goblin"] * 30,
                    9: ["Goblin"] * 30,
                    10: ["Goblin"] * 30
                },
            4:
                {
                    1: ["Goblin"] * 30,
                    2: ["Goblin"] * 30,
                    3: ["Goblin"] * 30,
                    4: ["Goblin"] * 30,
                    5: ["Goblin"] * 30,
                    6: ["Goblin"] * 30,
                    7: ["Goblin"] * 30,
                    8: ["Goblin"] * 30,
                    9: ["Goblin"] * 30,
                    10: ["Goblin"] * 30
                },
            5:
                {
                    1: ["Goblin"] * 30,
                    2: ["Goblin"] * 30,
                    3: ["Goblin"] * 30,
                    4: ["Goblin"] * 30,
                    5: ["Goblin"] * 30,
                    6: ["Goblin"] * 30,
                    7: ["Goblin"] * 30,
                    8: ["Goblin"] * 30,
                    9: ["Goblin"] * 30,
                    10: ["Goblin"] * 30
                },

        }

        self.entities = []
        self.time = 0
        self.map_edge = list(map(lambda x: [0, x], range(self.width + 200))) + \
                        list(map(lambda x: [x, 0], range(self.height + 200))) + \
                        list(map(lambda x: [x, self.height + 200], range(self.width + 200))) + \
                        list(map(lambda x: [self.width + 200, x], range(self.height + 200)))

        if theme == "summer":
            self.image = pg.image.load("summer.png").convert(screen)

        # ENEMY GROUP
        self.enemy = Enemy()

        # WEAPON GROUP
        self.weapons_eu = WeaponsEquipped()
        self.weapons_un = WeaponsUnequipped()
        # ITEM GROUP
        self.other_items = OtherItems()

        # BULLET GROUP (BULLETS CREATED BY WEAPONS)
        self.active_bullets = BulletGroup()

        # SKILLS GROUP
        self.skills = Skills()
        self.allocated_skills = AllocatedSkills()
        self.existing_skills = {"skill_1": SkinOfSteel(self.tower),
                                "skill_2": Greed(self.tower,  enemies = list(self.enemy.sprites())),
                                "skill_3": Eclipse(tower=self.tower,inventory=self.inventory),
                                "skill_4": Enlightenment(self.tower),
                                "skill_5": Efficiency(self.tower),
                                "skill_6": Surge(tower=self.tower,inventory=self.inventory),
                                "skill_7": Bash(self.tower)
                                }
        self.starting_skills = {}
        self.create_skill_dict()

        for skill in self.starting_skills.values():
            skill.image.convert(self.screen)
        ########### starting setup ################

        cannon1: Cannon = Cannon(self.tower.pos, attack_speed = 600)
        self.weapons_un.add(cannon1)
        self.equip(cannon1)

        # STATS
        self.stats = Stats(self.tower, self.weapons_eu)

    def next_level(self):

        self.current_level += 1

        # ERASE BEFORE CREATED SPRITES AND SHIT
        self.entities.clear()
        self.weapons_un.empty()
        self.enemy.empty()

        if len(self.stages[self.current_stage]) < self.current_level:
            return True

        for entity in self.stages[self.current_stage][self.current_level]:
            if entity == "Goblin":
                self.entities.append(Goblin(image=pg.image.load("goblin_trans.png").convert_alpha(self.screen),
                                            height=1,
                                            speed=[1, 1],
                                            map_width=self.width,
                                            map_height=self.height,
                                            level=self.current_level,
                                            tower_pos=self.tower.pos))
            if entity == "Boss_1":
                self.entities.append(Boss1(tower=self.tower, screen=self.screen))

        for ent in self.entities:
            if ent.drop:
                ent.drop.image.convert(self.screen)
                ent.drop.bullet_image.convert(self.screen)
                ent.drop.drop_image.convert(self.screen)
            randompos = random.choice(self.map_edge)
            ent.pos.x, ent.pos.y = randompos
            self.enemy.add(ent)

        # GREED
        if "skill_2" in self.starting_skills.keys():
            self.starting_skills["skill_2"].effect = True
            self.starting_skills["skill_2"].enemies = list(self.enemy.sprites())
            self.starting_skills["skill_2"].do_effect()
        self.entities.clear()

        return False

    def tower_attack(self, time_scale):

        for weapon in self.weapons_eu:

            if len(self.enemy.sprites()) > 0:
                enemy = random.choice(self.enemy.sprites())
                # attack speed === attack delay
                if weapon.range > (abs(enemy.pos.x - self.tower.pos.x) + abs(enemy.pos.y - self.tower.pos.y)) \
                        and weapon.time > weapon.attack_speed:
                    if hasattr(weapon, "min_range"):
                        if weapon.min_range > (abs(enemy.pos.x - self.tower.pos.x) + abs(enemy.pos.y - self.tower.pos.y)):
                            continue
                        else:
                            self.active_bullets.add(weapon.create_bullet(enemy, self.enemy))
                    else:
                        self.active_bullets.add(weapon.create_bullet(enemy, self.enemy))
                    weapon.time = 0

                else:
                    weapon.time += time_scale

    def update_bullets(self, screen_rect):

        for bullet in self.active_bullets:
            if bullet.bullet_pos.colliderect(self.pos):
                try:
                    bullet.update(screen_rect)
                except ValueError:
                    bullet.kill()
            else:
                bullet.kill()

    def update(self, screen):

        screen.blit(self.image, (0, 0))
        screen.blit(self.tower.image, self.tower.pos)
        for weapon in self.weapons_un.sprites():
            screen.blit(weapon.drop_image, weapon.drop_pos)

        # EFFICIENCY

        if "skill_5" in self.starting_skills.keys():
            if self.starting_skills["skill_5"].level == self.starting_skills["skill_5"].control_level:

                self.starting_skills["skill_5"].effect = True
                self.starting_skills["skill_5"].do_effect(list(self.starting_skills.values()))
                self.starting_skills["skill_5"].control_level += 1

        self.inventory.update(screen)
        self.hud.update(screen)
        self.stats.update(screen)


    def entity_move(self, screen):

        for o in self.enemy.sprites():

            if "skill_7" in self.starting_skills.keys():
                if self.starting_skills["skill_7"].chance >= random.random():

                    if hasattr(o, "attack"):
                        o.update(screen)
                    else:
                        o.move()
                    if self.tower.pos.colliderect(o.pos):
                        self.tower.hp -= o.damage

            if self.pos.colliderect(o.pos):
                screen.blit(o.image, o.pos)
                if hasattr(o, "bullets"):
                    for bullet in o.bullets.sprites():
                        bullet.update(screen)

            if o.hp < 0:

                if not self.tower.enlightenment:
                    self.tower.xp += o.xp
                elif isinstance(self.tower.enlightenment, float):
                    self.tower.xp += o.xp*self.tower.enlightenment

                if random.random() < o.drop_chance and o.drop:
                    a, b = o.drop.drop(o)
                    screen.blit(a, b)
                    o.drop.add(self.weapons_un)

                self.tower.gold += o.bounty

                o.kill()

    def equip(self, weapon: WeaponsUnequipped):

        for slot, item in self.inventory.inventory.items():

            try:
                if item.status == "Empty":
                    item.status = weapon
                    if hasattr(weapon, "damage"):
                        weapon.add(self.weapons_eu)
                    else:
                        weapon.add(self.other_items)
                    weapon.remove(self.weapons_un)
                    return True

            except AttributeError:
                continue

        print("i am no beast of Burden")
        return False

    def un_equip(self, weapon: WeaponsEquipped):

        for slot, item in self.inventory.inventory.items():

            try:
                if item.status == weapon:
                    item.status = "Empty"
                    weapon.add(self.weapons_un)
                    weapon.remove(self.weapons_eu)
                    break

            except AttributeError:
                continue

    def create_skill_dict(self):

        self.player.update()
        for name, skill in self.existing_skills.items():

            if name in self.player.unlocked_skills:
                self.starting_skills[name] = skill

    def roll_skills(self):
        self.skills.empty()
        choices = []

        for slot in self.hud.hud.values():
            slot.status = "Empty"

        for skill in self.starting_skills.values():
            if skill.level < skill.max_level:
                choices.append(skill)

        for slot in self.hud.hud.values():

            if len(choices) > 0:
                skill = random.choice(choices)
                if skill not in self.skills.sprites():
                    slot.status = skill
                    skill.add(self.skills)
                    choices.remove(skill)
            else:
                break

    def allocate_skill(self, skill):

        skill.add(self.allocated_skills)

    def gold_enemies(self):

        golders = []
        for i in range(15):

            enemy = Goblin(image=pg.image.load("goblin_trans.png").convert_alpha(self.screen),
                                            height=1,
                                            speed=[1, 1],
                                            map_width=self.width,
                                            map_height=self.height,
                                            level=self.current_level,
                                            tower_pos=self.tower.pos)
            enemy.bounty = 50
            enemy.xp = 0
            enemy.drop = None

            golders.append(enemy)

        for ent in golders:

            randompos = random.choice(self.map_edge)
            ent.pos.x, ent.pos.y = randompos
            self.enemy.add(ent)

    def rescale(self, new_screen: pg.surface.Surface):

        self.screen = new_screen

        self.width, self.height = new_screen.get_size()
        self.pos = pg.rect.Rect(50, 50, 600*self.width/800 - 100, 480*self.height/680 - 100)

        self.tower.pos.center = 600*self.width/800 // 2, 480*self.height/680 // 2
        a, b = self.image.get_size()
        self.image = pg.image.load("summer.png")
        self.image = pg.transform.scale(self.image, (a*self.width/800,b*self.height/680))

        self.inventory.rescale(new_screen)
        self.stats.rescale(new_screen)
        self.hud.rescale(new_screen)

    def equip_store_items(self, store: TowerdeStore):

        for item in store.items.sprites():

            item.tower_pos = self.tower.pos
            self.equip(item)



import json
from groups_towerde import PlayerItems
from towerde_items import *

"""
create profile of player, variable of stage unlocked ect...

SKILLS ARE UNLOCKED IN THE MAP CLASS AS THIS 

        self.starting_skills = {"skill_1": SkinOfSteel(self.tower),
                                "skill_2": Greed(self.tower,  enemies = list(self.enemy.sprites())),
                                "skill_3": Eclipse(tower=self.tower,inventory=self.inventory),
                                "skill_4": Enlightenment(self.tower),
                                "skill_5": Efficiency(self.tower),
                                "skill_6": Surge(tower=self.tower,inventory=self.inventory),
                                "skill_7": Bash(self.tower)
                                }

"""


class TowerdePlayer:

    def __init__(self, name="DefaultPlayer", load=False, load_file=None):

        self.name = name
        self.unlocked_skills_numbers = [1, 2, 3, 4, 5, 6, 7]
        self.unlocked_skills = []
        self.unlocked_level = 1
        self.saved = 0
        self.gold = 0
        self.items_names = []
        self.inventory_items = PlayerItems()

        if load and load_file:
            self.load(load_file)
            self.update()

    def update(self):

        self.unlocked_skills = list(map(lambda x: f"skill_{x}", self.unlocked_skills_numbers))

    def save(self, new=True):

        if new:

            self.saved += 1
            save_dict = {
                "name": self.name,
                "unlocked_skills_numbers": self.unlocked_skills_numbers,
                "unlocked_level": self.unlocked_level,
                "saved": self.saved,
                "gold": self.gold,
                "item_names": self.items_names
            }

            with open(f"towerde_save/{self.name}_{self.saved}", "w") as f:

                json.dump(save_dict, f)

        elif not new:

            save_dict = {
                "name": self.name,
                "unlocked_skills_numbers": self.unlocked_skills_numbers,
                "unlocked_level": self.unlocked_level,
                "saved": self.saved,
                "gold": self.gold,
                "item_names": self.items_names
            }

            with open(f"towerde_save/{self.name}_{self.saved}", "w") as f:

                json.dump(save_dict, f)

    def load(self, file):

        with open(f"towerde_save/{file}", "r") as f:

            data = json.load(f)

        try:
            self.name = data["name"]
            self.unlocked_skills_numbers = data["unlocked_skills_numbers"]
            self.unlocked_level = data["unlocked_level"]
            self.saved = data["saved"]
            self.gold = data["gold"]
            self.items_names = data["item_names"]
        except IndexError:
            print("data not loaded properly")

        for item in self.items_names:
            klass = globals()[item]
            item_new = klass()
            self.inventory_items.add(item_new)








import pygame as pg


class Enemy(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)


class BulletGroup(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)


class WeaponsEquipped(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)


class WeaponsUnequipped(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)


class Skills(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)


class AllocatedSkills(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)


class OtherItems(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)


class Texts(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)


class StoreItems(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)

class PlayerItems(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)

class BossBullets(pg.sprite.Group):

    def __init__(self):
        pg.sprite.Group.__init__(self)



from MovingEntity import MovingEntity
import pygame as pg
import random

class Food(MovingEntity):
    _game_width = 0
    _game_height = 0
    def __init__(self,width, height):
        super().__init__() 
        self._game_width = width
        self._game_height = height
        self._x = random.randrange(0,  self._game_width, MovingEntity.CELL_SIZE)
        self._y = random.randrange(0, self._game_height, MovingEntity.CELL_SIZE)
    # ############### CODE IA (Claude) ###############
    # Rendu ameliore de la pomme (cercle rouge, tige, feuille, reflet).
    def draw(self, screen):
        cell = MovingEntity.CELL_SIZE
        cx = self._x + cell // 2
        cy = self._y + cell // 2
        r = cell // 2 - 2
        # tige + feuille
        pg.draw.line(screen, (110, 70, 30), (cx, cy - r), (cx, cy - r - 3), 2)
        pg.draw.circle(screen, (60, 180, 75), (cx + 3, cy - r - 1), 3)
        # corps de la pomme + reflet
        pg.draw.circle(screen, (225, 55, 60), (cx, cy), r)
        pg.draw.circle(screen, (255, 150, 150), (cx - r // 3, cy - r // 3), max(2, r // 4))
    # ################################################
    def get_position(self):
        return self._x, self._y
    def respawn(self):
        self._x = random.randrange(0, self._game_width , MovingEntity.CELL_SIZE)
        self._y = random.randrange(0, self._game_height , MovingEntity.CELL_SIZE)
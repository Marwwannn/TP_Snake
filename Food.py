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
    def draw(self, screen):
        pg.draw.rect(screen, "green", (self._x, self._y, MovingEntity.CELL_SIZE, MovingEntity.CELL_SIZE))
    def get_position(self):
        return self._x, self._y
    def respawn(self):
        self._x = random.randrange(0, self._game_width , MovingEntity.CELL_SIZE)
        self._y = random.randrange(0, self._game_height , MovingEntity.CELL_SIZE)
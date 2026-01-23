from MovingEntity import MovingEntity
import pygame as pg

class Snake( MovingEntity ):
    def __init__( self , x , y):
        super().__init__ ()
        self._body = [(x , y) ]
        self._grow_pending = 0
    def update(self, game):
        posx, posy = MovingEntity.get_direction(self)
        new_posx = posx + self._body[0][0]
        new_posy = posy + self._body[0][1]
        if new_posx < 0 or new_posx >= game.get_width() or new_posy < 0 or new_posy >= game.get_height():
            if game.get_game_over() == False:
                game.set_game_over(True)
                return
            else: 
                return
        if (new_posx, new_posy) in self._body:
            if game.get_game_over() == False:
                game.set_game_over(True)
                return
            else: 
                return
        self._body.insert(0, (new_posx, new_posy))
        if self._grow_pending > 0:
            self._grow_pending -= 1
        else:
            self._body.pop()
    def draw(self, screen):
        for i in range (len(self._body)):
            pg.draw.rect( screen, "red", (self._body[i][0],self._body[i][1],MovingEntity.CELL_SIZE,MovingEntity.CELL_SIZE))   
    def grow(self,n):
        self._grow_pending += n

    def get_body(self):
        return self._body
    def get_grow_pending(self):
        return self._grow_pending
    def head_pos(self):
        return self._body[0]        
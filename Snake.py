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
    # ############### CODE IA (Claude) ###############
    # Rendu ameliore du serpent (degrade, coins arrondis, yeux).
    def draw(self, screen):
        cell = MovingEntity.CELL_SIZE
        n = len(self._body)
        for i, (x, y) in enumerate(self._body):
            if i == 0:
                color = (120, 230, 130)  # tete : vert clair
            else:
                # degrade du vert vers une teinte plus sombre vers la queue
                t = i / (n - 1) if n > 1 else 0
                color = (40, int(200 - 110 * t), 90)
            pg.draw.rect(screen, color, (x + 1, y + 1, cell - 2, cell - 2), border_radius=6)
        self._draw_eyes(screen)

    def _draw_eyes(self, screen):
        cell = MovingEntity.CELL_SIZE
        hx, hy = self._body[0]
        cx, cy = hx + cell // 2, hy + cell // 2
        off = cell // 4
        if self._dx != 0:  # deplacement horizontal
            ex = cx + (off if self._dx > 0 else -off)
            eyes = [(ex, cy - off), (ex, cy + off)]
        else:              # deplacement vertical
            ey = cy + (off if self._dy > 0 else -off)
            eyes = [(cx - off, ey), (cx + off, ey)]
        for ex, ey in eyes:
            pg.draw.circle(screen, "white", (ex, ey), 3)
            pg.draw.circle(screen, "black", (ex, ey), 1)
    # ################################################
    def grow(self,n):
        self._grow_pending += n

    def get_body(self):
        return self._body
    def get_grow_pending(self):
        return self._grow_pending
    def head_pos(self):
        return self._body[0]        
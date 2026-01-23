from Entity import Entity

class MovingEntity(Entity) :
    CELL_SIZE = 20
    DEFAULT_SPEED = 10
    def __init__ (self) :
        self._dx = self.CELL_SIZE
        self._dy = 0

    def set_cell_size(self, value):
        if value > 0:
            MovingEntity.CELL_SIZE = value
        else:
            raise ValueError("supp a 0 pour la cellule")

    def set_default_speed(self, value):
        if value > 0:
            MovingEntity.DEFAULT_SPEED = value
        else:
            raise ValueError("supp a 0 pour la vitesse")
    def set_direction(self, dx, dy):
        if dx == 0 and dy == 0:
            raise ValueError("dx et dy ne peuvent pas etre 0")
        else:
            self._dx = dx
            self._dy = dy

    def get_cell_size(self):
        return self.CELL_SIZE

    def get_default_speed(self):
        return self.DEFAULT_SPEED

    def get_direction(self):        
        return self._dx, self._dy

# =============================================================================
# Food.py
# -----------------------------------------------------------------------------
# HERITE de : MovingEntity (classe Food(MovingEntity)) -> donc aussi d'Entity.
#
# POURQUOI cette classe existe :
#   Represente la POMME que le serpent doit manger. Elle herite de
#   MovingEntity surtout pour reutiliser la grille (CELL_SIZE) et rester
#   alignee sur les cases comme le serpent. La pomme ne bouge pas vraiment :
#   quand elle est mangee, elle "reapparait" (respawn) a une case aleatoire.
# =============================================================================

from MovingEntity import MovingEntity            # Import de la classe mere (pour heriter de la grille/direction)
import pygame as pg                              # pygame pour le dessin ; renomme 'pg' pour aller plus vite
import random                                    # Module aleatoire pour placer la pomme au hasard

class Food(MovingEntity):                        # Food herite de MovingEntity
    _game_width = 0                              # Largeur du terrain (valeur par defaut, ecrasee dans __init__)
    _game_height = 0                             # Hauteur du terrain (valeur par defaut, ecrasee dans __init__)
    def __init__(self,width, height):           # Constructeur : recoit la taille du terrain de jeu
        super().__init__()                      # Appelle le constructeur de MovingEntity (initialise la direction)
        self._game_width = width                # Memorise la largeur du terrain pour cette pomme
        self._game_height = height              # Memorise la hauteur du terrain pour cette pomme
        self._x = random.randrange(0,  self._game_width, MovingEntity.CELL_SIZE)   # Position X alignee sur la grille, au hasard
        self._y = random.randrange(0, self._game_height, MovingEntity.CELL_SIZE)   # Position Y alignee sur la grille, au hasard
    # ############### CODE IA (Claude) ###############
    # Rendu ameliore de la pomme (cercle rouge, tige, feuille, reflet).
    def draw(self, screen):                     # Redefinit draw() (heritee d'Entity) pour dessiner la pomme
        cell = MovingEntity.CELL_SIZE           # Raccourci local vers la taille d'une cellule
        cx = self._x + cell // 2                # Coordonnee X du CENTRE de la cellule
        cy = self._y + cell // 2                # Coordonnee Y du CENTRE de la cellule
        r = cell // 2 - 2                       # Rayon de la pomme (un peu plus petit que la cellule)
        # tige + feuille
        pg.draw.line(screen, (110, 70, 30), (cx, cy - r), (cx, cy - r - 3), 2)     # Petite tige marron au-dessus
        pg.draw.circle(screen, (60, 180, 75), (cx + 3, cy - r - 1), 3)             # Petite feuille verte a cote de la tige
        # corps de la pomme + reflet
        pg.draw.circle(screen, (225, 55, 60), (cx, cy), r)                         # Corps rouge de la pomme
        pg.draw.circle(screen, (255, 150, 150), (cx - r // 3, cy - r // 3), max(2, r // 4))  # Reflet clair (effet brillant)
    # ################################################
    def get_position(self):                     # Getter : renvoie la position de la pomme
        return self._x, self._y                 # Retourne un tuple (x, y)
    def respawn(self):                          # Fait reapparaitre la pomme ailleurs (apres avoir ete mangee)
        self._x = random.randrange(0, self._game_width , MovingEntity.CELL_SIZE)   # Nouvelle position X aleatoire sur la grille
        self._y = random.randrange(0, self._game_height , MovingEntity.CELL_SIZE)  # Nouvelle position Y aleatoire sur la grille

# =============================================================================
# Snake.py
# -----------------------------------------------------------------------------
# HERITE de : MovingEntity (classe Snake(MovingEntity)) -> donc aussi d'Entity.
#
# POURQUOI cette classe existe :
#   Represente le SERPENT controle par le joueur (ou l'IA). Il herite de
#   MovingEntity pour la direction et la grille. Le serpent est une liste de
#   segments (_body) : a chaque update il avance d'une case (ajoute une tete,
#   retire la queue), grandit quand il mange, et meurt s'il touche un mur ou
#   son propre corps.
# =============================================================================

from MovingEntity import MovingEntity            # Import de la classe mere (direction + grille)
import pygame as pg                              # pygame pour le dessin

class Snake( MovingEntity ):                     # Snake herite de MovingEntity
    def __init__( self , x , y):                # Constructeur : position de depart (x, y) de la tete
        super().__init__ ()                     # Appelle le constructeur de MovingEntity (direction initiale)
        self._body = [(x , y) ]                 # Corps du serpent = liste de cases ; au depart une seule (la tete)
        self._grow_pending = 0                  # Nombre de segments a ajouter (en attente de croissance)
    def update(self, game):                     # Redefinit update() : fait avancer le serpent d'une case
        posx, posy = MovingEntity.get_direction(self)   # Recupere la direction courante (dx, dy)
        new_posx = posx + self._body[0][0]      # Nouvelle X de la tete = direction + X actuelle de la tete
        new_posy = posy + self._body[0][1]      # Nouvelle Y de la tete = direction + Y actuelle de la tete
        if new_posx < 0 or new_posx >= game.get_width() or new_posy < 0 or new_posy >= game.get_height():  # Sortie du terrain ?
            if game.get_game_over() == False:   # Si la partie n'est pas deja terminee...
                game.set_game_over(True)        # ...on declenche le Game Over
                return                          # On sort sans deplacer le serpent
            else:                               # Si la partie etait deja finie...
                return                          # ...on ne fait rien
        if (new_posx, new_posy) in self._body:  # La tete va-t-elle entrer dans son propre corps ?
            if game.get_game_over() == False:   # Si la partie n'est pas deja terminee...
                game.set_game_over(True)        # ...Game Over (le serpent s'est mordu)
                return                          # On sort
            else:                               # Sinon...
                return                          # ...rien a faire
        self._body.insert(0, (new_posx, new_posy))  # Pas de collision : on ajoute la nouvelle tete en debut de liste
        if self._grow_pending > 0:              # S'il reste de la croissance a faire...
            self._grow_pending -= 1             # ...on consomme une unite de croissance (et on NE retire PAS la queue)
        else:                                   # Sinon (pas de croissance)...
            self._body.pop()                    # ...on retire le dernier segment -> le serpent "avance" sans grandir
    # ############### CODE IA (Claude) ###############
    # Rendu ameliore du serpent (degrade, coins arrondis, yeux).
    def draw(self, screen):                     # Redefinit draw() : dessine tout le corps du serpent
        cell = MovingEntity.CELL_SIZE           # Raccourci vers la taille d'une cellule
        n = len(self._body)                     # Nombre de segments (longueur du serpent)
        for i, (x, y) in enumerate(self._body): # Parcourt chaque segment avec son indice i
            if i == 0:                          # Le premier segment est la tete
                color = (120, 230, 130)  # tete : vert clair                       # Couleur claire pour la tete
            else:                               # Pour les segments du corps...
                # degrade du vert vers une teinte plus sombre vers la queue
                t = i / (n - 1) if n > 1 else 0 # Position relative dans le corps (0 = tete, 1 = queue)
                color = (40, int(200 - 110 * t), 90)  # Vert de plus en plus sombre vers la queue
            pg.draw.rect(screen, color, (x + 1, y + 1, cell - 2, cell - 2), border_radius=6)  # Dessine le segment (coins arrondis)
        self._draw_eyes(screen)                 # Ajoute les yeux sur la tete

    def _draw_eyes(self, screen):               # Methode "privee" (prefixe _) : dessine les yeux du serpent
        cell = MovingEntity.CELL_SIZE           # Taille d'une cellule
        hx, hy = self._body[0]                  # Coordonnees de la tete
        cx, cy = hx + cell // 2, hy + cell // 2 # Centre de la tete
        off = cell // 4                         # Decalage des yeux par rapport au centre
        if self._dx != 0:  # deplacement horizontal                                # Si le serpent va a gauche/droite...
            ex = cx + (off if self._dx > 0 else -off)   # ...les yeux sont vers l'avant (cote du deplacement)
            eyes = [(ex, cy - off), (ex, cy + off)]     # Deux yeux empiles verticalement
        else:              # deplacement vertical                                  # Sinon (haut/bas)...
            ey = cy + (off if self._dy > 0 else -off)   # ...yeux vers l'avant (haut ou bas)
            eyes = [(cx - off, ey), (cx + off, ey)]     # Deux yeux cote a cote horizontalement
        for ex, ey in eyes:                     # Pour chacun des deux yeux...
            pg.draw.circle(screen, "white", (ex, ey), 3)  # Blanc de l'oeil
            pg.draw.circle(screen, "black", (ex, ey), 1)  # Pupille noire
    # ################################################
    def grow(self,n):                           # Fait grandir le serpent de n segments
        self._grow_pending += n                 # On ajoute n a la croissance en attente (appliquee aux prochains update)

    def get_body(self):                         # Getter : renvoie le corps complet
        return self._body                       # Liste des segments (x, y)
    def get_grow_pending(self):                 # Getter : renvoie la croissance restante
        return self._grow_pending               # Nombre de segments encore a ajouter
    def head_pos(self):                         # Getter pratique : position de la tete
        return self._body[0]                    # Premier element de la liste = tete

# =============================================================================
# MovingEntity.py
# -----------------------------------------------------------------------------
# HERITE de : Entity (classe MovingEntity(Entity))
#
# POURQUOI cette classe existe :
#   C'est une entite qui, en plus d'exister (Entity), peut SE DEPLACER.
#   Elle factorise tout ce qui est commun aux objets mobiles du jeu :
#       - une direction de deplacement (dx, dy)
#       - la taille d'une cellule de la grille (CELL_SIZE)
#       - la vitesse du jeu (DEFAULT_SPEED)
#   Le Snake ET la Food en heritent : ils partagent ainsi la meme grille
#   et le meme systeme de direction, sans dupliquer le code.
#
#   CELL_SIZE et DEFAULT_SPEED sont des ATTRIBUTS DE CLASSE (partages par
#   toutes les instances) : changer la taille/vitesse impacte tout le jeu.
# =============================================================================

from Entity import Entity                       # Import de la classe mere Entity (pour en heriter)

class MovingEntity(Entity) :                     # MovingEntity herite d'Entity -> recupere update()/draw()
    CELL_SIZE = 20                               # Attribut de CLASSE : taille d'une case de la grille (en pixels)
    DEFAULT_SPEED = 10                           # Attribut de CLASSE : vitesse du jeu (frames par seconde)
    def __init__ (self) :                        # Constructeur : appele a la creation de l'objet
        self._dx = self.CELL_SIZE                # Direction horizontale initiale : avance d'une case vers la droite
        self._dy = 0                             # Direction verticale initiale : aucun deplacement vertical

    def set_cell_size(self, value):              # Setter : modifie la taille des cellules
        if value > 0:                            # On verifie que la valeur est strictement positive
            MovingEntity.CELL_SIZE = value       # Mise a jour de l'attribut de CLASSE (impacte toutes les entites)
        else:                                    # Sinon (valeur <= 0)...
            raise ValueError("supp a 0 pour la cellule")  # ...on leve une erreur : taille invalide

    def set_default_speed(self, value):          # Setter : modifie la vitesse du jeu
        if value > 0:                            # La vitesse doit etre strictement positive
            MovingEntity.DEFAULT_SPEED = value   # Mise a jour de l'attribut de CLASSE
        else:                                    # Sinon (valeur <= 0)...
            raise ValueError("supp a 0 pour la vitesse")  # ...erreur : vitesse invalide
    def set_direction(self, dx, dy):             # Setter : change la direction de deplacement
        if dx == 0 and dy == 0:                  # Direction (0,0) = immobile -> interdit dans Snake
            raise ValueError("dx et dy ne peuvent pas etre 0")  # On refuse une direction nulle
        else:                                    # Sinon, direction valide...
            self._dx = dx                        # On enregistre la composante horizontale
            self._dy = dy                        # On enregistre la composante verticale

    def get_cell_size(self):                     # Getter : renvoie la taille d'une cellule
        return self.CELL_SIZE                    # Retourne l'attribut CELL_SIZE

    def get_default_speed(self):                 # Getter : renvoie la vitesse du jeu
        return self.DEFAULT_SPEED                # Retourne l'attribut DEFAULT_SPEED

    def get_direction(self):                     # Getter : renvoie la direction courante
        return self._dx, self._dy                # Retourne un tuple (dx, dy)

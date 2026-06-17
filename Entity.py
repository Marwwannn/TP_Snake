# =============================================================================
# Entity.py
# -----------------------------------------------------------------------------
# Classe de BASE (mere/abstraite) de toutes les entites du jeu.
# Elle n'herite de rien (classe racine de la hierarchie).
#
# POURQUOI cette classe existe :
#   Elle definit le "contrat" commun a toutes les choses affichees a l'ecran
#   (serpent, pomme, ...). Chaque entite doit savoir :
#       - se mettre a jour    -> update()
#       - se dessiner         -> draw()
#   Le jeu peut ainsi traiter toutes les entites de la meme facon
#   (boucle "for e in entities: e.update() / e.draw()") sans connaitre
#   leur type exact -> c'est le principe du POLYMORPHISME.
#
#   Ici les methodes sont vides (pass) : ce sont des "trous" que les
#   classes filles (MovingEntity, Snake, Food) viennent remplir.
# =============================================================================

class Entity :                       # Definition de la classe racine Entity
    def update ( self , game ) :     # Methode appelee a chaque frame pour faire evoluer l'entite ; 'game' = reference au jeu
        pass                         # Comportement par defaut : rien (les filles le redefiniront)
    def draw ( self , screen ) :     # Methode appelee a chaque frame pour dessiner l'entite ; 'screen' = surface d'affichage
        pass                         # Comportement par defaut : rien (les filles le redefiniront)

# ############### CODE IA (Claude) ###############
# Fichier entierement genere avec l'IA (agent / environnement DQN).
# -----------------------------------------------------------------------------
# N'HERITE de rien. POURQUOI cette classe existe :
#   GameAI est une version "modifiee" de Game.py concue pour ENTRAINER une IA.
#   Au lieu d'une boucle continue pilotee par le clavier, elle expose le jeu
#   comme un "environnement" controlable pas a pas :
#       reset()              -> recommence une partie
#       play_step(action)    -> joue UNE action et renvoie (reward, done, score)
#       get_state()          -> decrit la situation en 11 chiffres pour le reseau
#   Elle reutilise les MEMES classes Snake et Food que le jeu humain.
# -----------------------------------------------------------------------------
import os                                       # Pour construire des chemins de fichiers
import sys                                       # Pour modifier le chemin de recherche des modules
# Les classes du jeu de base (Snake, Food, MovingEntity) sont restees a la
# RACINE du projet. Comme ce fichier est dans IA/, on ajoute le dossier parent
# au chemin de recherche pour pouvoir les importer.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame                                   # Pour l'affichage optionnel pendant l'entrainement
import numpy as np                              # Pour manipuler les vecteurs d'etat/action (tableaux)
from Snake import Snake                         # Reutilise le serpent du jeu de base (a la racine)
from Food import Food                           # Reutilise la pomme du jeu de base (a la racine)
from MovingEntity import MovingEntity           # Pour acceder a CELL_SIZE (taille de la grille)


class GameAI:                                   # Environnement de jeu pour l'IA (ne herite de rien)
    """
    Version step-by-step du jeu Snake pour entrainer une IA (DQN).

    Differences avec Game.py :
      - reset()                 : reinitialise une partie
      - play_step(action)       : execute UNE action et renvoie (reward, done, score)
      - get_state()             : renvoie un vecteur 11 features pour le reseau
      - render=False par defaut : pas d'affichage = entrainement rapide

    Encodage des actions (vecteur 3 valeurs) :
      [1,0,0] = tout droit
      [0,1,0] = tourner a droite
      [0,0,1] = tourner a gauche
    """

    REWARD_FOOD = 10                            # Recompense quand l'IA mange une pomme
    REWARD_DEATH = -10                          # Punition quand l'IA meurt
    REWARD_STEP = 0                             # Recompense neutre pour un simple pas

    def __init__(self, width=600, height=600, render=False, speed=40):  # Constructeur ; render=affichage on/off
        self.width = width                      # Largeur du terrain
        self.height = height                    # Hauteur du terrain
        self.render = render                    # Affiche-t-on le jeu ? (False = entrainement rapide)
        self.speed = speed                      # Vitesse d'affichage (FPS) si render=True

        if self.render:                         # Si on veut voir le jeu...
            pygame.init()                       # ...on initialise pygame
            self.screen = pygame.display.set_mode((self.width, self.height))  # ...on cree la fenetre
            pygame.display.set_caption("Snake AI")           # ...on titre la fenetre
            self.clock = pygame.time.Clock()    # ...horloge pour limiter les FPS
            self.font = pygame.font.Font(None, 36)           # ...police pour afficher le score

        self.reset()                            # Prepare une premiere partie

    def reset(self):                            # Reinitialise une partie (debut ou apres une mort)
        self.snake = Snake(self.width // 2, self.height // 2)  # Nouveau serpent au centre
        self.food = Food(self.width, self.height)             # Nouvelle pomme
        self._respawn_food_safely()             # Replace la pomme pour qu'elle ne soit pas sur le serpent
        self.score = 0                          # Score remis a zero
        self.frame_iteration = 0                # Compteur de pas (sert a detecter les parties qui tournent en rond)
        self.game_over = False                  # Drapeau de fin de partie

    def play_step(self, action):                # Joue UNE action et fait avancer le jeu d'un pas
        self.frame_iteration += 1               # Incremente le compteur de pas

        if self.render:                         # Si l'affichage est actif...
            for event in pygame.event.get():    # ...on lit les evenements pygame
                if event.type == pygame.QUIT:   # ...si on ferme la fenetre...
                    pygame.quit()               # ...on quitte pygame
                    quit()                      # ...et on arrete le programme

        self._apply_action(action)              # Convertit l'action (droit/droite/gauche) en direction
        self._move_snake()                      # Fait avancer le serpent (peut declencher game_over)

        reward = self.REWARD_STEP               # Recompense par defaut (neutre)
        done = False                            # Par defaut, la partie continue

        if self.game_over or self.frame_iteration > 100 * len(self.snake.get_body()):  # Mort OU trop de pas sans manger ?
            done = True                         # La partie est terminee
            reward = self.REWARD_DEATH          # On applique la punition de mort
            return reward, done, self.score     # On renvoie le resultat de ce pas

        if self.snake.head_pos() == self.food.get_position():  # La tete est-elle sur la pomme ?
            self.score += 1                     # Score +1
            reward = self.REWARD_FOOD           # Recompense de pomme
            self.snake.grow(1)                  # Le serpent grandit
            self._respawn_food_safely()         # Nouvelle pomme (pas sur le corps)

        if self.render:                         # Si l'affichage est actif...
            self._update_ui()                   # ...on redessine la scene
            self.clock.tick(self.speed)         # ...on limite la vitesse a 'speed' FPS

        return reward, done, self.score         # Renvoie (recompense, fin?, score) au programme d'entrainement

    def get_state(self):                        # Construit le "regard" de l'IA : 11 booleens decrivant la situation
        head = self.snake.head_pos()            # Position de la tete
        cell = MovingEntity.CELL_SIZE           # Taille d'une cellule
        dx, dy = self.snake.get_direction()     # Direction courante du serpent

        point_l = (head[0] - cell, head[1])     # Case juste a GAUCHE de la tete
        point_r = (head[0] + cell, head[1])     # Case juste a DROITE de la tete
        point_u = (head[0], head[1] - cell)     # Case juste AU-DESSUS de la tete
        point_d = (head[0], head[1] + cell)     # Case juste EN-DESSOUS de la tete

        dir_l = dx == -cell                     # Le serpent va-t-il a gauche ?
        dir_r = dx == cell                      # ...a droite ?
        dir_u = dy == -cell                     # ...vers le haut ?
        dir_d = dy == cell                      # ...vers le bas ?

        food_x, food_y = self.food.get_position()  # Position de la pomme

        state = [                               # Vecteur d'etat (11 valeurs 0/1)
            (dir_r and self._is_collision(point_r))   # 1) Danger DROIT DEVANT (selon la direction actuelle)
            or (dir_l and self._is_collision(point_l))
            or (dir_u and self._is_collision(point_u))
            or (dir_d and self._is_collision(point_d)),

            (dir_u and self._is_collision(point_r))   # 2) Danger a DROITE du serpent
            or (dir_d and self._is_collision(point_l))
            or (dir_l and self._is_collision(point_u))
            or (dir_r and self._is_collision(point_d)),

            (dir_d and self._is_collision(point_r))   # 3) Danger a GAUCHE du serpent
            or (dir_u and self._is_collision(point_l))
            or (dir_r and self._is_collision(point_u))
            or (dir_l and self._is_collision(point_d)),

            dir_l, dir_r, dir_u, dir_d,         # 4-7) Direction actuelle (gauche, droite, haut, bas)

            food_x < head[0],                   # 8) Pomme a gauche de la tete ?
            food_x > head[0],                   # 9) Pomme a droite ?
            food_y < head[1],                   # 10) Pomme au-dessus ?
            food_y > head[1],                   # 11) Pomme en-dessous ?
        ]
        return np.array(state, dtype=int)       # Renvoie le tout en tableau d'entiers (0/1)

    def _apply_action(self, action):            # Traduit l'action [droit/droite/gauche] en nouvelle direction
        cell = MovingEntity.CELL_SIZE           # Taille d'une cellule
        clock_wise = [(cell, 0), (0, cell), (-cell, 0), (0, -cell)]  # Directions dans le sens horaire : D, B, G, H
        dx, dy = self.snake.get_direction()     # Direction actuelle
        idx = clock_wise.index((dx, dy))        # Indice de la direction actuelle dans la liste

        if np.array_equal(action, [1, 0, 0]):   # Action "tout droit"...
            new_dir = clock_wise[idx]           # ...on garde la meme direction
        elif np.array_equal(action, [0, 1, 0]): # Action "tourner a droite"...
            new_dir = clock_wise[(idx + 1) % 4] # ...on prend la direction suivante dans le sens horaire
        else:                                   # Action "tourner a gauche" ([0,0,1])...
            new_dir = clock_wise[(idx - 1) % 4] # ...on prend la direction precedente (sens anti-horaire)

        self.snake.set_direction(*new_dir)      # Applique la nouvelle direction au serpent

    def _move_snake(self):                      # Avance le serpent d'une case
        self.snake.update(self)                 # Appelle l'update du Snake (gere collisions/croissance)

    def _is_collision(self, point):             # Teste si une case 'point' provoque une collision
        if (point[0] < 0 or point[0] >= self.width  # Hors du terrain horizontalement ?
                or point[1] < 0 or point[1] >= self.height):  # ...ou verticalement ?
            return True                         # -> collision avec un mur
        if point in self.snake.get_body():      # La case fait-elle partie du corps du serpent ?
            return True                         # -> collision avec soi-meme
        return False                            # Sinon, pas de collision

    def _respawn_food_safely(self):             # Replace la pomme en evitant qu'elle tombe sur le serpent
        for _ in range(100):                    # On reessaie au maximum 100 fois
            self.food.respawn()                 # Nouvelle position aleatoire
            if self.food.get_position() not in self.snake.get_body():  # Si elle n'est pas sur le corps...
                return                          # ...c'est bon, on garde cette position

    def _update_ui(self):                       # Dessine la scene (uniquement si render=True)
        self.screen.fill((18, 18, 28))          # Fond sombre
        cell = MovingEntity.CELL_SIZE           # Taille d'une cellule
        for x in range(0, self.width, cell):    # Lignes verticales de la grille
            pygame.draw.line(self.screen, (30, 30, 45), (x, 0), (x, self.height))
        for y in range(0, self.height, cell):   # Lignes horizontales de la grille
            pygame.draw.line(self.screen, (30, 30, 45), (0, y), (self.width, y))
        for e in (self.food, self.snake):       # On dessine la pomme puis le serpent
            e.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, "white")  # Texte du score
        self.screen.blit(score_text, (10, 10)) # Affiche le score en haut a gauche
        pygame.display.flip()                   # Rafraichit l'ecran

    def get_width(self):                        # Getter : largeur (utilise par Snake.update pour les murs)
        return self.width

    def get_height(self):                       # Getter : hauteur
        return self.height

    def get_game_over(self):                    # Getter : etat de fin de partie
        return self.game_over

    def set_game_over(self, value):             # Setter : permet a Snake de signaler la mort
        self.game_over = value
# ##################################################

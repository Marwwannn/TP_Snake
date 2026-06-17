# =============================================================================
# Game.py
# -----------------------------------------------------------------------------
# N'HERITE de rien : c'est la classe "chef d'orchestre" du jeu.
#
# POURQUOI cette classe existe :
#   C'est le POINT D'ENTREE du jeu jouable par un humain. Elle ne represente
#   pas une entite affichable, mais elle GERE tout le reste :
#       - la fenetre pygame et la boucle principale (run)
#       - les entrees clavier (handle_events)
#       - la mise a jour des entites et le score (update)
#       - l'affichage (draw)
#   Elle contient un Snake et une Food (composition), et les traite via une
#   liste commune 'entities' grace au polymorphisme (Entity.update/draw).
# =============================================================================

import pygame                                   # Bibliotheque de jeu (fenetre, evenements, dessin)
from Snake import Snake                         # Import du serpent
from Food import Food                           # Import de la pomme

class Game:                                     # Classe principale du jeu (ne herite de rien)
    def __init__(self):                         # Constructeur : prepare une nouvelle partie
        pygame.init()                           # Initialise tous les modules de pygame
        self.width = 600                        # Largeur de la fenetre/terrain (pixels)
        self.height = 600                       # Hauteur de la fenetre/terrain (pixels)
        self.running = True                     # Drapeau : la boucle principale tourne tant que True
        self.screen = pygame.display.set_mode((self.width, self.height))  # Cree la fenetre d'affichage
        self.clock = pygame.time.Clock()        # Horloge pour limiter le nombre d'images par seconde
        self.game_over = False                  # Drapeau : True quand la partie est perdue
        self.score = 0                          # Score du joueur (nombre de pommes mangees)
        self.food = Food(self.width, self.height)        # Cree la pomme en lui donnant la taille du terrain
        self.snake = Snake(self.width//2, self.height//2)  # Cree le serpent au centre du terrain
        self.entities = [self.food, self.snake] # Liste des entites a mettre a jour/dessiner (polymorphisme)
    def handle_events(self):                    # Gere les evenements (clavier, fermeture de fenetre)
        for event in pygame.event.get():        # Parcourt tous les evenements en attente
            if event.type == pygame.QUIT:       # Clic sur la croix de fermeture ?
                self.game_over = True           # On marque la partie comme finie
                self.running = False            # Et on arrete la boucle principale
            if event.type == pygame.KEYDOWN:    # Une touche vient d'etre pressee ?
                if self.game_over and event.key == pygame.K_r:  # Si on est en Game Over et qu'on appuie sur R...
                    self.restart()              # ...on relance une partie
                    return                      # Et on sort (inutile de traiter les directions)
                dx, dy = self.snake.get_direction()  # Direction actuelle du serpent (pour empecher le demi-tour)
                if event.key == pygame.K_LEFT and dx != (self.snake.CELL_SIZE):     # Fleche gauche (si on n'allait pas a droite)
                    self.snake.set_direction(-self.snake.CELL_SIZE, 0)             # Nouvelle direction : vers la gauche
                if event.key == pygame.K_RIGHT and dx != (-self.snake.CELL_SIZE):   # Fleche droite (si on n'allait pas a gauche)
                    self.snake.set_direction(self.snake.CELL_SIZE, 0)              # Nouvelle direction : vers la droite
                if event.key == pygame.K_UP and dy != (self.snake.CELL_SIZE):       # Fleche haut (si on n'allait pas en bas)
                    self.snake.set_direction(0,-self.snake.CELL_SIZE)              # Nouvelle direction : vers le haut
                if event.key == pygame.K_DOWN and dy != (-self.snake.CELL_SIZE):    # Fleche bas (si on n'allait pas en haut)
                    self.snake.set_direction(0,self.snake.CELL_SIZE)               # Nouvelle direction : vers le bas


    def update(self):                           # Met a jour la logique du jeu (une frame)
        for e in self.entities:                 # Pour chaque entite (pomme, serpent)...
            e.update(self)                      # ...on appelle son update() (polymorphisme)
        if(self.snake.head_pos() == self.food.get_position()):  # La tete du serpent est-elle sur la pomme ?
            self.food.respawn()                 # Oui : la pomme reapparait ailleurs
            self.snake.grow(1)                  # Le serpent grandit d'un segment
            self.score += 1                     # Et le score augmente de 1

    def draw(self):                             # Dessine toute la scene a l'ecran
        # ############### CODE IA (Claude) ###############
        # Fond sombre + grille (visuel ameliore).
        self.screen.fill((18, 18, 28))          # Remplit le fond avec une couleur sombre
        cell = self.snake.CELL_SIZE             # Taille d'une cellule (pour tracer la grille)
        for x in range(0, self.width, cell):    # Pour chaque colonne de la grille...
            pygame.draw.line(self.screen, (30, 30, 45), (x, 0), (x, self.height))  # ...trace une ligne verticale
        for y in range(0, self.height, cell):   # Pour chaque ligne de la grille...
            pygame.draw.line(self.screen, (30, 30, 45), (0, y), (self.width, y))   # ...trace une ligne horizontale
        # ################################################
        for e in self.entities:                 # Pour chaque entite...
            e.draw(self.screen)                 # ...on la dessine (polymorphisme : pomme puis serpent)

        # ############### CODE IA (ChatGPT) ###############
        # Affichage du score et de l'ecran Game Over.
        # Utiliser GPT pour m'afficher le score
        font = pygame.font.Font(None, 36)       # Police par defaut, taille 36, pour le score
        score_text = font.render(f"Score: {self.score}", True, "white")  # Cree l'image texte du score
        self.screen.blit(score_text, (10, 10))  # Affiche le score en haut a gauche

        if self.game_over:                      # Si la partie est perdue...
            font_big = pygame.font.Font(None, 72)            # Grande police pour "GAME OVER"
            game_over_text = font_big.render("GAME OVER", True, "red")  # Texte rouge "GAME OVER"
            # Utiliser GPT pour centrer le texte
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))  # Rectangle centre a l'ecran
            self.screen.blit(game_over_text, text_rect)      # Affiche "GAME OVER" centre
            # Utiliser GPT pour afficher le texte de rejouer
            font_small = pygame.font.Font(None, 36)          # Petite police pour le message de relance
            restart_text = font_small.render("Appuie sur R pour rejouer", True, "white")  # Texte d'aide
            text_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))  # Centre, un peu plus bas
            self.screen.blit(restart_text, text_rect)        # Affiche le message de relance
        # ##################################################
        pygame.display.flip()                   # Met a jour l'ecran avec tout ce qui vient d'etre dessine

    def run(self):                              # Boucle principale du jeu
        nb=0                                    # Compteur d'etapes de vitesse deja appliquees (paliers)
        while self.running:                     # Tant que le jeu tourne...
            self.handle_events()                # On lit les entrees clavier/fenetre
            if self.game_over == False:         # Si la partie n'est pas finie...
                self.update()                   # ...on met a jour la logique du jeu
            if self.score == 10 and nb == 0:    # Au palier de 10 points (premiere fois)...
                self.snake.set_default_speed(self.snake.DEFAULT_SPEED + 10)  # ...on accelere le jeu de +10
                nb +=1                          # On passe au palier suivant
            if self.score == 20 and nb == 1:    # Au palier de 20 points (premiere fois)...
                self.snake.set_default_speed(self.snake.DEFAULT_SPEED + 30)  # ...on accelere encore (+30)
                nb +=1                          # Palier suivant
            self.draw()                         # On dessine la scene
            self.clock.tick(Snake.DEFAULT_SPEED)  # On limite la vitesse a DEFAULT_SPEED images/seconde
    def get_width(self):                        # Getter : largeur du terrain (utilise par Snake pour les collisions)
        return self.width                       # Retourne la largeur
    def get_height(self):                       # Getter : hauteur du terrain
        return self.height                      # Retourne la hauteur
    def get_game_over(self):                    # Getter : etat de fin de partie
        return self.game_over                   # Retourne True/False
    def set_game_over(self, value):             # Setter : permet a Snake de declencher le Game Over
        self.game_over = value                  # Met a jour le drapeau
    def restart(self):                          # Reinitialise une partie (apres Game Over)
        self.game_over = False                  # On enleve l'etat Game Over
        self.score = 0                          # On remet le score a zero
        self.snake = Snake(self.width // 2, self.height // 2)  # Nouveau serpent au centre
        self.food = Food(self.width, self.height)             # Nouvelle pomme
        self.entities = [self.food, self.snake]               # On reconstruit la liste des entites

if __name__ == "__main__":                      # Si ce fichier est lance directement (et non importe)...
    game = Game()                               # ...on cree une partie
    game.run()                                  # On lance la boucle de jeu
    pygame.quit()                               # A la fin, on ferme proprement pygame

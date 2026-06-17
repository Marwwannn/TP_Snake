# ############### CODE IA (Claude) ###############
# Fichier entierement genere avec l'IA (visualisation de l'agent qui joue).
# -----------------------------------------------------------------------------
# Ce fichier n'est PAS une classe : c'est un SCRIPT de demonstration.
# POURQUOI il existe :
#   Il CHARGE un reseau deja entraine (model/model.pth) et regarde l'IA jouer
#   toute seule, avec l'affichage active et SANS coup aleatoire (epsilon = 0).
#   C'est l'inverse de train.py : ici on ne fait qu'exploiter, pas apprendre.
# -----------------------------------------------------------------------------
"""
Lance le jeu : une IA entrainee (DQN) joue toute seule au Snake.

Usage :
  python play.py
  python play.py --speed 20
"""

import argparse                                 # Pour lire l'option --speed

import pygame                                   # Pour gerer l'affichage et les evenements fenetre

from GameAI import GameAI                       # L'environnement de jeu
from SnakeAI import Agent                       # Le joueur IA


def show_game_over(game, score, record):        # Affiche un ecran "Game Over" semi-transparent
    """Affiche un overlay Game Over par-dessus la derniere image de la partie."""
    overlay = pygame.Surface((game.width, game.height))  # Cree une surface de la taille de l'ecran
    overlay.set_alpha(180)                      # La rend semi-transparente (0=invisible, 255=opaque)
    overlay.fill("black")                       # La remplit de noir
    game.screen.blit(overlay, (0, 0))          # La pose par-dessus le jeu (effet assombri)

    font_big = pygame.font.Font(None, 72)       # Grande police pour "GAME OVER"
    font_small = pygame.font.Font(None, 36)     # Petite police pour les infos

    go = font_big.render("GAME OVER", True, "red")  # Texte rouge "GAME OVER"
    game.screen.blit(go, go.get_rect(center=(game.width // 2, game.height // 2 - 40)))  # Centre, un peu au-dessus

    sc = font_small.render(f"Score : {score}   |   Record : {record}", True, "white")  # Texte score + record
    game.screen.blit(sc, sc.get_rect(center=(game.width // 2, game.height // 2 + 20)))  # Centre, un peu en dessous

    info = font_small.render("Nouvelle partie...", True, "white")  # Message d'attente
    game.screen.blit(info, info.get_rect(center=(game.width // 2, game.height // 2 + 60)))  # Encore en dessous

    pygame.display.flip()                       # Affiche tout a l'ecran


def play(speed=40):                             # Fonction principale : fait jouer l'IA
    agent = Agent()                             # Cree l'agent (reseau neuf)
    if not agent.model.load():                  # Tente de charger le reseau entraine...
        print("Aucun modele trouve dans model/model.pth. Lance d'abord train.py.")  # Si echec : message
        return                                  # ...et on arrete (rien a montrer)

    # Mode exploitation pur : l'IA suit son reseau, aucun coup aleatoire.
    agent.eps_start = 0                          # Epsilon = 0 -> jamais d'action aleatoire

    game = GameAI(render=True, speed=speed)     # Environnement AVEC affichage
    record = 0                                  # Meilleur score de la session

    while True:                                 # Boucle infinie (ferme la fenetre pour quitter)
        state = game.get_state()                # Lit l'etat actuel
        action = agent.get_action(state)        # L'IA choisit la meilleure action
        _, done, score = game.play_step(action) # Joue l'action (on ignore la recompense ici)

        if done:                                # Si la partie est terminee...
            record = max(record, score)         # ...met a jour le record
            print(f"Game over. Score : {score} | Record : {record}")  # Affiche le resultat en console
            show_game_over(game, score, record) # Affiche l'ecran de fin

            # Pause de 1.5 s tout en restant reactif a la fermeture de fenetre.
            wait_until = pygame.time.get_ticks() + 1500  # Instant cible : maintenant + 1500 ms
            while pygame.time.get_ticks() < wait_until:  # Tant qu'on n'a pas attendu 1,5 s...
                for event in pygame.event.get():         # ...on lit les evenements
                    if event.type == pygame.QUIT:        # Si on ferme la fenetre...
                        pygame.quit()                    # ...on quitte pygame
                        return                           # ...et on sort de la fonction
                pygame.time.wait(20)                     # Petite pause pour ne pas saturer le CPU

            game.reset()                        # On relance une nouvelle partie


if __name__ == "__main__":                      # Si le script est lance directement...
    parser = argparse.ArgumentParser()          # Prepare le lecteur d'arguments
    parser.add_argument("--speed", type=int, default=40, help="FPS d'affichage")  # Option --speed
    args = parser.parse_args()                  # Lit les arguments
    try:                                        # On lance la demo...
        play(speed=args.speed)                  # ...avec la vitesse choisie
    except KeyboardInterrupt:                   # Si Ctrl+C...
        pygame.quit()                           # ...on ferme pygame proprement
# ##################################################

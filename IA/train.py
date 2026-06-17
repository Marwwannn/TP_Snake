# ############### CODE IA (Claude) ###############
# Fichier entierement genere avec l'IA (boucle d'entrainement DQN).
# -----------------------------------------------------------------------------
# Ce fichier n'est PAS une classe : c'est un SCRIPT d'entrainement.
# POURQUOI il existe :
#   Il fait jouer l'Agent (SnakeAI) dans l'environnement GameAI en boucle
#   infinie, lui fait apprendre apres chaque pas et apres chaque partie, et
#   sauvegarde le meilleur reseau dans model/model.pth.
# -----------------------------------------------------------------------------
"""
Boucle d'entrainement DQN pour Snake.

Usage :
  python train.py              # entrainement headless, plus rapide
  python train.py --render     # affiche le jeu pendant l'entrainement
"""

import argparse                                 # Pour lire les options de la ligne de commande (--render, --speed)
import time                                     # Pour mesurer le temps ecoule

from GameAI import GameAI                       # L'environnement de jeu (pas a pas)
from SnakeAI import Agent                       # Le joueur IA (reseau + memoire)


def train(render=False, speed=200, save_every_record=True):  # Fonction principale d'entrainement
    agent = Agent()                             # Cree l'agent (reseau neuf, memoire vide)
    game = GameAI(render=render, speed=speed)   # Cree l'environnement de jeu

    record = 0                                  # Meilleur score atteint jusqu'ici
    scores = []                                 # Liste de tous les scores (historique)
    total_score = 0                             # Somme des scores (pour la moyenne)
    start = time.time()                         # Heure de depart (pour mesurer la duree)

    while True:                                 # Boucle infinie (Ctrl+C pour arreter)
        state_old = game.get_state()            # Etat AVANT l'action
        action = agent.get_action(state_old)    # L'agent choisit une action

        reward, done, score = game.play_step(action)  # On joue l'action -> recompense, fin?, score
        state_new = game.get_state()            # Etat APRES l'action

        agent.train_short_memory(state_old, action, reward, state_new, done)  # Apprentissage immediat (1 pas)
        agent.remember(state_old, action, reward, state_new, done)            # Memorise la transition

        if done:                                # Si la partie est terminee...
            game.reset()                        # ...on recommence une partie
            agent.n_games += 1                  # ...on compte une partie de plus
            agent.train_long_memory()           # ...on entraine sur un gros lot de souvenirs

            if score > record:                  # Si on a battu le record...
                record = score                  # ...on met a jour le record
                if save_every_record:           # ...et si la sauvegarde auto est activee...
                    agent.model.save()          # ...on sauvegarde le reseau

            scores.append(score)                # Ajoute le score a l'historique
            total_score += score                # Cumule pour la moyenne
            mean = total_score / agent.n_games  # Score moyen depuis le debut
            elapsed = time.time() - start       # Temps total ecoule

            print(                              # Affiche un resume de la partie
                f"Game {agent.n_games:4d} | Score {score:3d} | "
                f"Record {record:3d} | Mean {mean:5.2f} | "
                f"Eps {agent.epsilon:3d} | {elapsed:6.0f}s"
            )


if __name__ == "__main__":                      # Si le script est lance directement...
    parser = argparse.ArgumentParser()          # Prepare le lecteur d'arguments
    parser.add_argument("--render", action="store_true", help="afficher le jeu pendant l'entrainement")  # Option --render
    parser.add_argument("--speed", type=int, default=200, help="FPS si --render")  # Option --speed (vitesse d'affichage)
    args = parser.parse_args()                  # Lit les arguments fournis
    try:                                        # On lance l'entrainement...
        train(render=args.render, speed=args.speed)  # ...avec les options choisies
    except KeyboardInterrupt:                   # Si l'utilisateur fait Ctrl+C...
        print("\nEntrainement interrompu par l'utilisateur.")  # ...message propre d'arret
# ##################################################

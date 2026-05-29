# ############### CODE IA (Claude) ###############
# Fichier entierement genere avec l'IA (boucle d'entrainement DQN).
"""
Boucle d'entrainement DQN pour Snake.

Usage :
  python train.py              # entrainement headless, plus rapide
  python train.py --render     # affiche le jeu pendant l'entrainement
"""

import argparse
import time

from GameAI import GameAI
from SnakeAI import Agent


def train(render=False, speed=200, save_every_record=True):
    agent = Agent()
    game = GameAI(render=render, speed=speed)

    record = 0
    scores = []
    total_score = 0
    start = time.time()

    while True:
        state_old = game.get_state()
        action = agent.get_action(state_old)

        reward, done, score = game.play_step(action)
        state_new = game.get_state()

        agent.train_short_memory(state_old, action, reward, state_new, done)
        agent.remember(state_old, action, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                if save_every_record:
                    agent.model.save()

            scores.append(score)
            total_score += score
            mean = total_score / agent.n_games
            elapsed = time.time() - start

            print(
                f"Game {agent.n_games:4d} | Score {score:3d} | "
                f"Record {record:3d} | Mean {mean:5.2f} | "
                f"Eps {agent.epsilon:3d} | {elapsed:6.0f}s"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true", help="afficher le jeu pendant l'entrainement")
    parser.add_argument("--speed", type=int, default=200, help="FPS si --render")
    args = parser.parse_args()
    try:
        train(render=args.render, speed=args.speed)
    except KeyboardInterrupt:
        print("\nEntrainement interrompu par l'utilisateur.")
# ##################################################

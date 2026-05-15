"""
Joue une partie en affichant le snake controle par le modele entraine.

Usage :
  python play.py
  python play.py --speed 20
"""

import argparse

import pygame

from GameAI import GameAI
from SnakeAI import Agent


def play(speed=20):
    agent = Agent()
    if not agent.model.load():
        print("Aucun modele trouve dans model/model.pth. Lance d'abord train.py.")
        return

    agent.eps_start = 0

    game = GameAI(render=True, speed=speed)

    while True:
        state = game.get_state()
        action = agent.get_action(state)
        _, done, score = game.play_step(action)
        if done:
            print(f"Game over. Score : {score}")
            pygame.time.wait(1500)
            game.reset()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--speed", type=int, default=20, help="FPS d'affichage")
    args = parser.parse_args()
    try:
        play(speed=args.speed)
    except KeyboardInterrupt:
        pygame.quit()

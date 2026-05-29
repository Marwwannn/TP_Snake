# ############### CODE IA (Claude) ###############
# Fichier entierement genere avec l'IA (visualisation de l'agent qui joue).
"""
Lance le jeu : une IA entrainee (DQN) joue toute seule au Snake.

Usage :
  python play.py
  python play.py --speed 20
"""

import argparse

import pygame

from GameAI import GameAI
from SnakeAI import Agent


def show_game_over(game, score, record):
    """Affiche un overlay Game Over par-dessus la derniere image de la partie."""
    overlay = pygame.Surface((game.width, game.height))
    overlay.set_alpha(180)
    overlay.fill("black")
    game.screen.blit(overlay, (0, 0))

    font_big = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    go = font_big.render("GAME OVER", True, "red")
    game.screen.blit(go, go.get_rect(center=(game.width // 2, game.height // 2 - 40)))

    sc = font_small.render(f"Score : {score}   |   Record : {record}", True, "white")
    game.screen.blit(sc, sc.get_rect(center=(game.width // 2, game.height // 2 + 20)))

    info = font_small.render("Nouvelle partie...", True, "white")
    game.screen.blit(info, info.get_rect(center=(game.width // 2, game.height // 2 + 60)))

    pygame.display.flip()


def play(speed=40):
    agent = Agent()
    if not agent.model.load():
        print("Aucun modele trouve dans model/model.pth. Lance d'abord train.py.")
        return

    # Mode exploitation pur : l'IA suit son reseau, aucun coup aleatoire.
    agent.eps_start = 0

    game = GameAI(render=True, speed=speed)
    record = 0

    while True:
        state = game.get_state()
        action = agent.get_action(state)
        _, done, score = game.play_step(action)

        if done:
            record = max(record, score)
            print(f"Game over. Score : {score} | Record : {record}")
            show_game_over(game, score, record)

            # Pause de 1.5 s tout en restant reactif a la fermeture de fenetre.
            wait_until = pygame.time.get_ticks() + 1500
            while pygame.time.get_ticks() < wait_until:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                pygame.time.wait(20)

            game.reset()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--speed", type=int, default=40, help="FPS d'affichage")
    args = parser.parse_args()
    try:
        play(speed=args.speed)
    except KeyboardInterrupt:
        pygame.quit()
# ##################################################

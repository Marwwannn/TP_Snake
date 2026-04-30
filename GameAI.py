import pygame
import numpy as np
from Snake import Snake
from Food import Food
from MovingEntity import MovingEntity


class GameAI:
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

    REWARD_FOOD = 10
    REWARD_DEATH = -10
    REWARD_STEP = 0

    def __init__(self, width=600, height=600, render=False, speed=40):
        self.width = width
        self.height = height
        self.render = render
        self.speed = speed

        if self.render:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Snake AI")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36)

        self.reset()

    def reset(self):
        self.snake = Snake(self.width // 2, self.height // 2)
        self.food = Food(self.width, self.height)
        self._respawn_food_safely()
        self.score = 0
        self.frame_iteration = 0
        self.game_over = False

    def play_step(self, action):
        self.frame_iteration += 1

        if self.render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        self._apply_action(action)
        self._move_snake()

        reward = self.REWARD_STEP
        done = False

        if self.game_over or self.frame_iteration > 100 * len(self.snake.get_body()):
            done = True
            reward = self.REWARD_DEATH
            return reward, done, self.score

        if self.snake.head_pos() == self.food.get_position():
            self.score += 1
            reward = self.REWARD_FOOD
            self.snake.grow(1)
            self._respawn_food_safely()

        if self.render:
            self._update_ui()
            self.clock.tick(self.speed)

        return reward, done, self.score

    def get_state(self):
        head = self.snake.head_pos()
        cell = MovingEntity.CELL_SIZE
        dx, dy = self.snake.get_direction()

        point_l = (head[0] - cell, head[1])
        point_r = (head[0] + cell, head[1])
        point_u = (head[0], head[1] - cell)
        point_d = (head[0], head[1] + cell)

        dir_l = dx == -cell
        dir_r = dx == cell
        dir_u = dy == -cell
        dir_d = dy == cell

        food_x, food_y = self.food.get_position()

        state = [
            (dir_r and self._is_collision(point_r))
            or (dir_l and self._is_collision(point_l))
            or (dir_u and self._is_collision(point_u))
            or (dir_d and self._is_collision(point_d)),

            (dir_u and self._is_collision(point_r))
            or (dir_d and self._is_collision(point_l))
            or (dir_l and self._is_collision(point_u))
            or (dir_r and self._is_collision(point_d)),

            (dir_d and self._is_collision(point_r))
            or (dir_u and self._is_collision(point_l))
            or (dir_r and self._is_collision(point_u))
            or (dir_l and self._is_collision(point_d)),

            dir_l, dir_r, dir_u, dir_d,

            food_x < head[0],
            food_x > head[0],
            food_y < head[1],
            food_y > head[1],
        ]
        return np.array(state, dtype=int)

    def _apply_action(self, action):
        cell = MovingEntity.CELL_SIZE
        clock_wise = [(cell, 0), (0, cell), (-cell, 0), (0, -cell)]
        dx, dy = self.snake.get_direction()
        idx = clock_wise.index((dx, dy))

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx + 1) % 4]
        else:
            new_dir = clock_wise[(idx - 1) % 4]

        self.snake.set_direction(*new_dir)

    def _move_snake(self):
        self.snake.update(self)

    def _is_collision(self, point):
        if (point[0] < 0 or point[0] >= self.width
                or point[1] < 0 or point[1] >= self.height):
            return True
        if point in self.snake.get_body():
            return True
        return False

    def _respawn_food_safely(self):
        for _ in range(100):
            self.food.respawn()
            if self.food.get_position() not in self.snake.get_body():
                return

    def _update_ui(self):
        self.screen.fill("black")
        for e in (self.food, self.snake):
            e.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, "white")
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_game_over(self):
        return self.game_over

    def set_game_over(self, value):
        self.game_over = value

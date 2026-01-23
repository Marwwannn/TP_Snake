import pygame
from Snake import Snake
from Food import Food

class Game:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 600
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.food = Food(self.width, self.height)
        self.snake = Snake(self.width//2, self.height//2)
        self.entities = [self.food, self.snake]
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_r:
                    self.restart()
                    return
                dx, dy = self.snake.get_direction()
                if event.key == pygame.K_LEFT and dx != (self.snake.CELL_SIZE):
                    self.snake.set_direction(-self.snake.CELL_SIZE, 0)
                if event.key == pygame.K_RIGHT and dx != (-self.snake.CELL_SIZE):
                    self.snake.set_direction(self.snake.CELL_SIZE, 0)
                if event.key == pygame.K_UP and dy != (self.snake.CELL_SIZE):
                    self.snake.set_direction(0,-self.snake.CELL_SIZE)
                if event.key == pygame.K_DOWN and dy != (-self.snake.CELL_SIZE):
                    self.snake.set_direction(0,self.snake.CELL_SIZE)


    def update(self):
        for e in self.entities:
            e.update(self)
        if(self.snake.head_pos() == self.food.get_position()):
            self.food.respawn()
            self.snake.grow(1)
            self.score += 1
    
    def draw(self):
        self.screen.fill("black")
        for e in self.entities:
            e.draw(self.screen)

        # Utiliser GPT pour m'afficher le score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, "white")
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            font_big = pygame.font.Font(None, 72)
            game_over_text = font_big.render("GAME OVER", True, "red")
            # Utiliser GPT pour centrer le texte
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, text_rect)
            # Utiliser GPT pour afficher le texte de rejouer
            font_small = pygame.font.Font(None, 36)
            restart_text = font_small.render("Appuie sur R pour rejouer", True, "white")
            text_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(restart_text, text_rect)
        pygame.display.flip()

    def run(self):
        nb=0
        while self.running:
            self.handle_events()
            if self.game_over == False:
                self.update()
            if self.score == 10 and nb == 0:
                self.snake.set_default_speed(self.snake.DEFAULT_SPEED + 10)
                nb +=1
            if self.score == 20 and nb == 1:
                self.snake.set_default_speed(self.snake.DEFAULT_SPEED + 30)
                nb +=1
            self.draw()
            self.clock.tick(Snake.DEFAULT_SPEED)
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_game_over(self):
        return self.game_over
    def set_game_over(self, value):
        self.game_over = value
    def restart(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake(self.width // 2, self.height // 2)
        self.food = Food(self.width, self.height)
        self.entities = [self.food, self.snake]

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit() 
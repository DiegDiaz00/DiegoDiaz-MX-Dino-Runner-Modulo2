from dino_runner.utils.constants import SHIELD_TYPE
import pygame
import random
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from dino_runner.components.obstacles.cactus import SmallCactus
from dino_runner.components.obstacles.cactus import LargeCactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.sound_lose = pygame.mixer.Sound('DiegoDiaz-MX-Dino-Runner-Modulo2/dino_runner/assets/Other/LOSE.mp3')
    
    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                self.obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    self.sound_lose.play()
                    pygame.time.delay(1000)
                    game.death_count += 1
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacles in self.obstacles:
            obstacles.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []

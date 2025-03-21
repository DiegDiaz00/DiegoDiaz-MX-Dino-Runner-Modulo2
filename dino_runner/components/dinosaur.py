import pygame
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, RUNNING_SHIELD, JUMPING_SHIELD, DUCKING_SHIELD, DEFAULT_TYPE, SHIELD_TYPE
from pygame.sprite import Sprite


RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD }
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD }
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD }

class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = 8.5
        self.has_power_up = False
        self.power_time_up = 0
        self.jump_sound = pygame.mixer.Sound('DiegoDiaz-MX-Dino-Runner-Modulo2/dino_runner/assets/Other/JUMP.mp3')

    def update(self, user_input):
        if self.dino_run:
            self.run()

        elif self.dino_duck:
            self.duck()

        elif self.dino_jump:
            self.jump()

        if user_input[pygame.K_UP] and not self.dino_jump or user_input[pygame.K_SPACE] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
            self.jump_sound.play()      

        if user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_jump = False
            self.dino_run = False
            self.dino_duck = True

        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_jump = False
            self.dino_duck = False
            self.dino_run = True 
        
        if self.step_index >= 9:
            self.step_index = 0

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS + 30
        self.step_index += 1


    def jump(self):
        self.image = JUMP_IMG[self.type]
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8
        if self.jump_vel < -8.5:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = 8.5
    

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

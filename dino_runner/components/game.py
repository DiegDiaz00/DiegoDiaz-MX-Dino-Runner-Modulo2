import pygame

from dino_runner.components.cloud import Cloud
from dino_runner.components.obstacles.text_generate import text_draw
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.clouds = Cloud()
        self.running = False
        self.score = 0
        self.death_count = 0
        self.high_score = 0
        self.power_up_manager = PowerUpManager()
        self.sound_power_up = pygame.mixer.Sound('DiegoDiaz-MX-Dino-Runner-Modulo2/dino_runner/assets/Other/POWERUP.mp3')
    
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.score = 0
        self.game_speed = 20
        self.power_up_manager.reset_power_ups()

    def sounds(self):
        pygame.mixer.music.load('DiegoDiaz-MX-Dino-Runner-Modulo2/dino_runner/assets/Other/BACKGROUNDSOUND.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.sounds()
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.clouds.update(self)
        self.update_score()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((93, 176, 254))
        self.draw_background()
        self.draw_score()
        self.draw_power_up_time()
        self.clouds.draw(self.screen)
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        


    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 20)
        text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        text_h = font.render(f'HI: {self.high_score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_h_rect = text_h.get_rect()
        text_h_rect.center = (850, 50)
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)
        self.screen.blit(text_h, text_h_rect)
        
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.sound_power_up.set_volume(0.2)
                self.sound_power_up.play(0)
                text_draw(
                f'{self.player.type.capitalize()} enabled for {time_to_show} seconds',
                self.screen,
                font_size = 18,
                pos_x_center = 500,
                pos_y_center = 50
                )
            else:
                self.sound_power_up.stop()
                self.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0 and self.game_speed < 1000:
                self.game_speed += 3
        
        if self.score > self.high_score:
            self.high_score = self.score


    def handle_events_on_menu(self) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                
                self.run()

    def show_menu(self):
        self.screen.fill((229, 0, 0))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            text_draw('Press any key to restart ', self.screen)
        else:
            pygame.mixer.music.pause()
            text_draw('You lost press to try again', self.screen)
            text_draw (f'Your score: {self. score}', self.screen, pos_y_center = half_screen_height + 50)
            text_draw (f' Your high score: {self.high_score}', self.screen, pos_y_center = half_screen_height + 100)
            text_draw (f' Death count: {self.death_count}', self.screen, pos_y_center = half_screen_height + 150)
        self.screen.blit(ICON,(half_screen_width-50,half_screen_height-150))
        pygame.display.update()
        self.handle_events_on_menu ()
    
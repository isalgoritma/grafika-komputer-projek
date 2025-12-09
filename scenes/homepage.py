import pygame # type: ignore
import os
import math

class Homepage:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        self.background = self.create_background()

        self.clouds = [
            [self.make_cloud(1.0), 60, 70, 0.08],
            [self.make_cloud(0.85), 250, 150, 0.08],
            [self.make_cloud(1.0), self.WIDTH * 0.65, 80, 0.08],
            [self.make_cloud(0.85), self.WIDTH * 0.82, 160, 0.08],
        ]

        fruits = pygame.image.load("assets/images/buah_homepage.png").convert_alpha()
        fruit_height = int(self.HEIGHT * 0.54)  
        fruit_width = int(fruit_height * (1000/350)) 
        self.fruits = pygame.transform.smoothscale(fruits, (fruit_width, fruit_height))
        self.fruit_y = int(self.HEIGHT * 0.46)  

        title_size = int(130 * (self.HEIGHT / 650))
        subtitle_size = int(42 * (self.HEIGHT / 650))
        start_size = int(70 * (self.HEIGHT / 650))
        
        self.title_font = pygame.font.Font("assets/fonts/heyam/Heyam.ttf", title_size)
        self.subtitle_font = pygame.font.Font("assets/fonts/heyam/Heyam.ttf", subtitle_size)
        self.start_font = pygame.font.Font("assets/fonts/heyam/Heyam.ttf", start_size)


        btn_width = int(360 * (self.WIDTH / 1000))
        btn_height = int(140 * (self.HEIGHT / 650))
        
        self.button_panel = pygame.Surface((btn_width, btn_height), pygame.SRCALPHA)
        pygame.draw.rect(self.button_panel, (255, 200, 120), (0, 0, btn_width, btn_height), border_radius=40)
        pygame.draw.rect(self.button_panel, (180, 110, 40), (0, 0, btn_width, btn_height), 6, border_radius=40)
        self.button_rect = self.button_panel.get_rect(center=(self.WIDTH // 2, int(self.HEIGHT * 0.65)))

        self.pulse_t = 0

    #bg ============= memanipulasi nilai warna rgb, berdasarkan koordinat y
    def create_background(self):
        bg = pygame.Surface((self.WIDTH, self.HEIGHT))
        for y in range(self.HEIGHT):
            t = y / self.HEIGHT
            r = (1 - t) * 0.56 + t * 1
            g = (1 - t) * 0.90 + t * 1
            b = (1 - t) * 1.00 + t * 1
            pygame.draw.line(bg, (int(r*255), int(g*255), int(b*255)), (0, y), (self.WIDTH, y))
        return bg


    def make_cloud(self, scale=1.0):
        w, h = int(260 * scale), int(130 * scale)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 255, 255), (60, 70), int(40 * scale))
        pygame.draw.circle(surf, (255, 255, 255), (110, 60), int(40 * scale))
        pygame.draw.circle(surf, (255, 255, 255), (160, 65), int(40 * scale))
        pygame.draw.circle(surf, (255, 255, 255), (210, 75), int(35 * scale))
        return surf

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.scene_manager.change_scene("pilih_kategori")

    def update(self, dt):
        for cloud in self.clouds: 
            img, x, y, spd = cloud
            x += spd
            if x > self.WIDTH:
                x = -200
            cloud[1] = x

        self.pulse_t += dt * 2

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for img, x, y, spd in self.clouds:
            self.screen.blit(img, (x, y))

        fruit_x = (self.WIDTH - self.fruits.get_width()) // 2
        self.screen.blit(self.fruits, (fruit_x, self.fruit_y))

        title = self.title_font.render("BLOOMIO", True, (255, 182, 210))
        shadow = self.title_font.render("BLOOMIO", True, (170, 100, 150))
        tx = self.WIDTH // 2 - title.get_width() // 2
        ty = int(self.HEIGHT * 0.23)
        self.screen.blit(shadow, (tx + 6, ty + 6))
        self.screen.blit(title, (tx, ty))

        subtitle = self.subtitle_font.render("Grow Your Plants", True, (50, 50, 50))
        subtitle_y = int(self.HEIGHT * 0.43)
        self.screen.blit(subtitle, (self.WIDTH // 2 - subtitle.get_width() // 2, subtitle_y))

        #start pulse ============== startny bergerak
        scale = 1 + 0.03 * math.sin(self.pulse_t)
        btn_scaled = pygame.transform.smoothscale(
            self.button_panel,
            (int(self.button_panel.get_width() * scale), int(self.button_panel.get_height() * scale))
        )
        btn_rect = btn_scaled.get_rect(center=self.button_rect.center)
        self.screen.blit(btn_scaled, btn_rect)

        start_text = self.start_font.render("START", True, (255, 255, 255))
        shadow = self.start_font.render("START", True, (240, 240, 240))
        sx = btn_rect.centerx - start_text.get_width() // 2
        sy = btn_rect.centery - start_text.get_height() // 2
        self.screen.blit(shadow, (sx + 3, sy + 3))
        self.screen.blit(start_text, (sx, sy))

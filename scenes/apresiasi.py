import pygame
import math
import random
import os

class Apresiasi:
    def __init__(self, screen, scene_manager, plant_type="strawberry"):
        self.screen = screen
        self.scene_manager = scene_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.plant_type = plant_type
        
        # background
        bg_path = os.path.join('assets', 'images', 'bg-select.png')
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        # font
        font_path = os.path.join('assets', 'fonts', 'Heyam.ttf')
        font_path2 = os.path.join('assets', 'fonts', 'Super Joyful.ttf')
        try:
            self.font_title = pygame.font.Font(font_path, 90)
            self.font_subtitle = pygame.font.Font(font_path, 50)
            self.font_message = pygame.font.Font(font_path2, 36)
            self.font_button = pygame.font.Font(font_path, 40)
        except:
            self.font_title = pygame.font.Font(None, 90)
            self.font_subtitle = pygame.font.Font(None, 50)
            self.font_message = pygame.font.Font(None, 36)
            self.font_button = pygame.font.Font(None, 40)
        
        # Warna dasar
        self.WHITE = (255, 255, 255)
        self.BUTTON_GREEN = (126, 176, 105)
        
        # Konfigurasi per tanaman
        self.plant_configs = {
            'strawberry': {
                'name': 'Stroberi',
                'color': (220, 20, 60),
                'light_color': (255, 105, 180),
                'bg_color': (255, 240, 245),
                'confetti_colors': [(220, 20, 60), (255, 105, 180), (255, 192, 203)],
                'scene_back': 'pilih_buah',
                'emoji': '🍓'
            },
            'apel': {
                'name': 'Apel',
                'color': (220, 20, 60),
                'light_color': (255, 105, 97),
                'bg_color': (255, 245, 245),
                'confetti_colors': [(220, 20, 60), (255, 105, 97), (34, 139, 34)],
                'scene_back': 'pilih_buah',
                'emoji': '🍎'
            },
            'melon': {
                'name': 'Melon',
                'color': (144, 238, 144),
                'light_color': (152, 251, 152),
                'bg_color': (240, 255, 240),
                'confetti_colors': [(144, 238, 144), (152, 251, 152), (34, 139, 34)],
                'scene_back': 'pilih_buah',
                'emoji': '🍈'
            },
            'pakcoy': {
                'name': 'Pakcoy',
                'color': (60, 140, 80),
                'light_color': (100, 180, 120),
                'bg_color': (240, 255, 245),
                'confetti_colors': [(60, 140, 80), (100, 180, 120), (50, 205, 50)],
                'scene_back': 'pilih_sayur',
                'emoji': '🌱'
            },
            'seledri': {
                'name': 'Seledri',
                'color': (34, 139, 34),
                'light_color': (50, 205, 50),
                'bg_color': (240, 255, 240),
                'confetti_colors': [(34, 139, 34), (50, 205, 50), (144, 238, 144)],
                'scene_back': 'pilih_sayur',
                'emoji': '🌿'
            },
            'selada': {
                'name': 'Selada',
                'color': (107, 142, 35),
                'light_color': (154, 205, 50),
                'bg_color': (245, 255, 250),
                'confetti_colors': [(107, 142, 35), (154, 205, 50), (34, 139, 34)],
                'scene_back': 'pilih_sayur',
                'emoji': '🥬'
            }
        }
        
        self.config = self.plant_configs.get(plant_type, self.plant_configs['strawberry'])
        
        # Animation
        self.alpha = 0
        self.animation_phase = 0  
        self.animation_timer = 0
        
        # Confetti particles
        self.confetti = []
        self.spawn_confetti()
        
        # Star particles
        self.stars = []
        self.spawn_stars()
        
        # Button state
        self.button_hover = False
        
    def spawn_confetti(self):
        for _ in range(100):
            self.confetti.append({
                'x': random.randint(0, self.width),
                'y': random.randint(-self.height, 0),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(2, 5),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-5, 5),
                'color': random.choice(self.config['confetti_colors']),
                'size': random.randint(8, 15),
                'shape': random.choice(['rect', 'circle'])
            })
    
    def spawn_stars(self):
        for _ in range(30):
            self.stars.append({
                'x': random.randint(100, self.width - 100),
                'y': random.randint(100, self.height - 100),
                'size': random.randint(3, 8),
                'pulse': random.uniform(0, math.pi * 2),
                'pulse_speed': random.uniform(2, 4)
            })
    
    def draw_rounded_rect(self, surface, color, rect, radius):
        if len(color) == 4:
            temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, color, temp_surface.get_rect(), border_radius=radius)
            surface.blit(temp_surface, (rect.x, rect.y))
        else:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_plant_icon(self, x, y):
        if self.plant_type == 'strawberry':
            self.draw_strawberry_icon(x, y)
        elif self.plant_type == 'apel':
            self.draw_apple_icon(x, y)
        elif self.plant_type == 'melon':
            self.draw_melon_icon(x, y)
        elif self.plant_type == 'pakcoy':
            self.draw_pakcoy_icon(x, y)
        elif self.plant_type == 'seledri':
            self.draw_celery_icon(x, y)
        elif self.plant_type == 'selada':
            self.draw_lettuce_icon(x, y)
    
    def draw_strawberry_icon(self, x, y):
        pygame.draw.line(self.screen, (34, 139, 34), (x, y - 35), (x, y - 25), 5)
    
        for i in range(5):
            angle = (360 / 5) * i - 90
            rad = math.radians(angle)
            leaf_x = x + math.cos(rad) * 18
            leaf_y = y - 25 + math.sin(rad) * 18
            pygame.draw.polygon(self.screen, (34, 139, 34), [
                (x, y - 25),
                (int(leaf_x), int(leaf_y)),
                (x, y - 23)
            ])
        
        pygame.draw.circle(self.screen, self.config['color'], (x - 10, y), 15)
        pygame.draw.circle(self.screen, self.config['color'], (x + 10, y), 15)
        pygame.draw.polygon(self.screen, self.config['color'], [
            (x - 20, y),
            (x, y + 35),
            (x + 20, y)
        ])
        
        pygame.draw.circle(self.screen, self.config['light_color'], (x - 6, y - 3), 8)
        pygame.draw.circle(self.screen, self.WHITE, (x - 8, y - 5), 4)
        
        for i in range(20):
            sx = x + random.randint(-15, 15)
            sy = y + random.randint(-8, 28)
            pygame.draw.circle(self.screen, (255, 223, 0), (sx, sy), 2)

    def draw_apple_icon(self, x, y):
        pygame.draw.line(self.screen, (101, 67, 33), (x, y - 25), (x, y - 35), 5)
        pygame.draw.ellipse(self.screen, (34, 139, 34), (x - 18, y - 40, 25, 15))
        pygame.draw.circle(self.screen, self.config['color'], (x, y), 30)
        pygame.draw.circle(self.screen, self.config['light_color'], (x - 8, y - 8), 12)
        pygame.draw.circle(self.screen, self.WHITE, (x - 10, y - 10), 6)
    
    def draw_melon_icon(self, x, y):
        pygame.draw.ellipse(self.screen, self.config['color'], (x - 35, y - 25, 70, 50))
        
        for i in range(5):
            offset = -25 + (i * 12)
            pygame.draw.arc(self.screen, (34, 139, 34), 
                          (x + offset - 5, y - 25, 20, 50), 0, math.pi, 3)
        
        pygame.draw.ellipse(self.screen, self.config['light_color'], (x - 25, y - 18, 30, 20))
        pygame.draw.ellipse(self.screen, self.WHITE, (x - 22, y - 15, 15, 10))
    
    def draw_pakcoy_icon(self, x, y):
        green_dark = (90, 170, 90)
        green_mid = (130, 230, 130)
        green_light = (190, 255, 190)
        stem_white = (240, 255, 240)

        def draw_leaf(cx, cy, r):
            pygame.draw.circle(self.screen, green_dark, (cx, cy), r)
            pygame.draw.circle(self.screen, green_mid, (cx, cy), r - 3)
            pygame.draw.circle(self.screen, green_light, (cx - 2, cy - 2), r - 7)

        spacing = 22  
        start_x = x - (spacing * 2.5)

        for i in range(6):
            lx = start_x + i * spacing
            draw_leaf(lx, y, 16)

        inner_start_x = x - spacing
        for i in range(3):
            lx = inner_start_x + i * spacing
            draw_leaf(lx, y - 18, 11)

        stem_start_x = start_x
        for i in range(6):
            sx = stem_start_x + i * spacing
            pygame.draw.rect(self.screen, stem_white,
                (sx - 3, y + 10, 7, 26),
                border_radius=3
            )

            pygame.draw.rect(self.screen, (255, 255, 255),
                (sx - 1, y + 13, 2, 18),
                border_radius=2
            )
    
    def draw_celery_icon(self, x, y):
        for i in range(3):
            offset = -15 + (i * 15)
            pygame.draw.line(self.screen, self.config['light_color'], 
                           (x + offset, y + 20), (x + offset, y - 25), 8)
        
        for i in range(3):
            offset = -15 + (i * 15)
            for j in range(3):
                leaf_y = y - 25 - (j * 8)
    
                pygame.draw.ellipse(self.screen, self.config['color'],
                                  (x + offset - 12, leaf_y, 15, 10))
    
                pygame.draw.ellipse(self.screen, self.config['color'],
                                  (x + offset + 2, leaf_y, 15, 10))
    
    def draw_lettuce_icon(self, x, y):
        layers = [
            (40, self.config['color']),
            (32, self.config['light_color']),
            (24, (154, 205, 50))
        ]
        
        for size, color in layers:
            for i in range(6):
                angle = (360 / 6) * i
                rad = math.radians(angle)
                
                leaf_surf = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.ellipse(leaf_surf, color, (0, 0, size, size))
                
                offset = (40 - size) // 2
                lx = x + int(math.cos(rad) * offset)
                ly = y + int(math.sin(rad) * offset)
                
                rect = leaf_surf.get_rect(center=(lx, ly))
                self.screen.blit(leaf_surf, rect)
    
    def draw_confetti(self):
        for conf in self.confetti:
            if conf['shape'] == 'circle':
                pygame.draw.circle(self.screen, conf['color'],
                                 (int(conf['x']), int(conf['y'])), 
                                 conf['size'] // 2)
            else:
                rect_surf = pygame.Surface((conf['size'], conf['size'] // 2), pygame.SRCALPHA)
                pygame.draw.rect(rect_surf, conf['color'], rect_surf.get_rect())
                rotated = pygame.transform.rotate(rect_surf, conf['rotation'])
                rect = rotated.get_rect(center=(int(conf['x']), int(conf['y'])))
                self.screen.blit(rotated, rect)
    
    def draw_stars(self):
        for star in self.stars:
            pulse = math.sin(star['pulse']) * 0.5 + 0.5
            size = int(star['size'] * (0.5 + pulse * 0.5))
            
            points = []
            for i in range(4):
                angle = (360 / 4) * i
                rad = math.radians(angle)
                px = star['x'] + math.cos(rad) * size
                py = star['y'] + math.sin(rad) * size
                points.append((px, py))
            
            pygame.draw.polygon(self.screen, (255, 223, 0), points)
            pygame.draw.circle(self.screen, (255, 255, 200), 
                             (int(star['x']), int(star['y'])), size // 2)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.animation_phase >= 1:
                mouse_pos = pygame.mouse.get_pos()
                popup_width = 600
                popup_height = 500
                popup_x = self.width // 2 - popup_width // 2
                popup_y = self.height // 2 - popup_height // 2
                
                btn_width = 250
                btn_height = 60
                btn_x = popup_x + popup_width // 2 - btn_width // 2
                btn_y = popup_y + 410
                
                btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
                self.button_hover = btn_rect.collidepoint(mouse_pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.animation_phase >= 1:
                mouse_pos = pygame.mouse.get_pos()
                popup_width = 600
                popup_height = 500
                popup_x = self.width // 2 - popup_width // 2
                popup_y = self.height // 2 - popup_height // 2
                
                btn_width = 250
                btn_height = 60
                btn_x = popup_x + popup_width // 2 - btn_width // 2
                btn_y = popup_y + 410
                
                btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
                if btn_rect.collidepoint(mouse_pos):
                    self.scene_manager.change_scene(self.config['scene_back'])
    
    def update(self, dt):
        self.animation_timer += dt
        
        if self.animation_phase == 0:
            self.alpha = min(1.0, self.animation_timer / 1.0)
            if self.alpha >= 1.0:
                self.animation_phase = 1
                self.animation_timer = 0
        
        for conf in self.confetti:
            conf['x'] += conf['vx']
            conf['y'] += conf['vy']
            conf['rotation'] += conf['rotation_speed']
            
            if conf['y'] > self.height + 20:
                conf['y'] = -20
                conf['x'] = random.randint(0, self.width)
        
        for star in self.stars:
            star['pulse'] += star['pulse_speed'] * dt
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(180 * self.alpha)))
        self.screen.blit(overlay, (0, 0))
        
        if self.alpha > 0.3:
            self.draw_confetti()
            self.draw_stars()
        
        if self.alpha >= 0.5:
            popup_width = 600
            popup_height = 500
            popup_x = self.width // 2 - popup_width // 2
            popup_y = self.height // 2 - popup_height // 2
        
            shadow_rect = pygame.Rect(popup_x + 10, popup_y + 10, popup_width, popup_height)
            self.draw_rounded_rect(self.screen, (0, 0, 0, int(100 * self.alpha)), shadow_rect, 30)
        
            popup_surf = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
            pygame.draw.rect(popup_surf, (255, 209, 128, int(255 * self.alpha)), 
                            popup_surf.get_rect(), border_radius=30)
            pygame.draw.rect(popup_surf, (219, 123, 43, int(255 * self.alpha)), 
                            popup_surf.get_rect(), 6, border_radius=30)

            self.screen.blit(popup_surf, (popup_x, popup_y))
            
            if self.alpha >= 1.0:
                # Title
                title_text = self.font_title.render("SELAMAT!", True, (255, 140, 0))
                title_shadow = self.font_title.render("SELAMAT!", True, (139, 69, 19))
                self.screen.blit(title_shadow, 
                                (popup_x + popup_width // 2 - title_text.get_width() // 2 + 4, popup_y + 54))
                self.screen.blit(title_text, 
                                (popup_x + popup_width // 2 - title_text.get_width() // 2, popup_y + 50))
                
                # Background icon
                circle_y = popup_y + 200
                pygame.draw.circle(self.screen, (255, 223, 0), 
                                (popup_x + popup_width // 2, circle_y), 75)
                pygame.draw.circle(self.screen, (255, 255, 150), 
                                (popup_x + popup_width // 2, circle_y), 65)
                
                # Messages
                msg1 = self.font_message.render("Kamu berhasil menanam", True, (88, 129, 87))
                msg2 = self.font_message.render(f"dan memanen {self.config['name']}!", True, (88, 129, 87))
                
                self.screen.blit(msg1, 
                                (popup_x + popup_width // 2 - msg1.get_width() // 2, popup_y + 300))
                self.screen.blit(msg2, 
                                (popup_x + popup_width // 2 - msg2.get_width() // 2, popup_y + 345))
                
                # Button kembali
                btn_width = 250
                btn_height = 60
                btn_x = popup_x + popup_width // 2 - btn_width // 2
                btn_y = popup_y + 410
                
                btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
                btn_color = (150, 200, 130) if self.button_hover else self.BUTTON_GREEN
                
                self.draw_rounded_rect(self.screen, btn_color, btn_rect, 18)
                pygame.draw.rect(self.screen, self.WHITE, btn_rect, 4, border_radius=18)
                
                btn_text = self.font_button.render("Kembali", True, self.WHITE)
                self.screen.blit(btn_text, 
                                (btn_x + btn_width // 2 - btn_text.get_width() // 2, btn_y + 13))

                self.draw_plant_icon(popup_x + popup_width // 2, circle_y)

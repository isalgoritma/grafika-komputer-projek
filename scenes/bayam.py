import pygame
import math
import random
import os

class GrowthBayam:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Load background
        bg_path = os.path.join('assets', 'images', 'bg-select.png')
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        # Load font
        font_path = os.path.join('assets', 'fonts', 'Heyam.ttf')
        try:
            self.font_title = pygame.font.Font(font_path, 60)
            self.font_stage = pygame.font.Font(font_path, 40)
            self.font_button = pygame.font.Font(font_path, 35)
        except:
            self.font_title = pygame.font.Font(None, 60)
            self.font_stage = pygame.font.Font(None, 40)
            self.font_button = pygame.font.Font(None, 35)
        
        # Warna
        self.SOIL_BROWN = (101, 67, 33)
        self.SOIL_DARK = (76, 50, 25)
        self.SPINACH_GREEN = (60, 140, 80)
        self.DARK_GREEN = (40, 100, 60)
        self.LIGHT_GREEN = (100, 180, 120)
        self.STEM_GREEN = (80, 120, 80)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 220, 100)
        self.BUTTON_GREEN = (126, 176, 105)
        self.WATER_BLUE = (100, 180, 255)
        
        # Tahapan pertumbuhan bayam
        self.stages = [
            "Biji",
            "Kecambah",
            "Vegetatif",
            "Generatif",
            "Panen"
        ]
        
        self.current_stage = 0
        
        # Faktor pertumbuhan
        self.water_level = 50
        self.sunlight_level = 50
        self.fertilizer_level = 50
        
        # UI Buttons
        self.buttons = {
            'water': {'rect': None, 'hover': False, 'label': 'Air'},
            'sun': {'rect': None, 'hover': False, 'label': 'Sinar'},
            'fertilizer': {'rect': None, 'hover': False, 'label': 'Pupuk'},
            'next': {'rect': None, 'hover': False, 'label': 'Tahap →'}
        }
        
        # Particle effects
        self.particles = []
        
        # Animation
        self.plant_sway = 0
        self.leaf_wave = 0
    
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Menggambar persegi dengan sudut melengkung"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_soil(self):
        """Menggambar tanah"""
        soil_y = self.height - 250
        
        # Tanah gelap
        pygame.draw.rect(self.screen, self.SOIL_DARK, 
                        (0, soil_y + 30, self.width, 220))
        
        # Tanah terang
        pygame.draw.rect(self.screen, self.SOIL_BROWN, 
                        (0, soil_y, self.width, 30))
        
        # Tekstur tanah
        for i in range(100):
            x = random.randint(0, self.width)
            y = random.randint(soil_y + 30, self.height)
            size = random.randint(1, 3)
            pygame.draw.circle(self.screen, self.SOIL_DARK, (x, y), size)
    
    def draw_seed(self, x, y):
        """Menggambar biji bayam"""
        # Biji kecil bulat
        pygame.draw.circle(self.screen, (120, 80, 40), (x, y), 8)
        pygame.draw.circle(self.screen, (150, 110, 60), (x, y), 5)
        pygame.draw.circle(self.screen, (180, 140, 80), (x - 2, y - 2), 2)
    
    def draw_sprout(self, x, y):
        """Menggambar kecambah bayam"""
        sway = math.sin(self.plant_sway) * 2
        
        # Batang kecil
        pygame.draw.line(self.screen, self.STEM_GREEN, 
                        (x, y), (x + int(sway), y - 35), 4)
        
        # Dua daun embrio kecil (kotiledon)
        # Daun kiri
        leaf_points_left = [
            (x + int(sway), y - 35),
            (x + int(sway) - 12, y - 32),
            (x + int(sway) - 8, y - 28),
            (x + int(sway), y - 30)
        ]
        pygame.draw.polygon(self.screen, self.SPINACH_GREEN, leaf_points_left)
        pygame.draw.polygon(self.screen, self.LIGHT_GREEN, [
            (x + int(sway), y - 35),
            (x + int(sway) - 10, y - 33),
            (x + int(sway) - 6, y - 30)
        ])
        
        # Daun kanan
        leaf_points_right = [
            (x + int(sway), y - 35),
            (x + int(sway) + 12, y - 32),
            (x + int(sway) + 8, y - 28),
            (x + int(sway), y - 30)
        ]
        pygame.draw.polygon(self.screen, self.SPINACH_GREEN, leaf_points_right)
        pygame.draw.polygon(self.screen, self.LIGHT_GREEN, [
            (x + int(sway), y - 35),
            (x + int(sway) + 10, y - 33),
            (x + int(sway) + 6, y - 30)
        ])
    
    def draw_spinach_leaf(self, x, y, size, angle, wave_offset=0):
        """Menggambar daun bayam (oval dengan tekstur)"""
        wave = math.sin(self.leaf_wave + wave_offset) * 2
        
        # Rotasi untuk variasi
        cos_a = math.cos(math.radians(angle))
        sin_a = math.sin(math.radians(angle))
        
        # Daun berbentuk oval memanjang
        leaf_width = int(size * 0.6)
        leaf_height = int(size)
        
        # Gambar oval untuk daun
        leaf_surf = pygame.Surface((leaf_width * 2, leaf_height * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(leaf_surf, self.SPINACH_GREEN, 
                           (0, 0, leaf_width * 2, leaf_height * 2))
        
        # Highlight
        pygame.draw.ellipse(leaf_surf, self.LIGHT_GREEN, 
                           (5, 5, leaf_width * 2 - 20, leaf_height * 2 - 20))
        
        # Urat daun (garis tengah)
        pygame.draw.line(leaf_surf, self.DARK_GREEN, 
                        (leaf_width, 0), (leaf_width, leaf_height * 2), 2)
        
        # Rotate and blit
        rotated = pygame.transform.rotate(leaf_surf, angle)
        rect = rotated.get_rect(center=(x + int(wave), y))
        self.screen.blit(rotated, rect)
    
    def draw_vegetative(self, x, y):
        """Menggambar fase vegetatif (banyak daun)"""
        sway = math.sin(self.plant_sway) * 3
        
        # Batang pusat (pendek, bayam tumbuh dari roset)
        pygame.draw.line(self.screen, self.STEM_GREEN, 
                        (x, y), (x + int(sway), y - 20), 6)
        
        # Bayam tumbuh dalam bentuk roset (daun melingkar dari pusat)
        # 8-10 daun
        num_leaves = 10
        for i in range(num_leaves):
            angle = (360 / num_leaves) * i
            distance = 35 + (i % 3) * 10
            rad = math.radians(angle)
            
            leaf_x = x + int(math.cos(rad) * distance) + int(sway * 0.5)
            leaf_y = y - 20 + int(math.sin(rad) * distance * 0.6)
            
            leaf_size = 40 + (i % 3) * 5
            leaf_angle = angle - 90
            
            self.draw_spinach_leaf(leaf_x, leaf_y, leaf_size, leaf_angle, i * 0.5)
    
    def draw_generative(self, x, y):
        """Menggambar fase generatif (mulai berbunga - opsional untuk bayam)"""
        # Bayam fase generatif mulai tumbuh tinggi (bolting)
        sway = math.sin(self.plant_sway) * 4
        
        # Batang memanjang ke atas
        pygame.draw.line(self.screen, self.STEM_GREEN, 
                        (x, y), (x + int(sway), y - 120), 8)
        
        # Daun-daun di batang
        for i in range(5):
            leaf_y = y - 25 - (i * 20)
            leaf_x = x + int(sway * (1 - i * 0.15))
            
            # Daun kiri
            self.draw_spinach_leaf(leaf_x - 15, leaf_y, 35, -45 + i * 5, i)
            
            # Daun kanan
            self.draw_spinach_leaf(leaf_x + 15, leaf_y, 35, 45 - i * 5, i + 0.3)
        
        # Bunga kecil di atas (kuning-hijau)
        flower_x = x + int(sway)
        flower_y = y - 125
        
        # Cluster bunga kecil
        for i in range(5):
            f_x = flower_x + random.randint(-8, 8)
            f_y = flower_y + random.randint(-5, 5)
            pygame.draw.circle(self.screen, self.YELLOW, (f_x, f_y), 3)
            pygame.draw.circle(self.screen, (255, 255, 150), (f_x, f_y), 2)
    
    def draw_harvest(self, x, y):
        """Menggambar hasil panen bayam"""
        # Tampilkan beberapa daun bayam yang sudah dipetik
        for i in range(5):
            leaf_x = x - 80 + (i * 40)
            leaf_y = y - 60 + ((i % 2) * 20)
            
            # Daun bayam segar
            self.draw_spinach_leaf(leaf_x, leaf_y, 50, -45 + (i * 20), i * 0.5)
        
        # Teks "Panen!"
        harvest_font = pygame.font.Font(None, 60)
        harvest_text = harvest_font.render("Panen!", True, self.SPINACH_GREEN)
        harvest_shadow = harvest_font.render("Panen!", True, self.DARK_GREEN)
        
        text_x = x - harvest_text.get_width() // 2
        text_y = y - 140
        
        self.screen.blit(harvest_shadow, (text_x + 3, text_y + 3))
        self.screen.blit(harvest_text, (text_x, text_y))
    
    def draw_plant(self):
        """Menggambar tanaman sesuai tahap"""
        center_x = self.width // 2
        soil_y = self.height - 250
        
        if self.current_stage == 0:  # Biji
            self.draw_seed(center_x, soil_y + 15)
        elif self.current_stage == 1:  # Kecambah
            self.draw_sprout(center_x, soil_y)
        elif self.current_stage == 2:  # Vegetatif
            self.draw_vegetative(center_x, soil_y)
        elif self.current_stage == 3:  # Generatif
            self.draw_generative(center_x, soil_y)
        elif self.current_stage == 4:  # Panen
            self.draw_harvest(center_x, soil_y)
    
    def draw_ui(self):
        """Menggambar UI controls"""
        # Stage indicator
        stage_text = self.font_stage.render(
            f"Tahap: {self.stages[self.current_stage]}", 
            True, self.WHITE
        )
        stage_bg = pygame.Rect(self.width // 2 - 200, 20, 400, 60)
        self.draw_rounded_rect(self.screen, (88, 129, 87, 200), stage_bg, 20)
        self.screen.blit(stage_text, 
                        (self.width // 2 - stage_text.get_width() // 2, 35))
        
        # Level bars (Air, Sinar, Pupuk)
        bar_width = 150
        bar_height = 20
        bar_x = 30
        bar_start_y = 100
        bar_spacing = 50
        
        levels = [
            ('Air', self.water_level, (100, 180, 255)),
            ('Sinar', self.sunlight_level, (255, 220, 100)),
            ('Pupuk', self.fertilizer_level, (100, 180, 100))
        ]
        
        for i, (label, level, color) in enumerate(levels):
            y = bar_start_y + (i * bar_spacing)
            
            # Label
            label_text = self.font_button.render(label, True, self.WHITE)
            self.screen.blit(label_text, (bar_x, y - 5))
            
            # Bar background
            bar_bg = pygame.Rect(bar_x + 100, y, bar_width, bar_height)
            pygame.draw.rect(self.screen, (50, 50, 50), bar_bg, border_radius=10)
            
            # Bar fill
            fill_width = int((level / 100) * bar_width)
            if fill_width > 0:
                bar_fill = pygame.Rect(bar_x + 100, y, fill_width, bar_height)
                pygame.draw.rect(self.screen, color, bar_fill, border_radius=10)
            
            # Border
            pygame.draw.rect(self.screen, self.WHITE, bar_bg, 2, border_radius=10)
        
        # Control buttons (bottom)
        button_y = self.height - 120
        button_spacing = 150
        start_x = self.width // 2 - (button_spacing * 1.5)
        
        controls = ['water', 'sun', 'fertilizer']
        for i, control in enumerate(controls):
            button_x = start_x + (i * button_spacing)
            button_rect = pygame.Rect(button_x, button_y, 120, 80)
            self.buttons[control]['rect'] = button_rect
            
            # Button background
            color = (126, 176, 105) if not self.buttons[control]['hover'] else (150, 200, 130)
            self.draw_rounded_rect(self.screen, color, button_rect, 15)
            
            # Border
            pygame.draw.rect(self.screen, (88, 129, 87), button_rect, 3, border_radius=15)
            
            # Label
            label = self.font_button.render(self.buttons[control]['label'], True, self.WHITE)
            self.screen.blit(label, 
                           (button_x + 60 - label.get_width() // 2, button_y + 50))
        
        # Next stage button
        next_button_rect = pygame.Rect(self.width - 250, button_y, 220, 80)
        self.buttons['next']['rect'] = next_button_rect
        
        color = (126, 176, 105) if not self.buttons['next']['hover'] else (150, 200, 130)
        self.draw_rounded_rect(self.screen, color, next_button_rect, 15)
        pygame.draw.rect(self.screen, (88, 129, 87), next_button_rect, 3, border_radius=15)
        
        next_text = self.font_button.render("Tahap →", True, self.WHITE)
        self.screen.blit(next_text, 
                        (self.width - 140 - next_text.get_width() // 2, button_y + 30))
    
    def add_particles(self, x, y, color, count=10):
        """Tambah particle effects"""
        for _ in range(count):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-5, -2),
                'life': 1.0,
                'color': color,
                'size': random.randint(2, 5)
            })
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for key in self.buttons:
                if self.buttons[key]['rect']:
                    self.buttons[key]['hover'] = self.buttons[key]['rect'].collidepoint(mouse_pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.buttons['water']['rect'] and self.buttons['water']['rect'].collidepoint(mouse_pos):
                self.water_level = min(100, self.water_level + 20)
                self.add_particles(mouse_pos[0], mouse_pos[1], self.WATER_BLUE, 15)
                print("Disiram!")
            
            elif self.buttons['sun']['rect'] and self.buttons['sun']['rect'].collidepoint(mouse_pos):
                self.sunlight_level = min(100, self.sunlight_level + 20)
                self.add_particles(mouse_pos[0], mouse_pos[1], self.YELLOW, 15)
                print("Dijemur!")
            
            elif self.buttons['fertilizer']['rect'] and self.buttons['fertilizer']['rect'].collidepoint(mouse_pos):
                self.fertilizer_level = min(100, self.fertilizer_level + 20)
                self.add_particles(mouse_pos[0], mouse_pos[1], self.SPINACH_GREEN, 15)
                print("Dipupuk!")
            
            elif self.buttons['next']['rect'] and self.buttons['next']['rect'].collidepoint(mouse_pos):
                if self.current_stage < len(self.stages) - 1:
                    self.current_stage += 1
                    print(f"Tahap: {self.stages[self.current_stage]}")
                else:
                    print("Selesai! Kembali ke menu...")
                    self.scene_manager.change_scene("pilih_sayur")
    
    def update(self, dt):
        """Update animasi"""
        self.plant_sway += dt * 2
        self.leaf_wave += dt * 3
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Decrease levels gradually
        self.water_level = max(0, self.water_level - dt * 2)
        self.sunlight_level = max(0, self.sunlight_level - dt * 2)
        self.fertilizer_level = max(0, self.fertilizer_level - dt * 2)
    
    def draw(self):
        """Render scene"""
        self.screen.blit(self.background, (0, 0))
        
        self.draw_soil()
        self.draw_plant()
        
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
        
        self.draw_ui()
import pygame
import math
import random
import os

class GrowthStroberi:
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
        self.GREEN = (80, 150, 80)
        self.DARK_GREEN = (60, 120, 60)
        self.RED = (220, 50, 50)
        self.LIGHT_RED = (255, 100, 100)
        self.PINK = (255, 150, 180)
        self.YELLOW = (255, 220, 100)
        self.WHITE = (255, 255, 255)
        self.BUTTON_GREEN = (126, 176, 105)
        self.BUTTON_DARK = (88, 129, 87)
        self.WATER_BLUE = (100, 180, 255)
        
        # Tahapan pertumbuhan
        self.stages = [
            "Biji",
            "Kecambah",
            "Vegetatif",
            "Generatif",
            "Bunga",
            "Buah",
            "Pematangan Buah",
            "Panen"
        ]
        
        self.current_stage = 0
        self.growth_progress = 0
        
        # Faktor pertumbuhan
        self.water_level = 50
        self.sunlight_level = 50
        self.fertilizer_level = 50
        
        # UI Buttons
        self.buttons = {
            'water': {'rect': None, 'hover': False, 'icon': '💧', 'label': 'Air'},
            'sun': {'rect': None, 'hover': False, 'icon': '☀️', 'label': 'Sinar'},
            'fertilizer': {'rect': None, 'hover': False, 'icon': '🌱', 'label': 'Pupuk'},
            'next': {'rect': None, 'hover': False, 'label': 'Tahap Berikutnya'}
        }
        
        # Particle effects
        self.particles = []
        
        # Animation
        self.plant_sway = 0
        self.flower_spin = 0
        
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Menggambar persegi dengan sudut melengkung"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_soil(self):
        """Menggambar tanah"""
        soil_y = self.height - 250
        
        # Tanah gelap (bawah)
        pygame.draw.rect(self.screen, self.SOIL_DARK, 
                        (0, soil_y + 30, self.width, 220))
        
        # Tanah terang (atas dengan tekstur)
        pygame.draw.rect(self.screen, self.SOIL_BROWN, 
                        (0, soil_y, self.width, 30))
        
        # Tambah tekstur tanah (dots kecil)
        for i in range(100):
            x = random.randint(0, self.width)
            y = random.randint(soil_y + 30, self.height)
            size = random.randint(1, 3)
            pygame.draw.circle(self.screen, self.SOIL_DARK, (x, y), size)
    
    def draw_seed(self, x, y):
        """Menggambar biji"""
        # Biji coklat
        pygame.draw.ellipse(self.screen, (139, 90, 43), (x-15, y-10, 30, 20))
        pygame.draw.ellipse(self.screen, (160, 110, 60), (x-12, y-8, 24, 16))
    
    def draw_sprout(self, x, y):
        """Menggambar kecambah"""
        sway = math.sin(self.plant_sway) * 3
        
        # Batang kecil
        pygame.draw.line(self.screen, self.DARK_GREEN, 
                        (x, y), (x + int(sway), y - 40), 5)
        
        # Daun pertama (kecil)
        leaf_points = [
            (x + int(sway), y - 40),
            (x + int(sway) - 15, y - 35),
            (x + int(sway) - 10, y - 30),
            (x + int(sway), y - 35)
        ]
        pygame.draw.polygon(self.screen, self.GREEN, leaf_points)
        
        # Daun kedua
        leaf_points2 = [
            (x + int(sway), y - 40),
            (x + int(sway) + 15, y - 35),
            (x + int(sway) + 10, y - 30),
            (x + int(sway), y - 35)
        ]
        pygame.draw.polygon(self.screen, self.GREEN, leaf_points2)
    
    def draw_vegetative(self, x, y):
        """Menggambar fase vegetatif (batang dan daun lebih banyak)"""
        sway = math.sin(self.plant_sway) * 5
        
        # Batang utama
        pygame.draw.line(self.screen, self.DARK_GREEN, 
                        (x, y), (x + int(sway), y - 80), 8)
        
        # Daun-daun (5 pasang)
        for i in range(5):
            leaf_y = y - 20 - (i * 15)
            leaf_x = x + int(sway * (1 - i * 0.1))
            
            # Daun kiri
            pygame.draw.ellipse(self.screen, self.GREEN, 
                              (leaf_x - 30, leaf_y - 10, 35, 20))
            pygame.draw.ellipse(self.screen, (100, 170, 100), 
                              (leaf_x - 28, leaf_y - 8, 31, 16))
            
            # Daun kanan
            pygame.draw.ellipse(self.screen, self.GREEN, 
                              (leaf_x, leaf_y - 10, 35, 20))
            pygame.draw.ellipse(self.screen, (100, 170, 100), 
                              (leaf_x + 2, leaf_y - 8, 31, 16))
    
    def draw_generative(self, x, y):
        """Menggambar fase generatif (siap berbunga)"""
        self.draw_vegetative(x, y)
        
        # Tambah tunas bunga di atas
        sway = math.sin(self.plant_sway) * 5
        bud_x = x + int(sway)
        bud_y = y - 90
        
        # Tunas kecil
        pygame.draw.circle(self.screen, (150, 200, 150), (bud_x, bud_y), 8)
        pygame.draw.circle(self.screen, (180, 220, 180), (bud_x, bud_y), 5)
    
    def draw_flower(self, x, y):
        """Menggambar fase berbunga"""
        self.draw_vegetative(x, y)
        
        sway = math.sin(self.plant_sway) * 5
        flower_x = x + int(sway)
        flower_y = y - 100
        
        # Kelopak bunga stroberi (putih/pink)
        for i in range(5):
            angle = (360 / 5) * i + self.flower_spin
            rad = math.radians(angle)
            petal_x = flower_x + math.cos(rad) * 15
            petal_y = flower_y + math.sin(rad) * 15
            pygame.draw.circle(self.screen, self.WHITE, (int(petal_x), int(petal_y)), 10)
            pygame.draw.circle(self.screen, self.PINK, (int(petal_x), int(petal_y)), 7)
        
        # Tengah bunga (kuning)
        pygame.draw.circle(self.screen, self.YELLOW, (flower_x, flower_y), 8)
        pygame.draw.circle(self.screen, (255, 240, 150), (flower_x - 2, flower_y - 2), 4)
    
    def draw_fruit(self, x, y):
        """Menggambar buah stroberi muda (hijau)"""
        self.draw_vegetative(x, y - 20)
        
        sway = math.sin(self.plant_sway) * 5
        fruit_x = x + int(sway)
        fruit_y = y - 110
        
        # Buah berbentuk hati (masih hijau)
        pygame.draw.circle(self.screen, (100, 200, 100), (fruit_x - 8, fruit_y), 12)
        pygame.draw.circle(self.screen, (100, 200, 100), (fruit_x + 8, fruit_y), 12)
        pygame.draw.polygon(self.screen, (100, 200, 100), [
            (fruit_x - 15, fruit_y),
            (fruit_x, fruit_y + 25),
            (fruit_x + 15, fruit_y)
        ])
        
        # Daun kecil di atas buah
        for i in range(5):
            angle = (360 / 5) * i - 90
            rad = math.radians(angle)
            leaf_x = fruit_x + math.cos(rad) * 12
            leaf_y = fruit_y - 8 + math.sin(rad) * 12
            pygame.draw.polygon(self.screen, self.DARK_GREEN, [
                (fruit_x, fruit_y - 8),
                (int(leaf_x), int(leaf_y)),
                (fruit_x, fruit_y - 5)
            ])
    
    def draw_ripe_fruit(self, x, y):
        """Menggambar buah stroberi matang (merah)"""
        self.draw_vegetative(x, y - 20)
        
        sway = math.sin(self.plant_sway) * 5
        fruit_x = x + int(sway)
        fruit_y = y - 110
        
        # Buah berbentuk hati (merah cerah)
        pygame.draw.circle(self.screen, self.RED, (fruit_x - 10, fruit_y), 15)
        pygame.draw.circle(self.screen, self.RED, (fruit_x + 10, fruit_y), 15)
        pygame.draw.polygon(self.screen, self.RED, [
            (fruit_x - 18, fruit_y),
            (fruit_x, fruit_y + 30),
            (fruit_x + 18, fruit_y)
        ])
        
        # Highlight
        pygame.draw.circle(self.screen, self.LIGHT_RED, (fruit_x - 5, fruit_y - 5), 8)
        
        # Biji-biji kecil
        for i in range(12):
            seed_x = fruit_x + random.randint(-12, 12)
            seed_y = fruit_y + random.randint(-8, 20)
            pygame.draw.circle(self.screen, self.YELLOW, (seed_x, seed_y), 2)
        
        # Daun di atas
        for i in range(5):
            angle = (360 / 5) * i - 90
            rad = math.radians(angle)
            leaf_x = fruit_x + math.cos(rad) * 15
            leaf_y = fruit_y - 12 + math.sin(rad) * 15
            pygame.draw.polygon(self.screen, self.DARK_GREEN, [
                (fruit_x, fruit_y - 12),
                (int(leaf_x), int(leaf_y)),
                (fruit_x, fruit_y - 8)
            ])
    
    def draw_harvest(self, x, y):
        """Menggambar hasil panen"""
        # Tampilkan beberapa buah stroberi yang sudah dipanen
        for i in range(3):
            fruit_x = x - 60 + (i * 60)
            fruit_y = y - 80
            
            # Buah stroberi
            pygame.draw.circle(self.screen, self.RED, (fruit_x - 8, fruit_y), 12)
            pygame.draw.circle(self.screen, self.RED, (fruit_x + 8, fruit_y), 12)
            pygame.draw.polygon(self.screen, self.RED, [
                (fruit_x - 15, fruit_y),
                (fruit_x, fruit_y + 25),
                (fruit_x + 15, fruit_y)
            ])
            
            pygame.draw.circle(self.screen, self.LIGHT_RED, (fruit_x - 3, fruit_y - 3), 6)
            
            # Biji
            for j in range(8):
                seed_x = fruit_x + random.randint(-10, 10)
                seed_y = fruit_y + random.randint(-5, 15)
                pygame.draw.circle(self.screen, self.YELLOW, (seed_x, seed_y), 1)
    
    def draw_plant(self):
        """Menggambar tanaman sesuai tahap"""
        center_x = self.width // 2
        soil_y = self.height - 250
        
        if self.current_stage == 0:  # Biji
            self.draw_seed(center_x, soil_y + 20)
        elif self.current_stage == 1:  # Kecambah
            self.draw_sprout(center_x, soil_y)
        elif self.current_stage == 2:  # Vegetatif
            self.draw_vegetative(center_x, soil_y)
        elif self.current_stage == 3:  # Generatif
            self.draw_generative(center_x, soil_y)
        elif self.current_stage == 4:  # Bunga
            self.draw_flower(center_x, soil_y)
        elif self.current_stage == 5:  # Buah
            self.draw_fruit(center_x, soil_y)
        elif self.current_stage == 6:  # Pematangan
            self.draw_ripe_fruit(center_x, soil_y)
        elif self.current_stage == 7:  # Panen
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
                self.add_particles(mouse_pos[0], mouse_pos[1], self.GREEN, 15)
                print("Dipupuk!")
            
            elif self.buttons['next']['rect'] and self.buttons['next']['rect'].collidepoint(mouse_pos):
                if self.current_stage < len(self.stages) - 1:
                    self.current_stage += 1
                    print(f"Tahap: {self.stages[self.current_stage]}")
                else:
                    print("Selesai! Kembali ke menu...")
                    self.scene_manager.change_scene("pilih_buah")
    
    def update(self, dt):
        """Update animasi"""
        self.plant_sway += dt * 2
        self.flower_spin += dt * 20
        
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
            alpha = int(255 * particle['life'])
            color = particle['color'] + (alpha,)
            pygame.draw.circle(self.screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
        
        self.draw_ui()
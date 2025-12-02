import pygame
import math
import random
import os

class GrowthApel:
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
            self.font_button = pygame.font.Font(font_path, 30)
            self.font_small = pygame.font.Font(font_path, 24)
        except:
            self.font_title = pygame.font.Font(None, 60)
            self.font_stage = pygame.font.Font(None, 40)
            self.font_button = pygame.font.Font(None, 30)
            self.font_small = pygame.font.Font(None, 24)
        
        # Warna
        self.SOIL_BROWN = (101, 67, 33)
        self.SOIL_DARK = (76, 50, 25)
        self.TRUNK_BROWN = (101, 67, 33)
        self.DARK_BROWN = (76, 50, 25)
        self.GREEN = (34, 139, 34)
        self.DARK_GREEN = (0, 100, 0)
        self.LEAF_GREEN = (50, 205, 50)
        self.LIGHT_GREEN = (144, 238, 144)
        self.RED_APPLE = (220, 20, 60)
        self.LIGHT_RED = (255, 105, 97)
        self.PINK = (255, 182, 193)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 223, 0)
        self.BUTTON_GREEN = (126, 176, 105)
        self.WATER_BLUE = (135, 206, 250)
        self.CLOUD_WHITE = (240, 248, 255)
        self.SKY_BLUE = (135, 206, 235)
        
        # Tahapan pertumbuhan
        self.stages = [
            "Biji",
            "Kecambah",
            "Daun Muda",
            "Bunga",
            "Buah Muda",
            "Buah Matang",
            "Panen"
        ]
        
        self.current_stage = 0
        self.growth_progress = 0
        self.stage_requirements = [20, 30, 40, 50, 60, 70, 80]
        
        # Faktor pertumbuhan
        self.water_level = 40
        self.sunlight_level = 40
        self.fertilizer_level = 40
        
        # Kebutuhan per detik
        self.water_consumption = 2.5
        self.sunlight_consumption = 2
        self.fertilizer_consumption = 1.5
        
        # Awan interaktif
        self.cloud = {
            'x': self.width // 4,
            'y': 100,
            'width': 150,
            'height': 80,
            'dragging': False,
            'raining': False,
            'rain_drops': []
        }
        
        # Matahari
        self.sun = {
            'x': self.width - 150,
            'y': 100,
            'radius': 50,
            'rays': [],
            'glow': 0
        }
        
        # Pupuk
        self.fertilizer_bag = {
            'x': self.width - 200,
            'y': self.height - 200,
            'width': 80,
            'height': 100,
            'hover': False,
            'particles': []
        }
        
        # Harvest state
        self.total_harvested = 0
        self.harvested_apples = []
        self.harvest_button_hover = False
        
        # Particle effects
        self.particles = []
        
        # Animation
        self.plant_sway = 0
        self.flower_spin = 0
        self.time = 0
        
        # Messages
        self.message = ""
        self.message_timer = 0
        
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Menggambar persegi dengan sudut melengkung"""
        if len(color) == 4:
            temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, color, temp_surface.get_rect(), border_radius=radius)
            surface.blit(temp_surface, (rect.x, rect.y))
        else:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_sky_elements(self):
        """Menggambar awan dan matahari"""
        # === AWAN ===
        cloud_x = int(self.cloud['x'])
        cloud_y = int(self.cloud['y'])
        
        # Bayangan awan
        pygame.draw.ellipse(self.screen, (200, 200, 200), 
                           (cloud_x + 5, cloud_y + 5, 60, 40))
        pygame.draw.ellipse(self.screen, (200, 200, 200), 
                           (cloud_x + 45, cloud_y + 5, 70, 50))
        pygame.draw.ellipse(self.screen, (200, 200, 200), 
                           (cloud_x + 85, cloud_y + 5, 60, 40))
        
        # Awan putih
        pygame.draw.ellipse(self.screen, self.CLOUD_WHITE, 
                           (cloud_x, cloud_y, 60, 40))
        pygame.draw.ellipse(self.screen, self.CLOUD_WHITE, 
                           (cloud_x + 40, cloud_y, 70, 50))
        pygame.draw.ellipse(self.screen, self.CLOUD_WHITE, 
                           (cloud_x + 80, cloud_y, 60, 40))
        
        # Highlight awan
        pygame.draw.ellipse(self.screen, (255, 255, 255), 
                           (cloud_x + 10, cloud_y + 5, 40, 25))
        
        # Tetesan hujan
        if self.cloud['raining']:
            for drop in self.cloud['rain_drops']:
                pygame.draw.line(self.screen, self.WATER_BLUE,
                               (int(drop['x']), int(drop['y'])),
                               (int(drop['x']), int(drop['y']) + 8), 2)
        
        # === MATAHARI ===
        sun_x = int(self.sun['x'])
        sun_y = int(self.sun['y'])
        radius = self.sun['radius']
        
        # Cahaya glow
        for i in range(3):
            glow_radius = radius + 20 - (i * 7)
            glow_alpha = 30 - (i * 10)
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 0, glow_alpha), 
                             (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surf, (sun_x - glow_radius, sun_y - glow_radius))
        
        # Sinar matahari
        for i in range(12):
            angle = (360 / 12) * i + self.time * 10
            rad = math.radians(angle)
            start_x = sun_x + math.cos(rad) * radius
            start_y = sun_y + math.sin(rad) * radius
            end_x = sun_x + math.cos(rad) * (radius + 25)
            end_y = sun_y + math.sin(rad) * (radius + 25)
            
            pygame.draw.line(self.screen, (255, 223, 0),
                           (int(start_x), int(start_y)),
                           (int(end_x), int(end_y)), 4)
        
        # Lingkaran matahari
        pygame.draw.circle(self.screen, (255, 200, 0), (sun_x, sun_y), radius)
        pygame.draw.circle(self.screen, self.YELLOW, (sun_x, sun_y), radius - 5)
        
        # Highlight
        pygame.draw.circle(self.screen, (255, 255, 200), (sun_x - 10, sun_y - 10), 15)
    
    def draw_soil(self):
        """Menggambar tanah dengan tekstur"""
        soil_y = self.height - 250
        
        # Lapisan tanah
        for i in range(5):
            y_offset = i * 3
            color_variation = (101 - i * 5, 67 - i * 3, 33 - i * 2)
            pygame.draw.rect(self.screen, color_variation,
                           (0, soil_y + 30 + y_offset, self.width, 3))
        
        # Tanah gelap (bawah)
        pygame.draw.rect(self.screen, self.SOIL_DARK, 
                        (0, soil_y + 45, self.width, 205))
        
        # Tanah terang (atas)
        pygame.draw.rect(self.screen, self.SOIL_BROWN, 
                        (0, soil_y, self.width, 45))
        
        # Tekstur tanah
        random.seed(42)
        for i in range(150):
            x = random.randint(0, self.width)
            y = random.randint(soil_y + 30, self.height)
            size = random.randint(1, 4)
            color_var = random.randint(0, 20)
            pygame.draw.circle(self.screen, 
                             (76 - color_var, 50 - color_var, 25 - color_var), 
                             (x, y), size)
        random.seed()
    
    def draw_seed(self, x, y):
        """Menggambar biji apel"""
        # Biji berbentuk oval dengan detail
        pygame.draw.ellipse(self.screen, (60, 40, 20), (x - 12, y - 8, 24, 16))
        pygame.draw.ellipse(self.screen, (101, 67, 33), (x - 10, y - 6, 20, 12))
        pygame.draw.ellipse(self.screen, (139, 90, 43), (x - 8, y - 5, 16, 10))
        # Highlight
        pygame.draw.ellipse(self.screen, (160, 110, 60), (x - 6, y - 4, 8, 5))
    
    def draw_sprout(self, x, y):
        """Menggambar kecambah dengan akar"""
        sway = math.sin(self.plant_sway) * 2
        
        # Akar
        for i in range(3):
            offset = (i - 1) * 8
            root_end_x = x + offset + random.randint(-2, 2)
            root_end_y = y + 15 + random.randint(0, 8)
            pygame.draw.line(self.screen, (139, 90, 43),
                           (x, y + 5), (root_end_x, root_end_y), 2)
        
        # Batang
        pygame.draw.line(self.screen, self.LIGHT_GREEN, 
                        (x, y), (x + int(sway), y - 40), 5)
        
        # Daun kecil (kotiledon)
        leaf_left = [
            (x + int(sway), y - 40),
            (x + int(sway) - 12, y - 35),
            (x + int(sway) - 8, y - 32),
            (x + int(sway), y - 35)
        ]
        pygame.draw.polygon(self.screen, self.LEAF_GREEN, leaf_left)
        
        leaf_right = [
            (x + int(sway), y - 40),
            (x + int(sway) + 12, y - 35),
            (x + int(sway) + 8, y - 32),
            (x + int(sway), y - 35)
        ]
        pygame.draw.polygon(self.screen, self.LEAF_GREEN, leaf_right)
    
    def draw_apple_leaf(self, x, y, size, angle):
        """Menggambar daun apel dengan detail"""
        leaf_surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
        
        # Bentuk daun oval
        pygame.draw.ellipse(leaf_surf, self.GREEN, (5, 0, size * 2 - 10, size * 2))
        pygame.draw.ellipse(leaf_surf, self.LEAF_GREEN, (10, 5, size * 2 - 20, size * 2 - 10))
        
        # Urat daun
        center_x = size
        center_y = size
        pygame.draw.line(leaf_surf, self.DARK_GREEN, 
                        (center_x, 5), (center_x, size * 2 - 5), 2)
        
        # Urat samping
        for i in range(4):
            offset_y = 10 + i * 12
            pygame.draw.line(leaf_surf, self.DARK_GREEN,
                           (center_x, offset_y),
                           (center_x + 8, offset_y + 5), 1)
            pygame.draw.line(leaf_surf, self.DARK_GREEN,
                           (center_x, offset_y),
                           (center_x - 8, offset_y + 5), 1)
        
        rotated = pygame.transform.rotate(leaf_surf, angle)
        rect = rotated.get_rect(center=(int(x), int(y)))
        self.screen.blit(rotated, rect)
    
    def draw_young_leaves(self, x, y):
        """Menggambar daun muda"""
        sway = math.sin(self.plant_sway) * 3
        
        # Batang utama
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 60), 8)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 60), 6)
        
        # Daun-daun muda
        for i in range(4):
            leaf_y = y - 15 - (i * 12)
            leaf_sway = sway * (1 - i * 0.15)
            
            # Daun kiri
            self.draw_apple_leaf(x + int(leaf_sway) - 25, leaf_y, 20, -30)
            # Daun kanan
            self.draw_apple_leaf(x + int(leaf_sway) + 25, leaf_y, 20, 30)
    
    def draw_flower(self, x, y):
        """Menggambar pohon dengan bunga"""
        sway = math.sin(self.plant_sway) * 4
        
        # Batang
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 90), 12)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 90), 8)
        
        # Cabang-cabang
        branches = [
            (y - 30, -35, 40),
            (y - 50, 35, 45),
            (y - 70, -30, 35)
        ]
        
        for branch_y, angle, length in branches:
            rad = math.radians(angle)
            end_x = x + int(sway) + int(math.cos(rad) * length)
            end_y = branch_y + int(math.sin(rad) * length)
            pygame.draw.line(self.screen, self.TRUNK_BROWN,
                           (x + int(sway), branch_y),
                           (end_x, end_y), 6)
            
            # Bunga di ujung cabang
            for i in range(3):
                flower_x = end_x + random.randint(-10, 10)
                flower_y = end_y + random.randint(-10, 10)
                
                # Kelopak bunga (5 kelopak)
                for j in range(5):
                    petal_angle = (360 / 5) * j + self.flower_spin * 0.5
                    petal_rad = math.radians(petal_angle)
                    petal_x = flower_x + math.cos(petal_rad) * 8
                    petal_y = flower_y + math.sin(petal_rad) * 8
                    pygame.draw.circle(self.screen, self.PINK, 
                                     (int(petal_x), int(petal_y)), 5)
                
                # Pusat bunga
                pygame.draw.circle(self.screen, self.YELLOW, (flower_x, flower_y), 4)
                pygame.draw.circle(self.screen, (255, 255, 200), (flower_x, flower_y), 2)
        
        # Daun di batang utama
        for i in range(5):
            leaf_y = y - 20 - (i * 15)
            self.draw_apple_leaf(x + int(sway) - 20, leaf_y, 22, -20 - i * 5)
            self.draw_apple_leaf(x + int(sway) + 20, leaf_y, 22, 20 + i * 5)
    
    def draw_young_fruit(self, x, y):
        """Menggambar pohon dengan buah muda (hijau kecil)"""
        sway = math.sin(self.plant_sway) * 4
        
        # Batang
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 100), 14)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 100), 10)
        
        # Cabang dengan buah
        branches = [
            (y - 35, -40, 50),
            (y - 55, 40, 55),
            (y - 75, -35, 45),
            (y - 90, 30, 40)
        ]
        
        for branch_y, angle, length in branches:
            rad = math.radians(angle)
            end_x = x + int(sway) + int(math.cos(rad) * length)
            end_y = branch_y + int(math.sin(rad) * length)
            pygame.draw.line(self.screen, self.TRUNK_BROWN,
                           (x + int(sway), branch_y),
                           (end_x, end_y), 7)
            
            # Buah muda (hijau kecil)
            fruit_x = end_x + random.randint(-8, 8)
            fruit_y = end_y + 10
            
            # Tangkai buah
            pygame.draw.line(self.screen, self.DARK_BROWN,
                           (end_x, end_y), (fruit_x, fruit_y), 2)
            
            # Buah hijau kecil
            pygame.draw.circle(self.screen, self.LIGHT_GREEN, (fruit_x, fruit_y), 10)
            pygame.draw.circle(self.screen, (180, 255, 180), (fruit_x - 3, fruit_y - 3), 4)
        
        # Daun
        for i in range(6):
            leaf_y = y - 25 - (i * 13)
            self.draw_apple_leaf(x + int(sway) - 22, leaf_y, 24, -25)
            self.draw_apple_leaf(x + int(sway) + 22, leaf_y, 24, 25)
    
    def draw_ripe_fruit(self, x, y):
        """Menggambar pohon dengan buah matang (merah)"""
        sway = math.sin(self.plant_sway) * 4
        
        # Batang
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 110), 16)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 110), 12)
        
        # Cabang dengan buah matang
        self.apple_positions = []
        branches = [
            (y - 40, -42, 55),
            (y - 60, 42, 60),
            (y - 80, -38, 50),
            (y - 95, 35, 45)
        ]
        
        for idx, (branch_y, angle, length) in enumerate(branches):
            rad = math.radians(angle)
            end_x = x + int(sway) + int(math.cos(rad) * length)
            end_y = branch_y + int(math.sin(rad) * length)
            pygame.draw.line(self.screen, self.TRUNK_BROWN,
                           (x + int(sway), branch_y),
                           (end_x, end_y), 8)
            
            # Buah matang (merah)
            fruit_x = end_x + random.randint(-10, 10)
            fruit_y = end_y + 12
            
            self.apple_positions.append((fruit_x, fruit_y))
            
            # Tangkai buah
            pygame.draw.line(self.screen, self.DARK_BROWN,
                           (end_x, end_y), (fruit_x, fruit_y - 14), 3)
            
            # Apel merah
            pygame.draw.circle(self.screen, self.RED_APPLE, (fruit_x, fruit_y), 14)
            pygame.draw.circle(self.screen, self.LIGHT_RED, (fruit_x - 4, fruit_y - 4), 6)
            pygame.draw.circle(self.screen, (255, 255, 255), (fruit_x - 5, fruit_y - 5), 3)
        
        # Daun lebat
        for i in range(8):
            leaf_y = y - 30 - (i * 11)
            self.draw_apple_leaf(x + int(sway) - 25, leaf_y, 26, -30 + i * 3)
            self.draw_apple_leaf(x + int(sway) + 25, leaf_y, 26, 30 - i * 3)
    
    def draw_harvest_ready(self, x, y):
        """Menggambar pohon siap panen"""
        sway = math.sin(self.plant_sway) * 4
        
        # Batang besar
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 120), 18)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 120), 14)
        
        # Cabang dengan apel siap panen
        self.apple_positions = []
        branches = [
            (y - 45, -45, 60),
            (y - 65, 45, 65),
            (y - 85, -40, 55),
            (y - 100, 38, 50),
            (y - 115, -30, 45)
        ]
        
        for idx, (branch_y, angle, length) in enumerate(branches):
            rad = math.radians(angle)
            end_x = x + int(sway) + int(math.cos(rad) * length)
            end_y = branch_y + int(math.sin(rad) * length)
            pygame.draw.line(self.screen, self.TRUNK_BROWN,
                           (x + int(sway), branch_y),
                           (end_x, end_y), 9)
            
            # Apel siap dipanen
            fruit_x = end_x + random.randint(-12, 12)
            fruit_y = end_y + 15
            
            # Skip jika sudah dipanen
            if idx in [a['id'] for a in self.harvested_apples]:
                continue
            
            self.apple_positions.append((fruit_x, fruit_y, idx))
            
            # Tangkai
            pygame.draw.line(self.screen, self.DARK_BROWN,
                           (end_x, end_y), (fruit_x, fruit_y - 16), 3)
            
            # Apel merah mengkilap
            pygame.draw.circle(self.screen, self.RED_APPLE, (fruit_x, fruit_y), 16)
            pygame.draw.circle(self.screen, self.LIGHT_RED, (fruit_x - 5, fruit_y - 5), 7)
            pygame.draw.circle(self.screen, (255, 255, 255), (fruit_x - 6, fruit_y - 6), 4)
            
            # Daun kecil di tangkai
            pygame.draw.ellipse(self.screen, self.GREEN, 
                              (fruit_x - 8, fruit_y - 18, 10, 6))
        
        # Daun lebat dan hijau
        for i in range(10):
            leaf_y = y - 35 - (i * 10)
            self.draw_apple_leaf(x + int(sway) - 28, leaf_y, 28, -35 + i * 4)
            self.draw_apple_leaf(x + int(sway) + 28, leaf_y, 28, 35 - i * 4)
    
    def draw_plant(self):
        """Menggambar tanaman sesuai tahap"""
        center_x = self.width // 2
        soil_y = self.height - 250
        
        if self.current_stage == 0:
            self.draw_seed(center_x, soil_y + 20)
        elif self.current_stage == 1:
            self.draw_sprout(center_x, soil_y)
        elif self.current_stage == 2:
            self.draw_young_leaves(center_x, soil_y)
        elif self.current_stage == 3:
            self.draw_flower(center_x, soil_y)
        elif self.current_stage == 4:
            self.draw_young_fruit(center_x, soil_y)
        elif self.current_stage == 5:
            self.draw_ripe_fruit(center_x, soil_y)
        elif self.current_stage == 6:
            self.draw_harvest_ready(center_x, soil_y)
    
    def draw_fertilizer_bag(self):
        """Menggambar kantong pupuk"""
        x = self.fertilizer_bag['x']
        y = self.fertilizer_bag['y']
        w = self.fertilizer_bag['width']
        h = self.fertilizer_bag['height']
        
        # Bayangan
        pygame.draw.rect(self.screen, (50, 50, 50), (x + 5, y + 5, w, h), border_radius=10)
        
        # Kantong
        color = (160, 82, 45) if not self.fertilizer_bag['hover'] else (139, 69, 19)
        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=10)
        pygame.draw.rect(self.screen, (101, 67, 33), (x, y, w, h), 3, border_radius=10)
        
        # Label
        pygame.draw.rect(self.screen, (222, 184, 135), (x + 10, y + 20, w - 20, h - 40), border_radius=5)
        
        text = self.font_small.render("PUPUK", True, (101, 67, 33))
        self.screen.blit(text, (x + w // 2 - text.get_width() // 2, y + 35))
        
        # Partikel pupuk
        for particle in self.fertilizer_bag['particles']:
            pygame.draw.circle(self.screen, (139, 90, 43),
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
    
    def draw_ui(self):
        """Menggambar UI dan progress bars"""
        # Progress bar
        progress_bg = pygame.Rect(self.width // 2 - 200, 20, 400, 25)
        self.draw_rounded_rect(self.screen, (50, 50, 50), progress_bg, 12)
        
        if self.current_stage < len(self.stages) - 1:
            progress_width = int((self.growth_progress / self.stage_requirements[self.current_stage]) * 380)
            progress_fill = pygame.Rect(self.width // 2 - 190, 25, progress_width, 15)
            pygame.draw.rect(self.screen, (76, 175, 80), progress_fill, border_radius=8)
        
        pygame.draw.rect(self.screen, self.WHITE, progress_bg, 2, border_radius=12)
        
        # Stage name
        stage_text = self.font_stage.render(self.stages[self.current_stage], True, self.WHITE)
        self.screen.blit(stage_text, (self.width // 2 - stage_text.get_width() // 2, 55))
        
        # Level bars
        bar_x = 30
        bar_y = 120
        bar_width = 200
        bar_height = 25
        bar_spacing = 45
        
        levels = [
            ('💧 Air', self.water_level, self.WATER_BLUE),
            ('☀ Cahaya', self.sunlight_level, self.YELLOW),
            ('🌱 Pupuk', self.fertilizer_level, self.GREEN)
        ]
        
        for i, (label, level, color) in enumerate(levels):
            y = bar_y + (i * bar_spacing)
            
            label_text = self.font_button.render(label, True, self.WHITE)
            label_bg = pygame.Rect(bar_x - 5, y - 8, label_text.get_width() + 10, 35)
            self.draw_rounded_rect(self.screen, (0, 0, 0, 150), label_bg, 8)
            self.screen.blit(label_text, (bar_x, y))
            
            bar_bg = pygame.Rect(bar_x + 150, y, bar_width, bar_height)
            pygame.draw.rect(self.screen, (50, 50, 50), bar_bg, border_radius=12)
            
            fill_width = int((level / 100) * bar_width)
            if fill_width > 0:
                bar_fill = pygame.Rect(bar_x + 150, y, fill_width, bar_height)
                pygame.draw.rect(self.screen, color, bar_fill, border_radius=12)
            
            pygame.draw.rect(self.screen, self.WHITE, bar_bg, 2, border_radius=12)
            
            pct_text = self.font_small.render(f"{int(level)}%", True, self.WHITE)
            self.screen.blit(pct_text, (bar_x + 150 + bar_width + 10, y + 2))
        
        # Harvest button (hanya muncul saat stage panen)
        if self.current_stage == 6 and self.total_harvested < 5:
            harvest_btn = pygame.Rect(self.width // 2 - 100, self.height - 180, 200, 60)
            btn_color = (255, 140, 0) if self.harvest_button_hover else (255, 165, 0)
            self.draw_rounded_rect(self.screen, btn_color, harvest_btn, 15)
            pygame.draw.rect(self.screen, self.WHITE, harvest_btn, 3, border_radius=15)
            
            harvest_text = self.font_button.render("🍎 PANEN!", True, self.WHITE)
            self.screen.blit(harvest_text, 
                           (self.width // 2 - harvest_text.get_width() // 2, 
                            self.height - 165))
            
            count_text = self.font_small.render(f"{self.total_harvested}/5 buah", True, self.WHITE)
            self.screen.blit(count_text,
                           (self.width // 2 - count_text.get_width() // 2,
                            self.height - 135))
        
        # Message
        if self.message_timer > 0:
            msg_text = self.font_button.render(self.message, True, self.WHITE)
            msg_bg = pygame.Rect(self.width // 2 - msg_text.get_width() // 2 - 20,
                                self.height // 2 - 50, 
                                msg_text.get_width() + 40, 60)
            self.draw_rounded_rect(self.screen, (0, 0, 0, 200), msg_bg, 15)
            self.screen.blit(msg_text, 
                           (self.width // 2 - msg_text.get_width() // 2, 
                            self.height // 2 - 35))
        
        # Back button
        back_button = pygame.Rect(self.width - 150, self.height - 70, 120, 50)
        color = self.BUTTON_GREEN if not back_button.collidepoint(pygame.mouse.get_pos()) else (150, 200, 130)
        self.draw_rounded_rect(self.screen, color, back_button, 12)
        pygame.draw.rect(self.screen, self.WHITE, back_button, 2, border_radius=12)
        
        back_text = self.font_button.render("← Kembali", True, self.WHITE)
        self.screen.blit(back_text, (self.width - 90 - back_text.get_width() // 2, self.height - 57))
    
    def show_message(self, message):
        """Tampilkan pesan sementara"""
        self.message = message
        self.message_timer = 2.0
    
    def harvest_apple(self, mouse_pos):
        """Panen apel yang diklik"""
        if self.current_stage != 6:
            return
        
        if not hasattr(self, 'apple_positions'):
            return
        
        for fx, fy, apple_id in self.apple_positions:
            # Skip jika sudah dipanen
            if apple_id in [a['id'] for a in self.harvested_apples]:
                continue
            
            # Cek jarak klik dengan apel
            dist = math.sqrt((mouse_pos[0] - fx)**2 + (mouse_pos[1] - fy)**2)
            if dist < 20:
                # Animasi panen
                self.harvested_apples.append({
                    'id': apple_id,
                    'x': fx,
                    'y': fy,
                    'vx': random.uniform(-5, 5),
                    'vy': random.uniform(-12, -8),
                    'rotation': 0,
                    'rot_speed': random.uniform(-8, 8)
                })
                self.total_harvested += 1
                self.show_message(f"Apel dipanen! {self.total_harvested}/5")
                
                # Particle effect
                for _ in range(15):
                    self.particles.append({
                        'x': fx,
                        'y': fy,
                        'vx': random.uniform(-3, 3),
                        'vy': random.uniform(-5, -2),
                        'life': 1.0,
                        'color': self.RED_APPLE,
                        'size': random.randint(2, 5)
                    })
                
                # Cek apakah semua apel sudah dipanen
                if self.total_harvested >= 5:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
                    self.show_message("Selamat! Semua apel terpanen!")
                
                break
    
    def handle_event(self, event):
        """Handle input events"""
        # Timer untuk pindah ke halaman apresiasi
        if event.type == pygame.USEREVENT + 1:
            # Pindah ke halaman apresiasi dengan parameter plant_type
            self.scene_manager.change_scene("apresiasi", plant_type="apel")
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop timer
            return
        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            bag_rect = pygame.Rect(
                self.fertilizer_bag['x'],
                self.fertilizer_bag['y'],
                self.fertilizer_bag['width'],
                self.fertilizer_bag['height']
            )
            self.fertilizer_bag['hover'] = bag_rect.collidepoint(mouse_pos)
            
            # Harvest button hover
            if self.current_stage == 6 and self.total_harvested < 5:
                harvest_btn = pygame.Rect(self.width // 2 - 100, self.height - 180, 200, 60)
                self.harvest_button_hover = harvest_btn.collidepoint(mouse_pos)
            
            if self.cloud['dragging']:
                self.cloud['x'] = mouse_pos[0] - self.cloud['width'] // 2
                self.cloud['x'] = max(50, min(self.width - 200, self.cloud['x']))
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Cek klik apel untuk panen
            if self.current_stage == 6:
                self.harvest_apple(mouse_pos)
            
            # Cloud (hujan)
            cloud_rect = pygame.Rect(
                self.cloud['x'], self.cloud['y'],
                self.cloud['width'], self.cloud['height']
            )
            if cloud_rect.collidepoint(mouse_pos):
                self.cloud['dragging'] = True
                self.cloud['raining'] = True
            
            # Sun (cahaya)
            sun_dist = math.sqrt((mouse_pos[0] - self.sun['x'])**2 + 
                               (mouse_pos[1] - self.sun['y'])**2)
            if sun_dist < self.sun['radius'] + 30:
                self.sunlight_level = min(100, self.sunlight_level + 25)
                self.show_message("Cahaya matahari +25%!")
                self.sun['glow'] = 50
            
            # Fertilizer bag
            bag_rect = pygame.Rect(
                self.fertilizer_bag['x'],
                self.fertilizer_bag['y'],
                self.fertilizer_bag['width'],
                self.fertilizer_bag['height']
            )
            if bag_rect.collidepoint(mouse_pos):
                self.fertilizer_level = min(100, self.fertilizer_level + 25)
                self.show_message("Pupuk ditambahkan +25%!")
                
                for _ in range(15):
                    self.fertilizer_bag['particles'].append({
                        'x': mouse_pos[0],
                        'y': mouse_pos[1],
                        'vx': random.uniform(-3, 3),
                        'vy': random.uniform(-8, -3),
                        'life': 1.0,
                        'size': random.randint(2, 4)
                    })
            
            # Back button
            back_button = pygame.Rect(self.width - 150, self.height - 70, 120, 50)
            if back_button.collidepoint(mouse_pos):
                self.scene_manager.change_scene("pilih_buah")
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.cloud['dragging'] = False
            self.cloud['raining'] = False
            self.cloud['rain_drops'].clear()
    
    def update(self, dt):
        """Update logic dan animasi"""
        self.time += dt
        self.plant_sway += dt * 2
        self.flower_spin += dt * 30
        
        if self.message_timer > 0:
            self.message_timer -= dt
        
        # Update rain
        if self.cloud['raining']:
            if random.random() < 0.5:
                self.cloud['rain_drops'].append({
                    'x': self.cloud['x'] + random.uniform(20, self.cloud['width'] - 20),
                    'y': self.cloud['y'] + self.cloud['height'],
                    'vy': random.uniform(8, 12)
                })
            
            soil_y = self.height - 250
            for drop in self.cloud['rain_drops'][:]:
                drop['y'] += drop['vy']
                
                if drop['y'] >= soil_y:
                    self.water_level = min(100, self.water_level + 0.5)
                    self.cloud['rain_drops'].remove(drop)
                    
                    for _ in range(3):
                        self.particles.append({
                            'x': drop['x'],
                            'y': soil_y,
                            'vx': random.uniform(-2, 2),
                            'vy': random.uniform(-3, -1),
                            'life': 0.5,
                            'color': self.WATER_BLUE,
                            'size': 2
                        })
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Update fertilizer particles
        for particle in self.fertilizer_bag['particles'][:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.fertilizer_bag['particles'].remove(particle)
        
        # Update harvested apples animation
        for apple in self.harvested_apples[:]:
            apple['x'] += apple['vx']
            apple['y'] += apple['vy']
            apple['vy'] += 0.5
            apple['rotation'] += apple['rot_speed']
            
            if apple['y'] > self.height + 50:
                self.harvested_apples.remove(apple)
        
        if self.sun['glow'] > 0:
            self.sun['glow'] = max(0, self.sun['glow'] - dt * 50)
        
        # Growth logic
        if self.current_stage < len(self.stages) - 1:
            if (self.water_level > 20 and 
                self.sunlight_level > 20 and 
                self.fertilizer_level > 20):
                
                growth_rate = 4
                self.growth_progress += growth_rate * dt
                
                self.water_level = max(0, self.water_level - self.water_consumption * dt)
                self.sunlight_level = max(0, self.sunlight_level - self.sunlight_consumption * dt)
                self.fertilizer_level = max(0, self.fertilizer_level - self.fertilizer_consumption * dt)
                
                if self.growth_progress >= self.stage_requirements[self.current_stage]:
                    self.current_stage += 1
                    self.growth_progress = 0
                    self.show_message(f"Tumbuh: {self.stages[self.current_stage]}!")
            else:
                if self.water_level < 10:
                    self.show_message("Butuh air!")
                elif self.sunlight_level < 10:
                    self.show_message("Butuh cahaya!")
                elif self.fertilizer_level < 10:
                    self.show_message("Butuh pupuk!")
        else:
            self.water_level = max(0, self.water_level - dt * 0.5)
            self.sunlight_level = max(0, self.sunlight_level - dt * 0.5)
            self.fertilizer_level = max(0, self.fertilizer_level - dt * 0.5)
    
    def draw(self):
        """Render scene"""
        self.screen.blit(self.background, (0, 0))
        
        self.draw_sky_elements()
        self.draw_soil()
        self.draw_plant()
        self.draw_fertilizer_bag()
        
        # Draw harvested apples (animasi jatuh)
        for apple in self.harvested_apples:
            ax, ay = int(apple['x']), int(apple['y'])
            
            apple_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(apple_surf, self.RED_APPLE, (20, 20), 16)
            pygame.draw.circle(apple_surf, self.LIGHT_RED, (15, 15), 7)
            
            rotated = pygame.transform.rotate(apple_surf, apple['rotation'])
            rect = rotated.get_rect(center=(ax, ay))
            self.screen.blit(rotated, rect)
        
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle['color'],
                             (int(particle['x']), int(particle['y'])),
                             particle['size'])
        
        self.draw_ui()
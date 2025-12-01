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
        self.GREEN = (34, 139, 34)
        self.DARK_GREEN = (0, 100, 0)
        self.LEAF_GREEN = (50, 205, 50)
        self.RED = (220, 20, 60)
        self.LIGHT_RED = (255, 105, 180)
        self.PINK = (255, 192, 203)
        self.YELLOW = (255, 223, 0)
        self.WHITE = (255, 255, 255)
        self.BUTTON_GREEN = (126, 176, 105)
        self.WATER_BLUE = (135, 206, 250)
        self.CLOUD_WHITE = (240, 248, 255)
        self.SKY_BLUE = (135, 206, 235)
        
        # Tahapan pertumbuhan
        self.stages = [
            "Biji",
            "Kecambah", 
            "Daun Muda",
            "Vegetatif",
            "Bunga",
            "Buah Muda",
            "Buah Matang",
            "Siap Panen"
        ]
        
        self.current_stage = 0
        self.growth_progress = 0
        self.stage_requirements = [15, 25, 35, 45, 55, 65, 75, 85]
        
        # Faktor pertumbuhan
        self.water_level = 30
        self.sunlight_level = 30
        self.fertilizer_level = 30
        
        # Kebutuhan per detik
        self.water_consumption = 3
        self.sunlight_consumption = 2.5
        self.fertilizer_consumption = 2
        
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
        self.harvest_ready = False
        self.harvest_button_hover = False
        self.harvested_fruits = []  # For animation
        self.total_harvested = 0
        
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
        glow_intensity = int(self.sun['glow'])
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
        
        # Tekstur tanah (batu-batu kecil)
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
        """Menggambar biji dengan detail"""
        pygame.draw.ellipse(self.screen, (60, 40, 20), (x - 20, y - 5, 40, 15))
        pygame.draw.ellipse(self.screen, (101, 67, 33), (x - 12, y - 8, 24, 16))
        pygame.draw.ellipse(self.screen, (139, 90, 43), (x - 10, y - 6, 20, 12))
        pygame.draw.line(self.screen, (101, 67, 33), (x - 8, y), (x + 8, y), 2)
        pygame.draw.ellipse(self.screen, (160, 110, 60), (x - 6, y - 4, 8, 5))
    
    def draw_sprout(self, x, y):
        """Menggambar kecambah dengan akar"""
        sway = math.sin(self.plant_sway) * 2
        
        for i in range(3):
            offset = (i - 1) * 10
            root_end_x = x + offset + random.randint(-3, 3)
            root_end_y = y + 20 + random.randint(0, 10)
            pygame.draw.line(self.screen, (139, 90, 43),
                           (x, y + 5), (root_end_x, root_end_y), 2)
        
        pygame.draw.line(self.screen, (144, 238, 144), 
                        (x, y), (x + int(sway), y - 35), 4)
        
        leaf_left = [(x + int(sway) - 15, y - 30), (x + int(sway) - 8, y - 35), (x + int(sway), y - 32)]
        pygame.draw.polygon(self.screen, self.LEAF_GREEN, leaf_left)
        pygame.draw.line(self.screen, self.DARK_GREEN, (x + int(sway), y - 32), (x + int(sway) - 12, y - 31), 1)
        
        leaf_right = [(x + int(sway) + 15, y - 30), (x + int(sway) + 8, y - 35), (x + int(sway), y - 32)]
        pygame.draw.polygon(self.screen, self.LEAF_GREEN, leaf_right)
        pygame.draw.line(self.screen, self.DARK_GREEN, (x + int(sway), y - 32), (x + int(sway) + 12, y - 31), 1)
    
    def draw_young_leaves(self, x, y):
        """Menggambar daun muda"""
        sway = math.sin(self.plant_sway) * 3
        pygame.draw.line(self.screen, self.GREEN, (x, y), (x + int(sway), y - 50), 6)
        
        for i in range(2):
            leaf_y = y - 20 - (i * 15)
            leaf_sway = sway * (1 - i * 0.2)
            
            for j in range(4):
                lx = x + int(leaf_sway) - 25 + j * 5
                ly = leaf_y - 5 + (j % 2) * 3
                lx2 = x + int(leaf_sway) - 20 + j * 5
                ly2 = leaf_y - 2 + ((j + 1) % 2) * 3
                pygame.draw.line(self.screen, self.GREEN, (lx, ly), (lx2, ly2), 3)
            
            pygame.draw.ellipse(self.screen, self.LEAF_GREEN, (x + int(leaf_sway) - 28, leaf_y - 8, 30, 18))
            pygame.draw.line(self.screen, self.DARK_GREEN, (x + int(leaf_sway), leaf_y), (x + int(leaf_sway) - 25, leaf_y), 2)
            
            for j in range(4):
                rx = x + int(leaf_sway) + 25 - j * 5
                ry = leaf_y - 5 + (j % 2) * 3
                rx2 = x + int(leaf_sway) + 20 - j * 5
                ry2 = leaf_y - 2 + ((j + 1) % 2) * 3
                pygame.draw.line(self.screen, self.GREEN, (rx, ry), (rx2, ry2), 3)
            
            pygame.draw.ellipse(self.screen, self.LEAF_GREEN, (x + int(leaf_sway), leaf_y - 8, 30, 18))
            pygame.draw.line(self.screen, self.DARK_GREEN, (x + int(leaf_sway), leaf_y), (x + int(leaf_sway) + 25, leaf_y), 2)
    
    def draw_vegetative(self, x, y):
        """Menggambar fase vegetatif lengkap"""
        sway = math.sin(self.plant_sway) * 4
        pygame.draw.line(self.screen, self.DARK_GREEN, (x, y), (x + int(sway), y - 70), 8)
        pygame.draw.line(self.screen, self.GREEN, (x, y), (x + int(sway), y - 70), 6)
        
        for i in range(6):
            leaf_y = y - 15 - (i * 12)
            leaf_x = x + int(sway * (1 - i * 0.1))
            size_factor = 1 + i * 0.1
            
            self.draw_strawberry_leaf(leaf_x - 30 * size_factor, leaf_y, 35 * size_factor, -20 - i * 5)
            self.draw_strawberry_leaf(leaf_x + 30 * size_factor, leaf_y, 35 * size_factor, 20 + i * 5)
    
    def draw_strawberry_leaf(self, x, y, size, angle):
        """Menggambar daun stroberi dengan detail serrations"""
        leaf_surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
        
        points = []
        for i in range(20):
            a = (360 / 20) * i
            rad = math.radians(a)
            r = size * (0.8 if i % 2 == 0 else 1.0)
            px = size + math.cos(rad) * r
            py = size + math.sin(rad) * r * 0.7
            points.append((px, py))
        
        pygame.draw.polygon(leaf_surf, self.GREEN, points)
        pygame.draw.polygon(leaf_surf, self.LEAF_GREEN, [(p[0] + 2, p[1] + 2) for p in points[:-5]])
        
        center = size
        for i in range(5):
            vein_angle = -60 + i * 30
            vein_rad = math.radians(vein_angle)
            vein_x = center + math.cos(vein_rad) * size * 0.8
            vein_y = center + math.sin(vein_rad) * size * 0.6
            pygame.draw.line(leaf_surf, self.DARK_GREEN, (center, center), (vein_x, vein_y), 2)
        
        rotated = pygame.transform.rotate(leaf_surf, angle)
        rect = rotated.get_rect(center=(int(x), int(y)))
        self.screen.blit(rotated, rect)
    
    def draw_flower(self, x, y):
        """Menggambar bunga stroberi yang realistis"""
        self.draw_vegetative(x, y)
        
        sway = math.sin(self.plant_sway) * 4
        flower_x = x + int(sway)
        flower_y = y - 85
        
        pygame.draw.line(self.screen, self.GREEN, (x + int(sway), y - 70), (flower_x, flower_y + 5), 4)
        
        for i in range(5):
            angle = (360 / 5) * i + self.flower_spin * 0.5
            rad = math.radians(angle)
            sepal_x = flower_x + math.cos(rad) * 18
            sepal_y = flower_y + math.sin(rad) * 18
            
            sepal_points = [
                (flower_x, flower_y),
                (sepal_x, sepal_y),
                (sepal_x + math.cos(rad + 0.3) * 8, sepal_y + math.sin(rad + 0.3) * 8)
            ]
            pygame.draw.polygon(self.screen, self.DARK_GREEN, sepal_points)
        
        for i in range(5):
            angle = (360 / 5) * i + self.flower_spin
            rad = math.radians(angle)
            petal_x = flower_x + math.cos(rad) * 16
            petal_y = flower_y + math.sin(rad) * 16
            
            pygame.draw.circle(self.screen, self.WHITE, (int(petal_x - 3), int(petal_y - 3)), 8)
            pygame.draw.circle(self.screen, self.WHITE, (int(petal_x + 3), int(petal_y - 3)), 8)
            pygame.draw.circle(self.screen, self.PINK, (int(petal_x), int(petal_y)), 7)
        
        pygame.draw.circle(self.screen, self.YELLOW, (flower_x, flower_y), 10)
        pygame.draw.circle(self.screen, (255, 255, 150), (flower_x, flower_y), 7)
        
        for i in range(8):
            angle = (360 / 8) * i
            rad = math.radians(angle)
            stamen_x = flower_x + math.cos(rad) * 5
            stamen_y = flower_y + math.sin(rad) * 5
            pygame.draw.circle(self.screen, (255, 200, 0), (int(stamen_x), int(stamen_y)), 2)
    
    def draw_young_fruit(self, x, y):
        """Menggambar buah muda (hijau)"""
        self.draw_vegetative(x, y - 10)
        
        sway = math.sin(self.plant_sway) * 4
        fruit_x = x + int(sway)
        fruit_y = y - 95
        
        pygame.draw.line(self.screen, self.GREEN, (fruit_x, y - 70), (fruit_x, fruit_y + 20), 4)
        
        for i in range(5):
            angle = (360 / 5) * i - 90
            rad = math.radians(angle)
            leaf_x = fruit_x + math.cos(rad) * 14
            leaf_y = fruit_y + 15 + math.sin(rad) * 14
            
            leaf_points = [
                (fruit_x, fruit_y + 15),
                (int(leaf_x), int(leaf_y)),
                (fruit_x + int(math.cos(rad + 0.5) * 8), fruit_y + 15 + int(math.sin(rad + 0.5) * 8))
            ]
            pygame.draw.polygon(self.screen, self.DARK_GREEN, leaf_points)
        
        pygame.draw.circle(self.screen, (144, 238, 144), (fruit_x - 8, fruit_y + 20), 12)
        pygame.draw.circle(self.screen, (144, 238, 144), (fruit_x + 8, fruit_y + 20), 12)
        pygame.draw.polygon(self.screen, (144, 238, 144), [
            (fruit_x - 15, fruit_y + 20),
            (fruit_x, fruit_y + 42),
            (fruit_x + 15, fruit_y + 20)
        ])
        
        pygame.draw.circle(self.screen, (200, 255, 200), (fruit_x - 5, fruit_y + 18), 6)
        
        random.seed(42)
        for i in range(15):
            seed_x = fruit_x + random.randint(-12, 12)
            seed_y = fruit_y + 20 + random.randint(-8, 20)
            if -10 < seed_x - fruit_x < 10:
                pygame.draw.circle(self.screen, (255, 255, 200), (seed_x, seed_y), 1)
        random.seed()
    
    def draw_ripe_fruit(self, x, y):
        """Menggambar buah matang (merah cerah)"""
        self.draw_vegetative(x, y - 10)
        
        sway = math.sin(self.plant_sway) * 4
        fruit_x = x + int(sway)
        fruit_y = y - 95
        
        pygame.draw.line(self.screen, self.GREEN, (fruit_x, y - 70), (fruit_x, fruit_y + 20), 5)
        
        for i in range(6):
            angle = (360 / 6) * i - 90
            rad = math.radians(angle)
            leaf_x = fruit_x + math.cos(rad) * 18
            leaf_y = fruit_y + 15 + math.sin(rad) * 18
            
            leaf_points = [
                (fruit_x, fruit_y + 15),
                (int(leaf_x), int(leaf_y)),
                (fruit_x + int(math.cos(rad + 0.5) * 10), fruit_y + 15 + int(math.sin(rad + 0.5) * 10))
            ]
            pygame.draw.polygon(self.screen, self.DARK_GREEN, leaf_points)
            pygame.draw.polygon(self.screen, self.GREEN, [
                (fruit_x, fruit_y + 15),
                (int(leaf_x * 0.7 + fruit_x * 0.3), int(leaf_y * 0.7 + (fruit_y + 15) * 0.3)),
                (fruit_x, fruit_y + 17)
            ])
        
        pygame.draw.circle(self.screen, self.RED, (fruit_x - 10, fruit_y + 23), 16)
        pygame.draw.circle(self.screen, self.RED, (fruit_x + 10, fruit_y + 23), 16)
        pygame.draw.polygon(self.screen, self.RED, [
            (fruit_x - 20, fruit_y + 23),
            (fruit_x, fruit_y + 50),
            (fruit_x + 20, fruit_y + 23)
        ])
        
        pygame.draw.circle(self.screen, self.LIGHT_RED, (fruit_x - 6, fruit_y + 20), 10)
        pygame.draw.circle(self.screen, (255, 255, 255), (fruit_x - 8, fruit_y + 18), 4)
        
        random.seed(42)
        for i in range(25):
            seed_x = fruit_x + random.randint(-15, 15)
            seed_y = fruit_y + 20 + random.randint(-8, 28)
            
            dist_from_center = abs(seed_x - fruit_x)
            if seed_y < fruit_y + 35:
                if dist_from_center < 16:
                    pygame.draw.ellipse(self.screen, self.YELLOW, (seed_x - 2, seed_y - 1, 4, 3))
                    pygame.draw.ellipse(self.screen, (255, 255, 150), (seed_x - 1, seed_y, 2, 1))
            else:
                max_dist = 20 * (1 - (seed_y - fruit_y - 35) / 15)
                if dist_from_center < max_dist:
                    pygame.draw.ellipse(self.screen, self.YELLOW, (seed_x - 2, seed_y - 1, 4, 3))
                    pygame.draw.ellipse(self.screen, (255, 255, 150), (seed_x - 1, seed_y, 2, 1))
        random.seed()
    
    def draw_harvest_ready(self, x, y):
        """Menggambar tanaman siap panen dengan beberapa buah"""
        sway = math.sin(self.plant_sway) * 4
        
        pygame.draw.line(self.screen, self.DARK_GREEN, (x, y), (x + int(sway), y - 70), 8)
        
        for i in range(5):
            leaf_y = y - 15 - (i * 12)
            leaf_x = x + int(sway * (1 - i * 0.1))
            size_factor = 1 + i * 0.1
            
            self.draw_strawberry_leaf(leaf_x - 30 * size_factor, leaf_y, 35 * size_factor, -20 - i * 5)
            self.draw_strawberry_leaf(leaf_x + 30 * size_factor, leaf_y, 35 * size_factor, 20 + i * 5)
        
        # 3 buah stroberi matang yang bisa diklik
        self.fruit_positions = [
            (x + int(sway) - 40, y - 50),
            (x + int(sway), y - 80),
            (x + int(sway) + 35, y - 55)
        ]
        
        for i, (fx, fy) in enumerate(self.fruit_positions):
            # Skip jika sudah dipanen
            if i in [f['id'] for f in self.harvested_fruits]:
                continue
                
            pygame.draw.line(self.screen, self.GREEN, (fx, fy - 5), (fx, fy + 10), 3)
            
            for j in range(5):
                angle = (360 / 5) * j - 90
                rad = math.radians(angle)
                leaf_x = fx + math.cos(rad) * 12
                leaf_y = fy + 10 + math.sin(rad) * 12
                pygame.draw.polygon(self.screen, self.DARK_GREEN, [
                    (fx, fy + 10),
                    (int(leaf_x), int(leaf_y)),
                    (fx, fy + 12)
                ])
            
            pygame.draw.circle(self.screen, self.RED, (fx - 7, fy + 15), 11)
            pygame.draw.circle(self.screen, self.RED, (fx + 7, fy + 15), 11)
            pygame.draw.polygon(self.screen, self.RED, [
                (fx - 14, fy + 15),
                (fx, fy + 35),
                (fx + 14, fy + 15)
            ])
            
            pygame.draw.circle(self.screen, self.LIGHT_RED, (fx - 4, fy + 13), 6)
            
            random.seed(42 + int(fx))
            for j in range(15):
                sx = fx + random.randint(-10, 10)
                sy = fy + 15 + random.randint(-5, 18)
                pygame.draw.circle(self.screen, self.YELLOW, (sx, sy), 1)
            random.seed()
    
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
            self.draw_vegetative(center_x, soil_y)
        elif self.current_stage == 4:
            self.draw_flower(center_x, soil_y)
        elif self.current_stage == 5:
            self.draw_young_fruit(center_x, soil_y)
        elif self.current_stage == 6:
            self.draw_ripe_fruit(center_x, soil_y)
        elif self.current_stage == 7:
            self.draw_harvest_ready(center_x, soil_y)
    
    def draw_fertilizer_bag(self):
        """Menggambar kantong pupuk"""
        x = self.fertilizer_bag['x']
        y = self.fertilizer_bag['y']
        w = self.fertilizer_bag['width']
        h = self.fertilizer_bag['height']
        
        pygame.draw.rect(self.screen, (50, 50, 50), (x + 5, y + 5, w, h), border_radius=10)
        
        color = (160, 82, 45) if not self.fertilizer_bag['hover'] else (139, 69, 19)
        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=10)
        pygame.draw.rect(self.screen, (101, 67, 33), (x, y, w, h), 3, border_radius=10)
        
        pygame.draw.rect(self.screen, (222, 184, 135), (x + 10, y + 20, w - 20, h - 40), border_radius=5)
        
        text = self.font_small.render("PUPUK", True, (101, 67, 33))
        self.screen.blit(text, (x + w // 2 - text.get_width() // 2, y + 35))
        
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
            ('☀️ Cahaya', self.sunlight_level, self.YELLOW),
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
        
        # Harvest button (hanya muncul saat siap panen)
        if self.current_stage == 7 and self.total_harvested < 3:
            harvest_btn = pygame.Rect(self.width // 2 - 100, self.height - 180, 200, 60)
            btn_color = (255, 140, 0) if self.harvest_button_hover else (255, 165, 0)
            self.draw_rounded_rect(self.screen, btn_color, harvest_btn, 15)
            pygame.draw.rect(self.screen, self.WHITE, harvest_btn, 3, border_radius=15)
            
            harvest_text = self.font_button.render("🍓 PANEN!", True, self.WHITE)
            self.screen.blit(harvest_text, 
                           (self.width // 2 - harvest_text.get_width() // 2, 
                            self.height - 165))
            
            count_text = self.font_small.render(f"{self.total_harvested}/3 buah", True, self.WHITE)
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
    
    def harvest_fruit(self, mouse_pos):
        """Panen buah yang diklik"""
        if self.current_stage != 7:
            return
        
        for i, (fx, fy) in enumerate(self.fruit_positions):
            # Skip jika sudah dipanen
            if i in [f['id'] for f in self.harvested_fruits]:
                continue
            
            # Cek jarak klik dengan buah
            dist = math.sqrt((mouse_pos[0] - fx)**2 + (mouse_pos[1] - fy)**2)
            if dist < 30:
                # Animasi panen
                self.harvested_fruits.append({
                    'id': i,
                    'x': fx,
                    'y': fy,
                    'vx': random.uniform(-5, 5),
                    'vy': random.uniform(-15, -10),
                    'rotation': 0,
                    'rot_speed': random.uniform(-10, 10)
                })
                self.total_harvested += 1
                self.show_message(f"Buah dipanen! {self.total_harvested}/3")
                
                # Particle effect
                for _ in range(20):
                    self.particles.append({
                        'x': fx,
                        'y': fy,
                        'vx': random.uniform(-4, 4),
                        'vy': random.uniform(-6, -2),
                        'life': 1.0,
                        'color': self.RED,
                        'size': random.randint(2, 5)
                    })
                
                # Cek apakah semua buah sudah dipanen
                if self.total_harvested >= 3:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # Timer untuk pindah scene
                    self.show_message("Selamat! Semua buah terpanen!")
                
                break
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.USEREVENT + 1:
            # Pindah ke halaman apresiasi setelah semua buah dipanen
            self.scene_manager.change_scene("apresiasi")
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop timer
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            bag_rect = pygame.Rect(
                self.fertilizer_bag['x'],
                self.fertilizer_bag['y'],
                self.fertilizer_bag['width'],
                self.fertilizer_bag['height']
            )
            self.fertilizer_bag['hover'] = bag_rect.collidepoint(mouse_pos)
            
            # Harvest button hover
            if self.current_stage == 7 and self.total_harvested < 3:
                harvest_btn = pygame.Rect(self.width // 2 - 100, self.height - 180, 200, 60)
                self.harvest_button_hover = harvest_btn.collidepoint(mouse_pos)
            
            if self.cloud['dragging']:
                self.cloud['x'] = mouse_pos[0] - self.cloud['width'] // 2
                self.cloud['x'] = max(50, min(self.width - 200, self.cloud['x']))
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Cek klik buah untuk panen
            if self.current_stage == 7:
                self.harvest_fruit(mouse_pos)
            
            cloud_rect = pygame.Rect(
                self.cloud['x'], self.cloud['y'],
                self.cloud['width'], self.cloud['height']
            )
            if cloud_rect.collidepoint(mouse_pos):
                self.cloud['dragging'] = True
                self.cloud['raining'] = True
            
            sun_dist = math.sqrt((mouse_pos[0] - self.sun['x'])**2 + 
                               (mouse_pos[1] - self.sun['y'])**2)
            if sun_dist < self.sun['radius'] + 30:
                self.sunlight_level = min(100, self.sunlight_level + 25)
                self.show_message("Cahaya matahari +25%!")
                self.sun['glow'] = 50
            
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
        
        # Update harvested fruits animation
        for fruit in self.harvested_fruits[:]:
            fruit['x'] += fruit['vx']
            fruit['y'] += fruit['vy']
            fruit['vy'] += 0.5  # Gravity
            fruit['rotation'] += fruit['rot_speed']
            
            # Remove jika keluar layar
            if fruit['y'] > self.height + 50:
                self.harvested_fruits.remove(fruit)
        
        if self.sun['glow'] > 0:
            self.sun['glow'] = max(0, self.sun['glow'] - dt * 50)
        
        # Growth logic
        if self.current_stage < len(self.stages) - 1:
            if (self.water_level > 20 and 
                self.sunlight_level > 20 and 
                self.fertilizer_level > 20):
                
                growth_rate = 5
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
        
        # Draw harvested fruits (animasi jatuh)
        for fruit in self.harvested_fruits:
            fx, fy = int(fruit['x']), int(fruit['y'])
            
            # Gambar buah yang jatuh dengan rotasi
            fruit_surf = pygame.Surface((40, 60), pygame.SRCALPHA)
            pygame.draw.circle(fruit_surf, self.RED, (13, 20), 11)
            pygame.draw.circle(fruit_surf, self.RED, (27, 20), 11)
            pygame.draw.polygon(fruit_surf, self.RED, [(6, 20), (20, 47), (34, 20)])
            
            rotated = pygame.transform.rotate(fruit_surf, fruit['rotation'])
            rect = rotated.get_rect(center=(fx, fy))
            self.screen.blit(rotated, rect)
        
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle['color'],
                             (int(particle['x']), int(particle['y'])),
                             particle['size'])
        
        self.draw_ui()
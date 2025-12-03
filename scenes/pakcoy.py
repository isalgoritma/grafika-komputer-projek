import pygame
import math
import random
import os

class GrowthPakcoy:
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
        
        # Warna realistis untuk pakcoy
        self.SOIL_BROWN = (101, 67, 33)
        self.SOIL_DARK = (76, 50, 25)
        self.PAKCOY_GREEN = (144, 238, 144)  # Hijau muda pakcoy
        self.DARK_GREEN = (34, 139, 34)
        self.LIGHT_GREEN = (200, 255, 200)
        self.STEM_WHITE = (245, 255, 250)  # Batang putih pakcoy
        self.STEM_LIGHT = (255, 255, 255)
        self.VEIN_GREEN = (100, 200, 100)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 223, 0)
        self.BUTTON_GREEN = (126, 176, 105)
        self.WATER_BLUE = (135, 206, 250)
        self.CLOUD_WHITE = (240, 248, 255)
        
        # Tahapan pertumbuhan pakcoy (30-45 hari)
        self.stages = [
            "Biji",
            "Kecambah",
            "2 Daun Sejati",
            "4-6 Daun",
            "Vegetatif Penuh",
            "Siap Panen"
        ]
        
        self.current_stage = 0
        self.growth_progress = 0
        self.stage_requirements = [12, 20, 30, 40, 50, 60]
        
        # Faktor pertumbuhan
        self.water_level = 35
        self.sunlight_level = 35
        self.fertilizer_level = 35
        
        # Kebutuhan per detik
        self.water_consumption = 3.5
        self.sunlight_consumption = 2.5
        self.fertilizer_consumption = 2.5
        
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
        self.harvest_complete = False
        self.harvest_animation = 0
        
        # Particle effects
        self.particles = []
        
        # Animation
        self.plant_sway = 0
        self.leaf_wave = 0
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
        """Menggambar biji pakcoy yang sangat kecil"""
        # Biji pakcoy sangat kecil, bulat, coklat kemerahan
        pygame.draw.circle(self.screen, (101, 67, 33), (x, y), 6)
        pygame.draw.circle(self.screen, (139, 90, 43), (x, y), 4)
        pygame.draw.circle(self.screen, (160, 110, 60), (x - 1, y - 1), 2)
    
    def draw_sprout(self, x, y):
        """Menggambar kecambah dengan dua kotiledon"""
        sway = math.sin(self.plant_sway) * 1.5
        
        # Akar kecil
        for i in range(3):
            offset = (i - 1) * 8
            root_end_x = x + offset + random.randint(-2, 2)
            root_end_y = y + 15 + random.randint(0, 8)
            pygame.draw.line(self.screen, (160, 110, 60),
                           (x, y + 3), (root_end_x, root_end_y), 2)
        
        # Batang kecambah
        pygame.draw.line(self.screen, (200, 255, 200), 
                        (x, y), (x + int(sway), y - 30), 3)
        
        # Kotiledon (daun embrio) - bulat kecil
        leaf_left = [(x + int(sway) - 12, y - 28), 
                     (x + int(sway) - 6, y - 32), 
                     (x + int(sway), y - 28)]
        pygame.draw.polygon(self.screen, self.PAKCOY_GREEN, leaf_left)
        pygame.draw.polygon(self.screen, self.LIGHT_GREEN, 
                          [(x + int(sway) - 10, y - 29), 
                           (x + int(sway) - 7, y - 31), 
                           (x + int(sway), y - 28)])
        
        leaf_right = [(x + int(sway) + 12, y - 28), 
                      (x + int(sway) + 6, y - 32), 
                      (x + int(sway), y - 28)]
        pygame.draw.polygon(self.screen, self.PAKCOY_GREEN, leaf_right)
        pygame.draw.polygon(self.screen, self.LIGHT_GREEN, 
                          [(x + int(sway) + 10, y - 29), 
                           (x + int(sway) + 7, y - 31), 
                           (x + int(sway), y - 28)])
    
    def draw_pakcoy_leaf(self, x, y, width, height, angle_offset=0, is_mature=False):
        """Menggambar satu helai daun pakcoy yang realistis - daun oval dengan batang putih"""
        # Hitung rotasi berdasarkan offset sudut
        angle_rad = math.radians(angle_offset)
        
        # Panjang batang putih (petiole)
        stem_length = height * 0.55
        
        # Posisi ujung batang (tempat daun mulai)
        stem_end_x = x + math.sin(angle_rad) * stem_length * 0.3
        stem_end_y = y - math.cos(angle_rad) * stem_length
        
        # GAMBAR BATANG PUTIH
        stem_width = 8 if is_mature else 5
        
        # Batang dengan gradient (lebih lebar di bawah)
        for i in range(int(stem_length)):
            progress = i / stem_length
            current_width = stem_width * (1.2 - progress * 0.4)
            
            px = x + math.sin(angle_rad) * i * 0.3
            py = y - math.cos(angle_rad) * i
            
            # Shadow
            pygame.draw.circle(self.screen, (220, 230, 220), 
                             (int(px) + 1, int(py) + 1), int(current_width // 2))
            # Batang putih
            pygame.draw.circle(self.screen, self.STEM_WHITE, 
                             (int(px), int(py)), int(current_width // 2))
            
            # Highlight di tengah
            if i % 2 == 0:
                pygame.draw.circle(self.screen, self.STEM_LIGHT,
                                 (int(px) - 1, int(py)), int(current_width // 4))
        
        # GAMBAR DAUN HIJAU (blade) - bentuk oval lebar
        leaf_width = width
        leaf_height = height * 0.55
        
        # Hitung posisi daun dengan rotasi
        leaf_points = []
        num_points = 20
        
        for i in range(num_points):
            angle = (math.pi * 2 * i / num_points)
            
            # Bentuk oval yang lebih lebar
            local_x = math.cos(angle) * leaf_width * 0.5
            local_y = math.sin(angle) * leaf_height * 0.5
            
            # Rotasi sesuai angle_offset
            rotated_x = local_x * math.cos(angle_rad) - local_y * math.sin(angle_rad)
            rotated_y = local_x * math.sin(angle_rad) + local_y * math.cos(angle_rad)
            
            leaf_points.append((
                stem_end_x + rotated_x,
                stem_end_y + rotated_y - leaf_height * 0.3
            ))
        
        # Shadow daun
        shadow_points = [(p[0] + 2, p[1] + 2) for p in leaf_points]
        pygame.draw.polygon(self.screen, (60, 120, 60), shadow_points)
        
        # Outline daun gelap
        pygame.draw.polygon(self.screen, self.DARK_GREEN, leaf_points)
        
        # Daun hijau muda
        inner_points = []
        for i, p in enumerate(leaf_points):
            center_x = stem_end_x
            center_y = stem_end_y - leaf_height * 0.3
            inner_points.append((
                p[0] + (center_x - p[0]) * 0.1,
                p[1] + (center_y - p[1]) * 0.1
            ))
        pygame.draw.polygon(self.screen, self.PAKCOY_GREEN, inner_points)
        
        # Highlight area di tengah daun
        highlight_points = []
        for i, p in enumerate(leaf_points):
            center_x = stem_end_x
            center_y = stem_end_y - leaf_height * 0.3
            if len(leaf_points) // 4 < i < len(leaf_points) * 3 // 4:
                highlight_points.append((
                    p[0] + (center_x - p[0]) * 0.5,
                    p[1] + (center_y - p[1]) * 0.5
                ))
        if len(highlight_points) > 2:
            pygame.draw.polygon(self.screen, self.LIGHT_GREEN, highlight_points)
        
        # Urat tengah daun
        pygame.draw.line(self.screen, (100, 180, 100),
                       (int(x), int(y)),
                       (int(stem_end_x), int(stem_end_y - leaf_height * 0.4)), 2)
    
    def draw_two_true_leaves(self, x, y):
        """Menggambar 2 daun sejati pertama"""
        sway = math.sin(self.plant_sway) * 2
        
        # Batang pusat sangat pendek
        pygame.draw.line(self.screen, self.STEM_WHITE, 
                        (x, y), (x + int(sway), y - 15), 5)
        
        # 2 daun sejati kecil
        leaf_y = y - 20
        leaf_x = x + int(sway)
        
        self.draw_pakcoy_leaf(leaf_x - 20, leaf_y, 25, 35, -15, 0.6)
        self.draw_pakcoy_leaf(leaf_x + 20, leaf_y, 25, 35, 15, 0.6)
    
    def draw_four_to_six_leaves(self, x, y):
        """Menggambar 4-6 daun (rosette mulai terbentuk)"""
        sway = math.sin(self.plant_sway) * 3
        
        # Batang pusat
        pygame.draw.line(self.screen, self.STEM_WHITE, 
                        (x, y), (x + int(sway), y - 25), 8)
        
        # 6 daun dalam formasi rosette
        center_x = x + int(sway)
        center_y = y - 30
        
        leaf_positions = [
            (-30, -10, -25, 0.7),
            (30, -10, 25, 0.7),
            (-25, 5, -15, 0.75),
            (25, 5, 15, 0.75),
            (-15, 15, -5, 0.8),
            (15, 15, 5, 0.8)
        ]
        
        for lx, ly, angle, maturity in leaf_positions:
            wave = math.sin(self.leaf_wave + lx * 0.1) * 2
            self.draw_pakcoy_leaf(center_x + lx, center_y + ly + int(wave), 
                                 30, 42, angle, maturity)
    
    def draw_full_vegetative(self, x, y):
        """Menggambar fase vegetatif penuh (rosette besar)"""
        sway = math.sin(self.plant_sway) * 4
        
        # Batang pusat tebal
        pygame.draw.line(self.screen, self.STEM_LIGHT, 
                        (x, y), (x + int(sway), y - 35), 12)
        pygame.draw.line(self.screen, self.STEM_WHITE, 
                        (x, y), (x + int(sway), y - 35), 10)
        
        # 10-12 daun dalam rosette sempurna
        center_x = x + int(sway)
        center_y = y - 40
        
        # Layer 1 (terluar)
        for i in range(6):
            angle_deg = (360 / 6) * i
            distance = 50
            rad = math.radians(angle_deg)
            lx = center_x + math.cos(rad) * distance
            ly = center_y + math.sin(rad) * distance * 0.7
            wave = math.sin(self.leaf_wave + i * 0.5) * 3
            
            self.draw_pakcoy_leaf(lx, ly + int(wave), 35, 50, 
                                 angle_deg - 90, 1.0)
        
        # Layer 2 (tengah)
        for i in range(4):
            angle_deg = (360 / 4) * i + 45
            distance = 30
            rad = math.radians(angle_deg)
            lx = center_x + math.cos(rad) * distance
            ly = center_y + math.sin(rad) * distance * 0.6
            wave = math.sin(self.leaf_wave + i * 0.7) * 2
            
            self.draw_pakcoy_leaf(lx, ly + int(wave), 32, 46, 
                                 angle_deg - 90, 0.95)
        
        # Layer 3 (dalam)
        for i in range(3):
            angle_deg = (360 / 3) * i
            distance = 15
            rad = math.radians(angle_deg)
            lx = center_x + math.cos(rad) * distance
            ly = center_y + math.sin(rad) * distance * 0.5
            
            self.draw_pakcoy_leaf(lx, ly, 28, 40, 
                                 angle_deg - 90, 0.85)
    
    def draw_harvest_ready(self, x, y):
        """Menggambar pakcoy siap panen (rosette maksimal)"""
        if self.harvest_complete:
            # Tampilan setelah dipanen - sisa akar
            pygame.draw.line(self.screen, self.STEM_WHITE, (x, y), (x, y - 20), 8)
            
            # Sisa daun kecil
            for i in range(3):
                angle = (360 / 3) * i
                rad = math.radians(angle)
                lx = x + math.cos(rad) * 12
                ly = y - 20 + math.sin(rad) * 8
                pygame.draw.ellipse(self.screen, self.PAKCOY_GREEN,
                                  (lx - 8, ly - 5, 16, 10))
            
            # Teks "Terpanen!"
            harvest_text = self.font_button.render("Terpanen!", True, self.DARK_GREEN)
            self.screen.blit(harvest_text, 
                           (x - harvest_text.get_width() // 2, y - 80))
            return
        
        sway = math.sin(self.plant_sway) * 5
        
        # Batang pusat sangat tebal
        pygame.draw.line(self.screen, self.STEM_LIGHT, 
                        (x, y), (x + int(sway), y - 45), 15)
        pygame.draw.line(self.screen, self.STEM_WHITE, 
                        (x, y), (x + int(sway), y - 45), 13)
        
        # Highlight batang
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (x - 3, y), (x - 3 + int(sway), y - 45), 5)
        
        # 14-16 daun dalam rosette maksimal
        center_x = x + int(sway)
        center_y = y - 50
        
        # Layer 1 (terluar - daun terbesar)
        for i in range(8):
            angle_deg = (360 / 8) * i
            distance = 65
            rad = math.radians(angle_deg)
            lx = center_x + math.cos(rad) * distance
            ly = center_y + math.sin(rad) * distance * 0.7
            wave = math.sin(self.leaf_wave + i * 0.4) * 4
            
            self.draw_pakcoy_leaf(lx, ly + int(wave), 42, 58, 
                                 angle_deg - 90, 1.0)
        
        # Layer 2 (tengah)
        for i in range(5):
            angle_deg = (360 / 5) * i + 36
            distance = 42
            rad = math.radians(angle_deg)
            lx = center_x + math.cos(rad) * distance
            ly = center_y + math.sin(rad) * distance * 0.65
            wave = math.sin(self.leaf_wave + i * 0.6) * 3
            
            self.draw_pakcoy_leaf(lx, ly + int(wave), 38, 52, 
                                 angle_deg - 90, 0.95)
        
        # Layer 3 (dalam)
        for i in range(4):
            angle_deg = (360 / 4) * i + 20
            distance = 22
            rad = math.radians(angle_deg)
            lx = center_x + math.cos(rad) * distance
            ly = center_y + math.sin(rad) * distance * 0.6
            wave = math.sin(self.leaf_wave + i * 0.8) * 2
            
            self.draw_pakcoy_leaf(lx, ly + int(wave), 32, 45, 
                                 angle_deg - 90, 0.9)
        
        # Indikator bisa dipanen (glow effect)
        if not self.harvest_complete:
            glow_radius = 90 + math.sin(self.time * 3) * 10
            glow_surf = pygame.Surface((int(glow_radius * 2), int(glow_radius * 2)), 
                                      pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (144, 238, 144, 30), 
                             (int(glow_radius), int(glow_radius)), int(glow_radius))
            self.screen.blit(glow_surf, 
                           (center_x - glow_radius, center_y - glow_radius * 0.7))
    
    def draw_plant(self):
        """Menggambar tanaman sesuai tahap"""
        center_x = self.width // 2
        soil_y = self.height - 250
        
        if self.current_stage == 0:
            self.draw_seed(center_x, soil_y + 15)
        elif self.current_stage == 1:
            self.draw_sprout(center_x, soil_y)
        elif self.current_stage == 2:
            self.draw_two_true_leaves(center_x, soil_y)
        elif self.current_stage == 3:
            self.draw_four_to_six_leaves(center_x, soil_y)
        elif self.current_stage == 4:
            self.draw_full_vegetative(center_x, soil_y)
        elif self.current_stage == 5:
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
            pygame.draw.rect(self.screen, (144, 238, 144), progress_fill, border_radius=8)
        
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
            ('☀ Cahaya', self.sunlight_level, self.YELLOW),
            ('🌱 Pupuk', self.fertilizer_level, self.PAKCOY_GREEN)
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
        if self.current_stage == 5 and not self.harvest_complete:
            harvest_btn = pygame.Rect(self.width // 2 - 100, self.height - 180, 200, 60)
            btn_color = (144, 238, 144) if not harvest_btn.collidepoint(pygame.mouse.get_pos()) else (100, 200, 100)
            self.draw_rounded_rect(self.screen, btn_color, harvest_btn, 15)
            pygame.draw.rect(self.screen, self.WHITE, harvest_btn, 3, border_radius=15)
            
            harvest_text = self.font_button.render("🥬 PANEN!", True, self.WHITE)
            self.screen.blit(harvest_text, 
                           (self.width // 2 - harvest_text.get_width() // 2, 
                            self.height - 165))
            
            weight_text = self.font_small.render("~200-300g", True, self.WHITE)
            self.screen.blit(weight_text,
                           (self.width // 2 - weight_text.get_width() // 2,
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
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            bag_rect = pygame.Rect(
                self.fertilizer_bag['x'],
                self.fertilizer_bag['y'],
                self.fertilizer_bag['width'],
                self.fertilizer_bag['height']
            )
            self.fertilizer_bag['hover'] = bag_rect.collidepoint(mouse_pos)
            
            if self.cloud['dragging']:
                self.cloud['x'] = mouse_pos[0] - self.cloud['width'] // 2
                self.cloud['x'] = max(50, min(self.width - 200, self.cloud['x']))
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Harvest button
            if self.current_stage == 5 and not self.harvest_complete:
                harvest_btn = pygame.Rect(self.width // 2 - 100, self.height - 180, 200, 60)
                if harvest_btn.collidepoint(mouse_pos):
                    self.harvest_complete = True
                    self.harvest_animation = 1.0
                    self.show_message("Pakcoy Terpanen! Berat: 250g")
                    
                    # Particle effect saat panen
                    center_x = self.width // 2
                    center_y = self.height - 300
                    for _ in range(50):
                        self.particles.append({
                            'x': center_x,
                            'y': center_y,
                            'vx': random.uniform(-6, 6),
                            'vy': random.uniform(-8, -3),
                            'life': 1.5,
                            'color': self.PAKCOY_GREEN,
                            'size': random.randint(3, 8)
                        })
                    
                    # Timer untuk pindah ke apresiasi.py
                    pygame.time.set_timer(pygame.USEREVENT + 1, 2500)
            
            # Cloud
            cloud_rect = pygame.Rect(
                self.cloud['x'], self.cloud['y'],
                self.cloud['width'], self.cloud['height']
            )
            if cloud_rect.collidepoint(mouse_pos):
                self.cloud['dragging'] = True
                self.cloud['raining'] = True
            
            # Sun
            sun_dist = math.sqrt((mouse_pos[0] - self.sun['x'])**2 + 
                               (mouse_pos[1] - self.sun['y'])**2)
            if sun_dist < self.sun['radius'] + 30:
                self.sunlight_level = min(100, self.sunlight_level + 25)
                self.show_message("Cahaya matahari +25%!")
                self.sun['glow'] = 50
            
            # Fertilizer
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
                self.scene_manager.change_scene("pilih_sayur")
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.cloud['dragging'] = False
            self.cloud['raining'] = False
            self.cloud['rain_drops'].clear()
        
        elif event.type == pygame.USEREVENT + 1:
            # Pindah ke apresiasi.py setelah panen
            self.scene_manager.change_scene("apresiasi", plant_type="pakcoy")
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
    
    def update(self, dt):
        """Update logic dan animasi"""
        self.time += dt
        self.plant_sway += dt * 1.5
        self.leaf_wave += dt * 2
        
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
        
        if self.sun['glow'] > 0:
            self.sun['glow'] = max(0, self.sun['glow'] - dt * 50)
        
        # Growth logic
        if self.current_stage < len(self.stages) - 1 and not self.harvest_complete:
            if (self.water_level > 20 and 
                self.sunlight_level > 20 and 
                self.fertilizer_level > 20):
                
                growth_rate = 6
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
        
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle['color'],
                             (int(particle['x']), int(particle['y'])),
                             particle['size'])
        
        self.draw_ui()
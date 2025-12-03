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
        font_path2 = os.path.join('assets', 'fonts', 'Super Joyful.ttf')
        try:
            self.font_stage = pygame.font.Font(font_path, 40)
            self.font_label = pygame.font.Font(font_path2, 28)
            self.font_popup = pygame.font.Font(font_path2, 36)
            self.font_button = pygame.font.Font(font_path, 30)
            self.font_small = pygame.font.Font(font_path2, 24)
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
            "Pohon Muda",
            "Bunga",
            "Buah Muda",
            "Buah Matang"
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
        self.need_message_cooldown = 0
        
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

    def draw_young_tree(self, x, y):
        """Menggambar pohon muda (sebelum berbunga) dengan kanopi besar tanpa bunga atau buah"""
        sway = math.sin(self.plant_sway) * 4

        # Batang besar
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 130), 40)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 130), 34)

        canopy_x = x + int(sway)
        canopy_y = y - 180

        # Bayangan kanopi
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                            (canopy_x - 113, canopy_y - 33, 226, 151))
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                            (canopy_x - 95, canopy_y - 43, 160, 135))
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                            (canopy_x - 40, canopy_y - 40, 150, 133))

        # Lapisan gelap
        pygame.draw.ellipse(self.screen, self.DARK_GREEN,
                            (canopy_x - 110, canopy_y - 30, 220, 145))
        pygame.draw.ellipse(self.screen, self.DARK_GREEN,
                            (canopy_x - 90, canopy_y - 40, 155, 130))
        pygame.draw.ellipse(self.screen, self.DARK_GREEN,
                            (canopy_x - 35, canopy_y - 37, 145, 128))

        # Lapisan hijau utama
        pygame.draw.ellipse(self.screen, self.GREEN,
                            (canopy_x - 105, canopy_y - 25, 210, 135))
        pygame.draw.ellipse(self.screen, self.GREEN,
                            (canopy_x - 85, canopy_y - 35, 150, 125))
        pygame.draw.ellipse(self.screen, self.GREEN,
                            (canopy_x - 30, canopy_y - 32, 140, 123))

        # Lapisan terang
        pygame.draw.ellipse(self.screen, self.LEAF_GREEN,
                            (canopy_x - 100, canopy_y - 20, 200, 125))
        pygame.draw.ellipse(self.screen, self.LEAF_GREEN,
                            (canopy_x - 80, canopy_y - 30, 145, 120))

        # Highlight
        pygame.draw.ellipse(self.screen, (100, 220, 100),
                            (canopy_x - 70, canopy_y - 5, 110, 55))
    
    def draw_flower(self, x, y):
        """Menggambar pohon berbunga dengan bentuk sama seperti pohon buah matang"""
        sway = math.sin(self.plant_sway) * 4

        # Batang besar (mengikuti draw_ripe_fruit)
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 130), 40)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 130), 34)

        # Titik pusat kanopi
        canopy_x = x + int(sway)
        canopy_y = y - 180

        # Bayangan kanopi organik (layer seperti ripe_fruit)
        pygame.draw.ellipse(self.screen, (25, 100, 25),
                        (canopy_x - 113, canopy_y - 33, 226, 151))
        pygame.draw.ellipse(self.screen, (25, 100, 25),
                        (canopy_x - 95, canopy_y - 43, 160, 135))
        pygame.draw.ellipse(self.screen, (25, 100, 25),
                        (canopy_x - 40, canopy_y - 40, 150, 133))

        # Layer daun gelap
        pygame.draw.ellipse(self.screen, self.DARK_GREEN,
                        (canopy_x - 110, canopy_y - 30, 220, 145))
        pygame.draw.ellipse(self.screen, self.DARK_GREEN,
                        (canopy_x - 90, canopy_y - 40, 155, 130))
        pygame.draw.ellipse(self.screen, self.DARK_GREEN,
                        (canopy_x - 35, canopy_y - 37, 145, 128))

        # Layer hijau utama
        pygame.draw.ellipse(self.screen, self.GREEN,
                        (canopy_x - 105, canopy_y - 25, 210, 135))
        pygame.draw.ellipse(self.screen, self.GREEN,
                        (canopy_x - 85, canopy_y - 35, 150, 125))
        pygame.draw.ellipse(self.screen, self.GREEN,
                        (canopy_x - 30, canopy_y - 32, 140, 123))

        # Layer terang
        pygame.draw.ellipse(self.screen, self.LEAF_GREEN,
                        (canopy_x - 100, canopy_y - 20, 200, 125))
        pygame.draw.ellipse(self.screen, self.LEAF_GREEN,
                        (canopy_x - 80, canopy_y - 30, 145, 120))

        # Highlight
        pygame.draw.ellipse(self.screen, (100, 220, 100),
                        (canopy_x - 70, canopy_y - 5, 110, 55))

        # Titik-titik bunga (di posisi mirip apel matang)
        flower_spots = [
            (canopy_x - 65, canopy_y + 15),
            (canopy_x - 40, canopy_y - 10),
            (canopy_x - 15, canopy_y + 20),
            (canopy_x + 10, canopy_y - 5),
            (canopy_x + 40, canopy_y + 15),
            (canopy_x + 65, canopy_y + 25),
            (canopy_x - 80, canopy_y + 30),
            (canopy_x + 55, canopy_y + 35),
            (canopy_x - 25, canopy_y + 30),
            (canopy_x + 25, canopy_y + 25)
        ]

        # Menggambar bunga-bunga
        for fx, fy in flower_spots:
            for i in range(5):  # kelopak
                angle = (360 / 5) * i + self.flower_spin * 0.5
                rad = math.radians(angle)
                px = fx + math.cos(rad) * 10
                py = fy + math.sin(rad) * 10
                pygame.draw.circle(self.screen, self.PINK, (int(px), int(py)), 6)

            # pusat bunga
            pygame.draw.circle(self.screen, self.YELLOW, (fx, fy), 5)
            pygame.draw.circle(self.screen, (255, 255, 200), (fx, fy), 3)

    
    def draw_young_fruit(self, x, y):
        """Menggambar pohon dengan buah muda (hijau kecil) dengan bentuk seperti draw_ripe_fruit()"""
        sway = math.sin(self.plant_sway) * 4

        # Batang besar
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 130), 40)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 130), 34)

        canopy_x = x + int(sway)
        canopy_y = y - 180

        # Bayangan kanopi
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                        (canopy_x - 113, canopy_y - 33, 226, 151))
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                        (canopy_x - 95, canopy_y - 43, 160, 135))
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                        (canopy_x - 40, canopy_y - 40, 150, 133))

        # Lapisan gelap
        pygame.draw.ellipse(self.screen, self.DARK_GREEN, 
                        (canopy_x - 110, canopy_y - 30, 220, 145))
        pygame.draw.ellipse(self.screen, self.DARK_GREEN, 
                        (canopy_x - 90, canopy_y - 40, 155, 130))
        pygame.draw.ellipse(self.screen, self.DARK_GREEN, 
                        (canopy_x - 35, canopy_y - 37, 145, 128))

        # Lapisan hijau utama
        pygame.draw.ellipse(self.screen, self.GREEN, 
                        (canopy_x - 105, canopy_y - 25, 210, 135))
        pygame.draw.ellipse(self.screen, self.GREEN, 
                        (canopy_x - 85, canopy_y - 35, 150, 125))
        pygame.draw.ellipse(self.screen, self.GREEN, 
                        (canopy_x - 30, canopy_y - 32, 140, 123))

        # Lapisan terang
        pygame.draw.ellipse(self.screen, self.LEAF_GREEN, 
                        (canopy_x - 100, canopy_y - 20, 200, 125))
        pygame.draw.ellipse(self.screen, self.LEAF_GREEN, 
                        (canopy_x - 80, canopy_y - 30, 145, 120))

        # Highlight
        pygame.draw.ellipse(self.screen, (100, 220, 100), 
                        (canopy_x - 70, canopy_y - 5, 110, 55))

        # Titik buah muda (posisi sama seperti apel matang)
        young_spots = [
            (canopy_x - 65, canopy_y + 15),
            (canopy_x - 40, canopy_y - 10),
            (canopy_x - 15, canopy_y + 20),
            (canopy_x + 10, canopy_y - 5),
            (canopy_x + 40, canopy_y + 15),
            (canopy_x + 65, canopy_y + 25),
            (canopy_x - 80, canopy_y + 30),
            (canopy_x + 55, canopy_y + 35),
            (canopy_x - 25, canopy_y + 30),
            (canopy_x + 25, canopy_y + 25)
        ]

        # Gambar buah muda hijau
        for ax, ay in young_spots:
            # Apel hijau kecil
            pygame.draw.circle(self.screen, self.LIGHT_GREEN, (ax, ay), 10)
            pygame.draw.circle(self.screen, (180, 255, 180), (ax - 3, ay - 3), 4)
            pygame.draw.circle(self.screen, (255, 255, 255), (ax - 4, ay - 4), 2)

    
    def draw_ripe_fruit(self, x, y):
        """Menggambar pohon dengan buah matang (merah)"""
        sway = math.sin(self.plant_sway) * 4
        
        # Batang lebih besar dan tinggi
        pygame.draw.line(self.screen, self.TRUNK_BROWN, (x, y), (x + int(sway), y - 130), 40)
        pygame.draw.line(self.screen, self.DARK_BROWN, (x, y), (x + int(sway), y - 130), 34)
        
        # Kanopi organik (meliuk-liuk)
        canopy_x = x + int(sway)
        canopy_y = y - 180
        
        # Bayangan kanopi organik - lebih besar
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                           (canopy_x - 113, canopy_y - 33, 226, 151))
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                           (canopy_x - 95, canopy_y - 43, 160, 135))
        pygame.draw.ellipse(self.screen, (25, 100, 25), 
                           (canopy_x - 40, canopy_y - 40, 150, 133))
        
        # Lapisan kanopi organik (tidak bulat sempurna) - lebih besar
        pygame.draw.ellipse(self.screen, self.DARK_GREEN, 
                           (canopy_x - 110, canopy_y - 30, 220, 145))
        pygame.draw.ellipse(self.screen, self.DARK_GREEN, 
                           (canopy_x - 90, canopy_y - 40, 155, 130))
        pygame.draw.ellipse(self.screen, self.DARK_GREEN, 
                           (canopy_x - 35, canopy_y - 37, 145, 128))
        
        pygame.draw.ellipse(self.screen, self.GREEN, 
                           (canopy_x - 105, canopy_y - 25, 210, 135))
        pygame.draw.ellipse(self.screen, self.GREEN, 
                           (canopy_x - 85, canopy_y - 35, 150, 125))
        pygame.draw.ellipse(self.screen, self.GREEN, 
                           (canopy_x - 30, canopy_y - 32, 140, 123))
        
        pygame.draw.ellipse(self.screen, self.LEAF_GREEN, 
                           (canopy_x - 100, canopy_y - 20, 200, 125))
        pygame.draw.ellipse(self.screen, self.LEAF_GREEN, 
                           (canopy_x - 80, canopy_y - 30, 145, 120))
        
        # Highlight kanopi
        pygame.draw.ellipse(self.screen, (100, 220, 100), 
                           (canopy_x - 70, canopy_y - 5, 110, 55))
        
        # Apel-apel pada pohon - lebih banyak dan tersebar
        self.apple_positions = []
        apple_spots = [
            (canopy_x - 65, canopy_y + 15),
            (canopy_x - 40, canopy_y - 10),
            (canopy_x - 15, canopy_y + 20),
            (canopy_x + 10, canopy_y - 5),
            (canopy_x + 40, canopy_y + 15),
            (canopy_x + 65, canopy_y + 25),
            (canopy_x - 80, canopy_y + 30),
            (canopy_x + 55, canopy_y + 35),
            (canopy_x - 25, canopy_y + 30),
            (canopy_x + 25, canopy_y + 25)
        ]
        
        for idx, (ax, ay) in enumerate(apple_spots):
            self.apple_positions.append((ax, ay, idx))
            
            # Apel merah mengkilap
            pygame.draw.circle(self.screen, self.RED_APPLE, (ax, ay), 12)
            pygame.draw.circle(self.screen, self.LIGHT_RED, (ax - 4, ay - 4), 5)
            pygame.draw.circle(self.screen, (255, 255, 255), (ax - 5, ay - 5), 2)
    

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
            self.draw_young_tree(center_x, soil_y)
        elif self.current_stage == 4:
            self.draw_flower(center_x, soil_y)
        elif self.current_stage == 5:
            self.draw_young_fruit(center_x, soil_y)
        elif self.current_stage == 6:
            self.draw_ripe_fruit(center_x, soil_y)
    
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
            
    def get_harvest_button_rect(self):
        """Menghasilkan rect tombol panen yang otomatis menyesuaikan teks."""
        text_title = self.font_button.render("PANEN!", True, self.WHITE)
        text_count = self.font_small.render(f"{self.total_harvested}/5 buah", True, self.WHITE)

        content_width = max(text_title.get_width(), text_count.get_width())
        padding_x = 40
        padding_y = 25

        btn_width = content_width + padding_x
        btn_height = text_title.get_height() + text_count.get_height() + padding_y

        btn_x = self.width // 2 - btn_width // 2
        btn_y = self.height - 180

        return pygame.Rect(btn_x, btn_y, btn_width, btn_height)

    
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
            ('Air', self.water_level, self.WATER_BLUE),
            ('Cahaya', self.sunlight_level, self.YELLOW),
            ('Pupuk', self.fertilizer_level, self.GREEN)
        ]
        
        for i, (label, level, color) in enumerate(levels):
            y = bar_y + (i * bar_spacing)
            
            label_text = self.font_label.render(label, True, self.WHITE)
            self.screen.blit(label_text, (bar_x, y - 2))
            
            bar_bg = pygame.Rect(bar_x + 115, y, bar_width, bar_height)
            pygame.draw.rect(self.screen, (50, 50, 50), bar_bg, border_radius=12)
            
            fill_width = int((level / 100) * bar_width)
            if fill_width > 0:
                bar_fill = pygame.Rect(bar_x + 115, y, fill_width, bar_height)
                pygame.draw.rect(self.screen, color, bar_fill, border_radius=12)
            
            pygame.draw.rect(self.screen, self.WHITE, bar_bg, 2, border_radius=12)
            
            pct_text = self.font_small.render(f"{int(level)}%", True, self.WHITE)
            self.screen.blit(pct_text, (bar_x + 115 + bar_width + 10, y - 1))
        
        # Harvest button (hanya muncul saat stage panen)
        if self.current_stage == 6 and self.total_harvested < 5:

            harvest_btn = self.get_harvest_button_rect()

            # Hover color
            btn_color = (255, 140, 0) if self.harvest_button_hover else (255, 165, 0)

            self.draw_rounded_rect(self.screen, btn_color, harvest_btn, 15)
            pygame.draw.rect(self.screen, self.WHITE, harvest_btn, 3, border_radius=15)

            # Text PANEN!
            text_title = self.font_button.render("PANEN!", True, self.WHITE)
            self.screen.blit(
                text_title,
                (
                    harvest_btn.x + harvest_btn.width // 2 - text_title.get_width() // 2,
                    harvest_btn.y + 10
                )
            )

            # Text jumlah
            text_count = self.font_small.render(f"{self.total_harvested}/5 buah", True, self.WHITE)
            self.screen.blit(
                text_count,
                (
                    harvest_btn.x + harvest_btn.width // 2 - text_count.get_width() // 2,
                    harvest_btn.y + harvest_btn.height - text_count.get_height() - 10
                )
            )

        
        # Message
        if self.message_timer > 0:
            msg_text = self.font_popup.render(self.message, True, self.WHITE)
            msg_bg = pygame.Rect(self.width // 2 - msg_text.get_width() // 2 - 20,
                                self.height // 2 - 50, 
                                msg_text.get_width() + 40, 60)
            self.draw_rounded_rect(self.screen, (150, 200, 130), msg_bg, 15)
            self.screen.blit(msg_text, 
                           (self.width // 2 - msg_text.get_width() // 2, 
                            self.height // 2 - 40))
            pygame.draw.rect(self.screen, self.WHITE, msg_bg, 2, border_radius=12)
        
        # Back button
        back_button = pygame.Rect(self.width - 150, self.height - 70, 120, 50)
        color = self.BUTTON_GREEN if not back_button.collidepoint(pygame.mouse.get_pos()) else (150, 200, 130)
        self.draw_rounded_rect(self.screen, color, back_button, 12)
        pygame.draw.rect(self.screen, self.WHITE, back_button, 2, border_radius=12)
        
        back_text = self.font_button.render("Kembali", True, self.WHITE)
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
            
            if self.cloud['dragging']:
                self.cloud['x'] = mouse_pos[0] - self.cloud['width'] // 2

            bag_rect = pygame.Rect(
                self.fertilizer_bag['x'],
                self.fertilizer_bag['y'],
                self.fertilizer_bag['width'],
                self.fertilizer_bag['height']
            )
            self.fertilizer_bag['hover'] = bag_rect.collidepoint(mouse_pos)
            
            # Harvest button hover
            if self.current_stage == 6 and self.total_harvested < 5:
                harvest_btn = self.get_harvest_button_rect()
                self.harvest_button_hover = harvest_btn.collidepoint(mouse_pos)

                # Render teks
                text_title = self.font_button.render("PANEN!", True, self.WHITE)
                text_count = self.font_small.render(f"{self.total_harvested}/5 buah", True, self.WHITE)

                # Hitung ukuran tombol berdasarkan teks paling lebar
                content_width = max(text_title.get_width(), text_count.get_width())
                padding_x = 40   # kiri-kanan
                padding_y = 25   # atas-bawah total

                btn_width = content_width + padding_x
                btn_height = text_title.get_height() + text_count.get_height() + padding_y

                # Posisi tombol
                btn_x = self.width // 2 - btn_width // 2
                btn_y = self.height - 180

                harvest_btn = pygame.Rect(btn_x, btn_y, btn_width, btn_height)

                # Warna hover
                btn_color = (255, 140, 0) if self.harvest_button_hover else (255, 165, 0)

                # Gambar tombol
                self.draw_rounded_rect(self.screen, btn_color, harvest_btn, 18)
                pygame.draw.rect(self.screen, self.WHITE, harvest_btn, 3, border_radius=18)

                # Teks PANEN!
                self.screen.blit(
                    text_title,
                    (btn_x + btn_width // 2 - text_title.get_width() // 2,
                    btn_y + 10)
                )

                # Teks jumlah panen (0/5 buah)
                self.screen.blit(
                    text_count,
                    (btn_x + btn_width // 2 - text_count.get_width() // 2,
                    btn_y + btn_height - text_count.get_height() - 10)
                )

        
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
        # === CLOUD MOVEMENT ===
        if self.cloud['dragging']:
            # mengikuti mouse
            mouse_x, _ = pygame.mouse.get_pos()
            self.cloud['x'] = mouse_x - self.cloud['width'] // 2
        else:
            # gerak natural kiri-kanan
            self.cloud['x'] += 0.4
            if self.cloud['x'] > self.width:
                self.cloud['x'] = -150

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
                    self.show_message(f"Fase {self.stages[self.current_stage]}!")
            else:
                # Turunkan cooldown jika masih berjalan
                if self.need_message_cooldown > 0:
                    self.need_message_cooldown -= dt

                # Hanya tampilkan pesan jika cooldown habis
                if self.need_message_cooldown <= 0:

                    if self.water_level < 20:
                        self.show_message("Butuh air!")
                        self.need_message_cooldown = 1.5  # cooldown 1.5 detik

                    elif self.sunlight_level < 20:
                        self.show_message("Butuh cahaya!")
                        self.need_message_cooldown = 1.5

                    elif self.fertilizer_level < 20:
                        self.show_message("Butuh pupuk!")
                        self.need_message_cooldown = 1.5
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
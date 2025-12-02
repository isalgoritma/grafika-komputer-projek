import pygame
import math
import random
import os

class GrowthSeledri:
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
        self.CELERY_GREEN = (34, 139, 34)
        self.DARK_GREEN = (0, 100, 0)
        self.LIGHT_GREEN = (144, 238, 144)
        self.BRIGHT_GREEN = (50, 205, 50)
        self.STEM_GREEN = (152, 251, 152)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 223, 0)
        self.BUTTON_GREEN = (126, 176, 105)
        self.WATER_BLUE = (135, 206, 250)
        self.CLOUD_WHITE = (240, 248, 255)
        
        # Tahapan pertumbuhan seledri
        self.stages = [
            "Biji",
            "Kecambah",
            "Daun Muda",
            "Vegetatif",
            "Siap Panen"
        ]
        
        self.current_stage = 0
        self.growth_progress = 0
        self.stage_requirements = [15, 30, 45, 60, 75]
        
        # Faktor pertumbuhan
        self.water_level = 35
        self.sunlight_level = 35
        self.fertilizer_level = 35
        
        # Kebutuhan per detik
        self.water_consumption = 2.8
        self.sunlight_consumption = 2.3
        self.fertilizer_consumption = 1.8
        
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
        self.total_harvested = 0
        self.harvested_celery = []
        self.harvest_button_hover = False
        
        # Particle effects
        self.particles = []
        
        # Animation
        self.plant_sway = 0
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
        """Menggambar biji seledri (sangat kecil)"""
        # Biji seledri sangat kecil, bulat lonjong
        pygame.draw.ellipse(self.screen, (60, 50, 40), (x - 8, y - 4, 16, 8))
        pygame.draw.ellipse(self.screen, (90, 75, 50), (x - 6, y - 3, 12, 6))
        pygame.draw.ellipse(self.screen, (120, 100, 70), (x - 4, y - 2, 8, 4))
        # Highlight kecil
        pygame.draw.ellipse(self.screen, (140, 120, 90), (x - 3, y - 1, 4, 2))
    
    def draw_sprout(self, x, y):
        """Menggambar kecambah seledri"""
        sway = math.sin(self.plant_sway) * 2
        
        # Akar tipis
        for i in range(3):
            offset = (i - 1) * 6
            root_end_x = x + offset + random.randint(-2, 2)
            root_end_y = y + 12 + random.randint(0, 6)
            pygame.draw.line(self.screen, (139, 90, 43),
                           (x, y + 5), (root_end_x, root_end_y), 1)
        
        # Batang tipis
        pygame.draw.line(self.screen, self.STEM_GREEN, 
                        (x, y), (x + int(sway), y - 30), 3)
        
        # Daun embrio kecil (dua helai)
        leaf_left = [
            (x + int(sway), y - 30),
            (x + int(sway) - 8, y - 27),
            (x + int(sway) - 6, y - 25),
            (x + int(sway), y - 28)
        ]
        pygame.draw.polygon(self.screen, self.LIGHT_GREEN, leaf_left)
        
        leaf_right = [
            (x + int(sway), y - 30),
            (x + int(sway) + 8, y - 27),
            (x + int(sway) + 6, y - 25),
            (x + int(sway), y - 28)
        ]
        pygame.draw.polygon(self.screen, self.LIGHT_GREEN, leaf_right)
    
    def draw_celery_leaf(self, x, y, size, angle):
        """Menggambar daun seledri yang detail (bergerigi halus)"""
        leaf_surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
        
        # Bentuk daun dengan tepi bergerigi
        points = []
        num_points = 16
        for i in range(num_points):
            a = (360 / num_points) * i
            rad = math.radians(a)
            # Gerigi halus
            r = size * (0.85 if i % 2 == 0 else 1.0)
            px = size + math.cos(rad) * r
            py = size + math.sin(rad) * r * 1.2  # Lebih lonjong
            points.append((px, py))
        
        pygame.draw.polygon(leaf_surf, self.CELERY_GREEN, points)
        pygame.draw.polygon(leaf_surf, self.BRIGHT_GREEN, 
                          [(p[0] + 2, p[1] + 2) for p in points[:-4]])
        
        # Urat daun tengah
        center = size
        pygame.draw.line(leaf_surf, self.DARK_GREEN, 
                        (center, 5), (center, size * 2 - 5), 2)
        
        # Urat samping
        for i in range(5):
            vein_angle = -60 + i * 30
            vein_rad = math.radians(vein_angle)
            vein_x = center + math.cos(vein_rad) * size * 0.7
            vein_y = center + math.sin(vein_rad) * size * 0.9
            pygame.draw.line(leaf_surf, self.DARK_GREEN, 
                           (center, center), (vein_x, vein_y), 1)
        
        rotated = pygame.transform.rotate(leaf_surf, angle)
        rect = rotated.get_rect(center=(int(x), int(y)))
        self.screen.blit(rotated, rect)
    
    def draw_young_leaves(self, x, y):
        """Menggambar daun muda seledri (beberapa batang muda)"""
        sway = math.sin(self.plant_sway) * 3
        
        # 2-3 batang muda
        for i in range(3):
            offset = (i - 1) * 12
            stem_x = x + offset
            stem_sway = sway * (1 - abs(i - 1) * 0.2)
            
            # Batang hijau muda
            pygame.draw.line(self.screen, self.STEM_GREEN, 
                           (stem_x, y), 
                           (stem_x + int(stem_sway), y - 50), 6)
            pygame.draw.line(self.screen, self.LIGHT_GREEN, 
                           (stem_x, y), 
                           (stem_x + int(stem_sway), y - 50), 4)
            
            # Daun-daun kecil di batang
            for j in range(3):
                leaf_y = y - 15 - (j * 12)
                # Daun kiri
                self.draw_celery_leaf(stem_x + int(stem_sway) - 15, leaf_y, 12, -30)
                # Daun kanan
                self.draw_celery_leaf(stem_x + int(stem_sway) + 15, leaf_y, 12, 30)
    
    def draw_vegetative(self, x, y):
        """Menggambar fase vegetatif (banyak batang, daun lebat)"""
        sway = math.sin(self.plant_sway) * 4
        
        # 5-6 batang seledri yang tumbuh bersamaan
        for i in range(6):
            offset = (i - 2.5) * 14
            stem_x = x + offset
            stem_sway = sway * (1 - abs(i - 2.5) * 0.1)
            stem_height = 70 + (i % 3) * 10
            
            # Batang yang lebih tebal
            pygame.draw.line(self.screen, self.CELERY_GREEN, 
                           (stem_x, y), 
                           (stem_x + int(stem_sway), y - stem_height), 9)
            pygame.draw.line(self.screen, self.STEM_GREEN, 
                           (stem_x, y), 
                           (stem_x + int(stem_sway), y - stem_height), 7)
            
            # Highlight pada batang
            pygame.draw.line(self.screen, self.LIGHT_GREEN, 
                           (stem_x + 2, y - 5), 
                           (stem_x + int(stem_sway) + 2, y - stem_height + 5), 2)
            
            # Daun-daun berlimpah
            num_leaves = 5 + (i % 2)
            for j in range(num_leaves):
                leaf_y = y - 15 - (j * 12)
                leaf_size = 16 + (j % 3) * 2
                
                # Daun kiri
                self.draw_celery_leaf(
                    stem_x + int(stem_sway * (1 - j * 0.1)) - 18, 
                    leaf_y, 
                    leaf_size, 
                    -35 - j * 3
                )
                
                # Daun kanan
                self.draw_celery_leaf(
                    stem_x + int(stem_sway * (1 - j * 0.1)) + 18, 
                    leaf_y, 
                    leaf_size, 
                    35 + j * 3
                )
    
    def draw_harvest_ready(self, x, y):
        """Menggambar seledri siap panen (maksimal pertumbuhan)"""
        sway = math.sin(self.plant_sway) * 5
        
        # 7-8 batang seledri yang siap dipanen
        self.celery_positions = []
        
        for i in range(8):
            offset = (i - 3.5) * 16
            stem_x = x + offset
            stem_sway = sway * (1 - abs(i - 3.5) * 0.08)
            stem_height = 85 + (i % 4) * 8
            
            # Skip jika sudah dipanen
            if i in [c['id'] for c in self.harvested_celery]:
                continue
            
            self.celery_positions.append((stem_x, y, stem_height, i))
            
            # Batang tebal dan panjang
            pygame.draw.line(self.screen, self.CELERY_GREEN, 
                           (stem_x, y), 
                           (stem_x + int(stem_sway), y - stem_height), 11)
            pygame.draw.line(self.screen, self.STEM_GREEN, 
                           (stem_x, y), 
                           (stem_x + int(stem_sway), y - stem_height), 9)
            
            # Highlight mengkilap
            pygame.draw.line(self.screen, (200, 255, 200), 
                           (stem_x + 3, y - 5), 
                           (stem_x + int(stem_sway) + 3, y - stem_height + 5), 3)
            
            # Daun-daun lebat dan segar
            num_leaves = 6
            for j in range(num_leaves):
                leaf_y = y - 18 - (j * 13)
                leaf_size = 18 + (j % 3) * 3
                leaf_sway_factor = 1 - j * 0.12
                
                # Daun kiri
                self.draw_celery_leaf(
                    stem_x + int(stem_sway * leaf_sway_factor) - 20, 
                    leaf_y, 
                    leaf_size, 
                    -40 - j * 4
                )
                
                # Daun kanan
                self.draw_celery_leaf(
                    stem_x + int(stem_sway * leaf_sway_factor) + 20, 
                    leaf_y, 
                    leaf_size, 
                    40 + j * 4
                )
    
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
            ('🌱 Pupuk', self.fertilizer_level, self.CELERY_GREEN)
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
        if self.current_stage == 4 and self.total_harvested < 8:
            harvest_btn = pygame.Rect(self.width // 2 - 100, self.height - 180, 200, 60)
            btn_color = (255, 140, 0) if self.harvest_button_hover else (255, 165, 0)
            self.draw_rounded_rect(self.screen, btn_color, harvest_btn, 15)
            pygame.draw.rect(self.screen, self.WHITE, harvest_btn, 3, border_radius=15)
            
            harvest_text = self.font_button.render("🌿 PANEN!", True, self.WHITE)
            self.screen.blit(harvest_text, 
                           (self.width // 2 - harvest_text.get_width() // 2, 
                            self.height - 165))
            
            count_text = self.font_small.render(f"{self.total_harvested}/8 batang", True, self.WHITE)
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
    
    def harvest_celery(self, mouse_pos):
        """Panen seledri yang diklik"""
        if self.current_stage != 4:
            return
        
        if not hasattr(self, 'celery_positions'):
            return
        
        for stem_x, stem_y, stem_height, celery_id in self.celery_positions:
            # Skip jika sudah dipanen
            if celery_id in [c['id'] for c in self.harvested_celery]:
                continue
            
            # Cek area klik (batang dan sekitarnya)
            sway = math.sin(self.plant_sway) * 5
            top_x = stem_x + int(sway)
            top_y = stem_y - stem_height
            
            # Cek apakah mouse dekat dengan batang
            dist_to_stem = min(
                math.sqrt((mouse_pos[0] - stem_x)**2 + (mouse_pos[1] - stem_y)**2),
                math.sqrt((mouse_pos[0] - top_x)**2 + (mouse_pos[1] - top_y)**2)
            )
            
            if dist_to_stem < 25:
                # Animasi panen
                self.harvested_celery.append({
                    'id': celery_id,
                    'x': stem_x,
                    'y': stem_y - stem_height // 2,
                    'vx': random.uniform(-4, 4),
                    'vy': random.uniform(-10, -6),
                    'rotation': 0,
                    'rot_speed': random.uniform(-6, 6),
                    'height': stem_height
                })
                self.total_harvested += 1
                self.show_message(f"Seledri dipanen! {self.total_harvested}/8")
                
                # Particle effect
                for _ in range(20):
                    self.particles.append({
                        'x': stem_x,
                        'y': stem_y - stem_height // 2,
                        'vx': random.uniform(-3, 3),
                        'vy': random.uniform(-5, -2),
                        'life': 1.0,
                        'color': self.CELERY_GREEN,
                        'size': random.randint(2, 5)
                    })
                
                # Cek apakah semua seledri sudah dipanen
                if self.total_harvested >= 8:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
                    self.show_message("Selamat! Semua seledri terpanen!")
                
                break
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.USEREVENT + 1:
            # Pindah ke halaman apresiasi
            self.scene_manager.change_scene("apresiasi", plant_type="seledri")
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        
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
            if self.current_stage == 4 and self.total_harvested < 8:
                harvest_btn = pygame.Rect(self.width // 2 - 100, self.height - 180, 200, 60)
                self.harvest_button_hover = harvest_btn.collidepoint(mouse_pos)
            
            if self.cloud['dragging']:
                self.cloud['x'] = mouse_pos[0] - self.cloud['width'] // 2
                self.cloud['x'] = max(50, min(self.width - 200, self.cloud['x']))
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Cek klik seledri untuk panen
            if self.current_stage == 4:
                self.harvest_celery(mouse_pos)
            
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
                self.scene_manager.change_scene("pilih_sayur")
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.cloud['dragging'] = False
            self.cloud['raining'] = False
            self.cloud['rain_drops'].clear()
    
    def update(self, dt):
        """Update logic dan animasi"""
        self.time += dt
        self.plant_sway += dt * 2
        
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
        
        # Update harvested celery animation
        for celery in self.harvested_celery[:]:
            celery['x'] += celery['vx']
            celery['y'] += celery['vy']
            celery['vy'] += 0.5
            celery['rotation'] += celery['rot_speed']
            
            if celery['y'] > self.height + 50:
                self.harvested_celery.remove(celery)
        
        if self.sun['glow'] > 0:
            self.sun['glow'] = max(0, self.sun['glow'] - dt * 50)
        
        # Growth logic
        if self.current_stage < len(self.stages) - 1:
            if (self.water_level > 20 and 
                self.sunlight_level > 20 and 
                self.fertilizer_level > 20):
                
                growth_rate = 4.5
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
        
        # Draw harvested celery (animasi jatuh)
        for celery in self.harvested_celery:
            cx, cy = int(celery['x']), int(celery['y'])
            
            # Gambar batang seledri yang jatuh dengan rotasi
            celery_surf = pygame.Surface((20, celery['height']), pygame.SRCALPHA)
            pygame.draw.rect(celery_surf, self.CELERY_GREEN, (0, 0, 20, celery['height']))
            pygame.draw.rect(celery_surf, self.STEM_GREEN, (2, 0, 16, celery['height']))
            
            rotated = pygame.transform.rotate(celery_surf, celery['rotation'])
            rect = rotated.get_rect(center=(cx, cy))
            self.screen.blit(rotated, rect)
        
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle['color'],
                             (int(particle['x']), int(particle['y'])),
                             particle['size'])
        
        self.draw_ui()
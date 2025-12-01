import pygame
import math
import os

class PilihSayur:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Load background image
        bg_path = os.path.join('assets', 'images', 'bg-select.png')
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        # Load custom font
        font_path = os.path.join('assets', 'fonts', 'Heyam.ttf')
        try:
            self.font_title = pygame.font.Font(font_path, 80)
            self.font_button = pygame.font.Font(font_path, 50)
        except:
            print("Warning: Custom font not found, using default")
            self.font_title = pygame.font.Font(None, 80)
            self.font_button = pygame.font.Font(None, 50)
        
        # Warna
        self.CARD_BG = (255, 209, 128)
        self.CARD_BORDER = (219, 123, 43)
        self.BUTTON_GREEN = (126, 176, 105)
        self.BUTTON_DARK = (88, 129, 87)
        self.TEXT_WHITE = (255, 255, 255)
        self.TEXT_GREEN = (88, 129, 87)
        
        # Data kartu
        self.cards = [
            {
                'name': 'BAYAM',
                'color': (100, 150, 100),
                'scene': 'bayam',
                'pos': [100, 150],
                'target_pos': [100, 150],
                'scale': 1.0,
                'target_scale': 1.0,
                'hover': False,
                'rotation': 0
            },
            {
                'name': 'SELEDRI',
                'color': (120, 160, 90),
                'scene': 'growth_seledri',
                'pos': [700, 150],
                'target_pos': [700, 150],
                'scale': 1.0,
                'target_scale': 1.0,
                'hover': False,
                'rotation': 0
            },
            {
                'name': 'SELADA',
                'color': (130, 180, 100),
                'scene': 'growth_selada',
                'pos': [400, 450],
                'target_pos': [400, 450],
                'scale': 1.0,
                'target_scale': 1.0,
                'hover': False,
                'rotation': 0
            }
        ]
        
        # Animasi masuk dari samping
        self.cards[0]['pos'][0] = -500
        self.cards[1]['pos'][0] = self.width + 500
        self.cards[2]['pos'][1] = self.height + 300
        
        # Timer untuk delay animasi kartu
        self.animation_timer = 0
    
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Menggambar persegi dengan sudut melengkung"""
        if len(color) == 4:
            temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, color, temp_surface.get_rect(), border_radius=radius)
            surface.blit(temp_surface, (rect.x, rect.y))
        else:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_plant_card(self, card, index):
        """Menggambar kartu tanaman dengan animasi"""
        x, y = card['pos']
        scale = card['scale']
        
        card_width = int(400 * scale)
        card_height = int(280 * scale)
        
        # Update posisi dengan smooth interpolation
        card['pos'][0] += (card['target_pos'][0] - card['pos'][0]) * 0.12
        card['pos'][1] += (card['target_pos'][1] - card['pos'][1]) * 0.12
        
        # Update scale dengan smooth interpolation
        card['scale'] += (card['target_scale'] - card['scale']) * 0.2
        
        x = int(card['pos'][0])
        y = int(card['pos'][1])
        
        # Efek floating saat hover (naik turun halus)
        if card['hover']:
            float_offset = math.sin(pygame.time.get_ticks() * 0.003) * 8
            y += int(float_offset)
            
            # Tambah sedikit rotasi (efek visual saja, tidak benar-benar rotate)
            card['rotation'] += (5 - card['rotation']) * 0.1
        else:
            card['rotation'] += (0 - card['rotation']) * 0.1
        
        # Bayangan kartu
        shadow_offset = int(8 * scale)
        shadow_rect = pygame.Rect(
            x + shadow_offset, 
            y + shadow_offset, 
            card_width, 
            card_height
        )
        self.draw_rounded_rect(self.screen, (50, 50, 50, 120), shadow_rect, 30)
        
        # Border kartu
        card_rect = pygame.Rect(x, y, card_width, card_height)
        self.draw_rounded_rect(self.screen, self.CARD_BORDER, card_rect, 30)
        
        # Background kartu
        inner_rect = pygame.Rect(
            x + 8, 
            y + 8, 
            card_width - 16, 
            card_height - 16
        )
        self.draw_rounded_rect(self.screen, self.CARD_BG, inner_rect, 25)
        
        # Teks nama tanaman dengan efek glow saat hover
        font_size = int(80 * scale)
        scaled_font = pygame.font.Font(None, font_size)
        
        if card['hover']:
            # Efek glow dengan multiple shadow
            for offset in range(8, 0, -2):
                glow_alpha = int(30 * (offset / 8))
                glow_color = (card['color'][0], card['color'][1], card['color'][2])
                glow_text = scaled_font.render(card['name'], True, glow_color)
                glow_x = x + card_width // 2 - glow_text.get_width() // 2
                glow_y = y + int(50 * scale)
                self.screen.blit(glow_text, (glow_x, glow_y))
        
        title_shadow = scaled_font.render(card['name'], True, card['color'])
        title_text = scaled_font.render(card['name'], True, self.TEXT_GREEN)
        
        title_x = x + card_width // 2 - title_text.get_width() // 2
        title_y = y + int(50 * scale)
        
        self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
        self.screen.blit(title_text, (title_x, title_y))
        
        # Tombol Play dengan animasi pulse saat hover
        button_width = int(180 * scale)
        button_height = int(60 * scale)
        
        if card['hover']:
            pulse = math.sin(pygame.time.get_ticks() * 0.008) * 5
            button_width += int(pulse)
            button_height += int(pulse * 0.5)
        
        button_x = x + card_width // 2 - button_width // 2
        button_y = y + card_height - int(100 * scale)
        
        # Bayangan tombol
        shadow_button = pygame.Rect(button_x + 3, button_y + 3, button_width, button_height)
        self.draw_rounded_rect(self.screen, self.BUTTON_DARK, shadow_button, 25)
        
        # Tombol utama
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.draw_rounded_rect(self.screen, self.BUTTON_DARK, button_rect, 25)
        
        button_inner = pygame.Rect(
            button_x + 5, 
            button_y + 5, 
            button_width - 10, 
            button_height - 10
        )
        self.draw_rounded_rect(self.screen, self.BUTTON_GREEN, button_inner, 20)
        
        # Teks tombol
        button_font_size = int(50 * scale)
        button_font = pygame.font.Font(None, button_font_size)
        play_text = button_font.render("Play", True, self.TEXT_WHITE)
        play_x = button_x + button_width // 2 - play_text.get_width() // 2
        play_y = button_y + button_height // 2 - play_text.get_height() // 2
        self.screen.blit(play_text, (play_x, play_y))
        
        return button_rect
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for card in self.cards:
                # Cek hover pada card
                card_rect = pygame.Rect(
                    card['pos'][0], 
                    card['pos'][1], 
                    int(400 * card['scale']), 
                    int(280 * card['scale'])
                )
                if card_rect.collidepoint(mouse_pos):
                    card['hover'] = True
                    card['target_scale'] = 1.08
                else:
                    card['hover'] = False
                    card['target_scale'] = 1.0
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, card in enumerate(self.cards):
                card_rect = pygame.Rect(
                    card['pos'][0], 
                    card['pos'][1], 
                    int(400 * card['scale']), 
                    int(280 * card['scale'])
                )
                if card_rect.collidepoint(mouse_pos):
                    plant_name = card['name'].lower()
                    print(f"Memilih tanaman: {plant_name}")
                    # Transisi ke growth scene
                    self.scene_manager.change_scene(card['scene'])
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Kembali ke menu kategori
                self.scene_manager.change_scene("pilih_kategori")
    
    def update(self, dt):
        """Update animasi"""
        self.animation_timer += dt
        
        # Animasi masuk kartu dari samping dan bawah
        if self.animation_timer > 0.1:
            self.cards[0]['target_pos'][0] = 100
        if self.animation_timer > 0.3:
            self.cards[1]['target_pos'][0] = 700
        if self.animation_timer > 0.5:
            self.cards[2]['target_pos'][1] = 450
    
    def draw(self):
        """Render scene"""
        # Background
        self.screen.blit(self.background, (0, 0))
        
        # Judul dengan shadow
        title = self.font_title.render("Pilih Sayur Favoritmu!", True, self.TEXT_WHITE)
        title_shadow = self.font_title.render("Pilih Sayur Favoritmu!", True, (50, 50, 50))
        title_x = self.width // 2 - title.get_width() // 2
        self.screen.blit(title_shadow, (title_x + 3, 33))
        self.screen.blit(title, (title_x, 30))
        
        # Gambar semua kartu
        for i, card in enumerate(self.cards):
            self.draw_plant_card(card, i)
        
        # Instruksi
        info_font = pygame.font.Font(None, 40)
        info_text = info_font.render("Klik kartu untuk mulai menanam!", True, self.TEXT_WHITE)
        self.screen.blit(info_text, (self.width // 2 - info_text.get_width() // 2, self.height - 40))
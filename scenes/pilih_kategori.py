import pygame # type: ignore
import os
import sys

pygame.init()

# WINDOW
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pilih Kategori - Bloomio")

background = pygame.image.load("assets/images/bg-kategori.png").convert()
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

font_level = pygame.font.Font("assets/fonts/Heyam.ttf", 38)
font_title = pygame.font.Font("assets/fonts/Heyam.ttf", 78)
font_button = pygame.font.Font("assets/fonts/Heyam.ttf", 40)

def create_card(level_number, title_text, y_pos):
    CARD_W, CARD_H = 520, 200   # ukuran figma
    card = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)

    # Warna card
    pygame.draw.rect(card, (255, 186, 97), (0, 0, CARD_W, CARD_H), border_radius=45)
    pygame.draw.rect(card, (150, 90, 40), (0, 0, CARD_W, CARD_H), 6, border_radius=45)

    # -- LEVEL TEXT --
    level_text = font_level.render(f"Level {level_number}", True, (255, 255, 255))
    card.blit(level_text, (25, 20))

    # -- JUDUL (SAYUR / BUAH), posisi tengah TIDAK MEPET --
    title = font_title.render(title_text, True, (80, 120, 65))
    tx = CARD_W//2 - title.get_width()//2
    card.blit(title, (tx, 60))

    # -- BUTTON SELECT --
    BTN_W, BTN_H = 150, 55
    btn_rect = pygame.Rect(CARD_W//2 - BTN_W//2, 130, BTN_W, BTN_H)

    pygame.draw.rect(card, (180, 230, 140), btn_rect, border_radius=30)
    pygame.draw.rect(card, (60, 90, 50), btn_rect, 4, border_radius=30)

    btn_text = font_button.render("Select", True, (255, 255, 255))
    card.blit(btn_text, (
        btn_rect.x + BTN_W//2 - btn_text.get_width()//2,
        btn_rect.y + BTN_H//2 - btn_text.get_height()//2
    ))

    # posisi di layar
    rect = card.get_rect(center=(WIDTH//2, y_pos))

    return card, rect, btn_rect

card_sayur, rect_sayur, btn_sayur = create_card(1, "SAYUR", 250)
card_buah, rect_buah, btn_buah = create_card(2, "BUAH", 460)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos

            # Klik SAYUR -> halaman pilih sayur
            if rect_sayur.collidepoint(mx, my):
                bx, by = mx - rect_sayur.x, my - rect_sayur.y
                if btn_sayur.collidepoint(bx, by):
                    pygame.quit()
                    os.system("python scenes/pilih_sayur.py")
                    sys.exit()

            # Klik BUAH -> halaman pilih buah
            if rect_buah.collidepoint(mx, my):
                bx, by = mx - rect_buah.x, my - rect_buah.y
                if btn_buah.collidepoint(bx, by):
                    pygame.quit()
                    os.system("python scenes/pilih_buah.py")
                    sys.exit()

    # Render
    screen.blit(background, (0, 0))
    screen.blit(card_sayur, rect_sayur)
    screen.blit(card_buah, rect_buah)

    pygame.display.flip()

pygame.quit()
import pygame
import math
import os

class PilihKategori:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Load background
        bg_path = os.path.join('assets', 'images', 'bg-select.png')
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        # Load custom font - UPDATED to use Joyful.ttf
        font_path = os.path.join('assets', 'fonts', 'Joyful.ttf')
        try:
            self.font_title = pygame.font.Font(font_path, 80)
            self.font_level = pygame.font.Font(font_path, 70)
            self.font_desc = pygame.font.Font(font_path, 35)
        except:
            print("Warning: Joyful.ttf not found, using default font")
            self.font_title = pygame.font.Font(None, 80)
            self.font_level = pygame.font.Font(None, 70)
            self.font_desc = pygame.font.Font(None, 35)
        
        # Warna
        self.CARD_BG = (255, 209, 128)
        self.CARD_BORDER = (219, 123, 43)
        self.TEXT_WHITE = (255, 255, 255)
        self.TEXT_GREEN = (88, 129, 87)
        self.VEGETABLE_COLOR = (100, 180, 100)
        self.FRUIT_COLOR = (220, 100, 100)
        
        # Data level cards
        self.cards = [
            {
                'level': 'Level 1',
                'category': 'SAYURAN',
                'desc': 'Pakcoy • Seledri • Selada',
                'color': self.VEGETABLE_COLOR,
                'scene': 'pilih_sayur',
                'pos': [200, 300],
                'target_pos': [200, 300],
                'scale': 1.0,
                'target_scale': 1.0,
                'hover': False
            },
            {
                'level': 'Level 2',
                'category': 'BUAH-BUAHAN',
                'desc': 'Stroberi • Apel • Melon',
                'color': self.FRUIT_COLOR,
                'scene': 'pilih_buah',
                'pos': [700, 300],
                'target_pos': [700, 300],
                'scale': 1.0,
                'target_scale': 1.0,
                'hover': False
            }
        ]
        
        # Animasi entrance
        self.cards[0]['pos'][0] = -500
        self.cards[1]['pos'][0] = self.width + 500
        
        self.animation_timer = 0
    
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Menggambar persegi dengan sudut melengkung"""
        if len(color) == 4:
            temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, color, temp_surface.get_rect(), border_radius=radius)
            surface.blit(temp_surface, (rect.x, rect.y))
        else:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_card(self, card):
        """Menggambar kartu level"""
        x, y = card['pos']
        scale = card['scale']
        
        card_width = int(380 * scale)
        card_height = int(400 * scale)
        
        # Smooth interpolation
        card['pos'][0] += (card['target_pos'][0] - card['pos'][0]) * 0.15
        card['pos'][1] += (card['target_pos'][1] - card['pos'][1]) * 0.15
        card['scale'] += (card['target_scale'] - card['scale']) * 0.2
        
        x = int(card['pos'][0])
        y = int(card['pos'][1])
        
        # Hover bounce
        if card['hover']:
            bounce = math.sin(pygame.time.get_ticks() * 0.005) * 8
            y += int(bounce)
        
        # Shadow
        shadow_rect = pygame.Rect(x + 8, y + 8, card_width, card_height)
        self.draw_rounded_rect(self.screen, (50, 50, 50, 120), shadow_rect, 35)
        
        # Border
        border_rect = pygame.Rect(x, y, card_width, card_height)
        self.draw_rounded_rect(self.screen, self.CARD_BORDER, border_rect, 35)
        
        # Background
        inner_rect = pygame.Rect(x + 10, y + 10, card_width - 20, card_height - 20)
        self.draw_rounded_rect(self.screen, self.CARD_BG, inner_rect, 30)
        
        # Level badge dengan warna kategori
        badge_width = int(card_width * 0.8)
        badge_height = int(80 * scale)
        badge_x = x + (card_width - badge_width) // 2
        badge_y = y + int(40 * scale)
        
        badge_rect = pygame.Rect(badge_x, badge_y, badge_width, badge_height)
        self.draw_rounded_rect(self.screen, card['color'], badge_rect, 20)
        
        # Level text
        font_size = int(50 * scale)
        level_font = pygame.font.Font(None, font_size) if not hasattr(self, 'font_level') else self.font_level
        level_text = level_font.render(card['level'], True, self.TEXT_WHITE)
        level_x = badge_x + badge_width // 2 - level_text.get_width() // 2
        level_y = badge_y + badge_height // 2 - level_text.get_height() // 2
        self.screen.blit(level_text, (level_x, level_y))
        
        # Category name
        cat_font_size = int(60 * scale)
        cat_font = pygame.font.Font(None, cat_font_size)
        cat_shadow = cat_font.render(card['category'], True, card['color'])
        cat_text = cat_font.render(card['category'], True, self.TEXT_GREEN)
        
        cat_x = x + card_width // 2 - cat_text.get_width() // 2
        cat_y = badge_y + badge_height + int(50 * scale)
        
        self.screen.blit(cat_shadow, (cat_x + 3, cat_y + 3))
        self.screen.blit(cat_text, (cat_x, cat_y))
        
        # Description
        desc_font_size = int(28 * scale)
        desc_font = pygame.font.Font(None, desc_font_size)
        desc_text = desc_font.render(card['desc'], True, self.TEXT_GREEN)
        desc_x = x + card_width // 2 - desc_text.get_width() // 2
        desc_y = cat_y + int(70 * scale)
        self.screen.blit(desc_text, (desc_x, desc_y))
        
        return pygame.Rect(x, y, card_width, card_height)
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for card in self.cards:
                card_rect = pygame.Rect(
                    card['pos'][0], 
                    card['pos'][1], 
                    int(380 * card['scale']), 
                    int(400 * card['scale'])
                )
                if card_rect.collidepoint(mouse_pos):
                    card['hover'] = True
                    card['target_scale'] = 1.08
                else:
                    card['hover'] = False
                    card['target_scale'] = 1.0
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for card in self.cards:
                card_rect = pygame.Rect(
                    card['pos'][0], 
                    card['pos'][1], 
                    int(380 * card['scale']), 
                    int(400 * card['scale'])
                )
                if card_rect.collidepoint(mouse_pos):
                    print(f"Memilih kategori: {card['category']}")
                    self.scene_manager.change_scene(card['scene'])
    
    def update(self, dt):
        """Update animasi"""
        self.animation_timer += dt
        
        if self.animation_timer > 0.2:
            self.cards[0]['target_pos'][0] = 200
        if self.animation_timer > 0.4:
            self.cards[1]['target_pos'][0] = 700
    
    def draw(self):
        """Render scene"""
        # Background
        self.screen.blit(self.background, (0, 0))
        
        # Title with custom font
        title = self.font_title.render("Pilih Level", True, self.TEXT_WHITE)
        title_shadow = self.font_title.render("Pilih Level", True, (50, 50, 50))
        title_x = self.width // 2 - title.get_width() // 2
        self.screen.blit(title_shadow, (title_x + 3, 53))
        self.screen.blit(title, (title_x, 50))
        
        # Draw cards
        for card in self.cards:
            self.draw_card(card)

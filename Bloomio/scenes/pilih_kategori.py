import pygame # type: ignore
import os
import sys

pygame.init()

# WINDOW
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pilih Kategori - Bloomio")

# ============================
# BACKGROUND
# ============================
background = pygame.image.load("assets/images/bg-kategori.png").convert()
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

# ============================
# FONTS
# ============================
font_level = pygame.font.Font("assets/fonts/Heyam.ttf", 38)
font_title = pygame.font.Font("assets/fonts/Heyam.ttf", 78)
font_button = pygame.font.Font("assets/fonts/Heyam.ttf", 40)

# ============================
# CREATE CARD (FINAL FIT FIGMA)
# ============================
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


# ============================
# CREATE BOTH CARDS
# ============================
card_sayur, rect_sayur, btn_sayur = create_card(1, "SAYUR", 250)
card_buah, rect_buah, btn_buah = create_card(2, "BUAH", 460)

# ============================
# GAME LOOP
# ============================
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

import pygame # type: ignore
import cairo # type: ignore
import math
import subprocess
import sys
import os

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bloomio - Main Menu")

#bg langit
def draw_background():
    bg = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = (1 - t) * 0.56 + t * 1
        g = (1 - t) * 0.90 + t * 1
        b = (1 - t) * 1.00 + t * 1
        pygame.draw.line(bg, (int(r*255), int(g*255), int(b*255)), (0, y), (WIDTH, y))
    return bg

background = draw_background()

#awan
def make_cloud(scale=1.0):
    w, h = int(260 * scale), int(130 * scale)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)

    pygame.draw.circle(surf, (255, 255, 255), (60, 70), int(40 * scale))
    pygame.draw.circle(surf, (255, 255, 255), (110, 60), int(40 * scale))
    pygame.draw.circle(surf, (255, 255, 255), (160, 65), int(40 * scale))
    pygame.draw.circle(surf, (255, 255, 255), (210, 75), int(35 * scale))

    return surf

clouds = [
    [make_cloud(1.0), 60, 70, 0.08],
    [make_cloud(0.85), 250, 150, 0.08],
    [make_cloud(1.0), 650, 80, 0.08],
    [make_cloud(0.85), 820, 160, 0.08],
]

#buah homepage
fruits = pygame.image.load("assets/images/buah_homepage.png").convert_alpha()
fruits = pygame.transform.smoothscale(fruits, (1000, 350))

#tombol START (background)
button_panel = pygame.Surface((360, 140), pygame.SRCALPHA)
pygame.draw.rect(button_panel, (255, 200, 120), (0, 0, 360, 140), border_radius=40)
pygame.draw.rect(button_panel, (180, 110, 40), (0, 0, 360, 140), 6, border_radius=40)

button_rect = button_panel.get_rect(center=(WIDTH // 2, 420))

title_font = pygame.font.Font("assets/fonts/heyam/Heyam.ttf", 130)
subtitle_font = pygame.font.Font("assets/fonts/heyam/Heyam.ttf", 42)
start_font = pygame.font.Font("assets/fonts/heyam/Heyam.ttf", 70)

title_text = title_font.render("BLOOMIO", True, (255, 182, 210))
title_shadow = title_font.render("BLOOMIO", True, (170, 100, 150))

subtitle_text = subtitle_font.render("Grow Your Plants", True, (50, 50, 50))

start_text = start_font.render("START", True, (255, 255, 255))
start_shadow = start_font.render("START", True, (240, 240, 240))

#animasi
pulse_t = 0
running = True
scene = "menu"

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if button_rect.collidepoint(e.pos):
                pygame.quit()
                os.system("python scenes/pilih_kategori.py")   #ubah ini untuk next page
                sys.exit()

    if scene == "menu":
        # BG
        screen.blit(background, (0, 0))

        #gerak awan
        for cloud in clouds:
            img, x, y, spd = cloud
            x += spd
            if x > WIDTH:
                x = -200
            cloud[1] = x
            screen.blit(img, (x, y))

        #buah homepage
        screen.blit(fruits, (0, 300))

        #judul BLOOMIO
        tx = WIDTH // 2 - title_text.get_width() // 2
        ty = 150
        screen.blit(title_shadow, (tx + 6, ty + 6))
        screen.blit(title_text, (tx, ty))

        #subtitle
        screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, 280))

        #animasi tombol 
        pulse_t += 0.01
        scale = 1 + 0.03 * math.sin(pulse_t)

        btn_scaled = pygame.transform.smoothscale(
            button_panel,
            (int(360 * scale), int(140 * scale))
        )
        btn_rect = btn_scaled.get_rect(center=button_rect.center)

        screen.blit(btn_scaled, btn_rect)

        #tulisan start
        sx = btn_rect.centerx - start_text.get_width() // 2
        sy = btn_rect.centery - start_text.get_height() // 2
        screen.blit(start_shadow, (sx + 3, sy + 3))
        screen.blit(start_text, (sx, sy))

    else:
        screen.fill((220, 240, 255))
        f = pygame.font.SysFont("Arial", 60)
        t = f.render("Ini halaman berikutnya", True, (70, 70, 70))
        screen.blit(t, (220, 300))

    pygame.display.flip()

pygame.quit()



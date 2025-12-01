import pygame
import math

def draw_rounded_rect(surface, color, rect, radius):
    """
    Menggambar persegi dengan sudut melengkung
    
    Args:
        surface: pygame surface untuk menggambar
        color: warna (R, G, B) atau (R, G, B, A)
        rect: pygame.Rect object
        radius: radius sudut melengkung
    """
    if len(color) == 4:
        # Jika ada alpha channel, buat surface baru untuk transparency
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color, temp_surface.get_rect(), border_radius=radius)
        surface.blit(temp_surface, (rect.x, rect.y))
    else:
        pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_cloud(surface, x, y, size=1, color=(160, 160, 160)):
    """
    Menggambar awan menggunakan beberapa lingkaran
    
    Args:
        surface: pygame surface
        x, y: posisi tengah awan
        size: skala ukuran awan
        color: warna awan
    """
    pygame.draw.circle(surface, color, (int(x), int(y)), int(30 * size))
    pygame.draw.circle(surface, color, (int(x + 25 * size), int(y - 10 * size)), int(35 * size))
    pygame.draw.circle(surface, color, (int(x + 50 * size), int(y)), int(30 * size))
    pygame.draw.circle(surface, color, (int(x + 70 * size), int(y + 5 * size)), int(25 * size))


def draw_tree(surface, x, y, size=1, tree_color=(67, 104, 80), trunk_color=(101, 67, 33)):
    """
    Menggambar pohon sederhana
    
    Args:
        surface: pygame surface
        x, y: posisi dasar batang pohon
        size: skala ukuran pohon
        tree_color: warna daun
        trunk_color: warna batang
    """
    # Batang
    trunk_rect = pygame.Rect(
        int(x - 8 * size), 
        int(y - 30 * size), 
        int(16 * size), 
        int(40 * size)
    )
    pygame.draw.rect(surface, trunk_color, trunk_rect)
    
    # Daun (3 lingkaran membentuk pohon)
    pygame.draw.circle(surface, tree_color, (int(x - 15 * size), int(y - 40 * size)), int(25 * size))
    pygame.draw.circle(surface, tree_color, (int(x + 15 * size), int(y - 40 * size)), int(25 * size))
    pygame.draw.circle(surface, tree_color, (int(x), int(y - 60 * size)), int(30 * size))


def draw_sun(surface, x, y, radius=40, color=(255, 220, 100)):
    """
    Menggambar matahari dengan sinar
    
    Args:
        surface: pygame surface
        x, y: posisi tengah matahari
        radius: radius matahari
        color: warna matahari
    """
    # Gambar sinar
    ray_length = radius * 1.5
    num_rays = 12
    for i in range(num_rays):
        angle = (360 / num_rays) * i
        rad = math.radians(angle)
        
        start_x = x + math.cos(rad) * radius
        start_y = y + math.sin(rad) * radius
        end_x = x + math.cos(rad) * ray_length
        end_y = y + math.sin(rad) * ray_length
        
        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 3)
    
    # Gambar lingkaran matahari
    pygame.draw.circle(surface, color, (int(x), int(y)), radius)
    
    # Highlight
    highlight_color = (255, 255, 200)
    pygame.draw.circle(surface, highlight_color, (int(x - 10), int(y - 10)), int(radius * 0.3))


def draw_grass_blades(surface, x, y, count=5, height=20, color=(100, 180, 100)):
    """
    Menggambar rumput kecil
    
    Args:
        surface: pygame surface
        x, y: posisi dasar rumput
        count: jumlah helai rumput
        height: tinggi rumput
        color: warna rumput
    """
    for i in range(count):
        offset_x = (i - count // 2) * 5
        blade_height = height + (i % 3) * 5
        
        # Gambar helai rumput sebagai garis melengkung
        start = (x + offset_x, y)
        control = (x + offset_x + 3, y - blade_height // 2)
        end = (x + offset_x, y - blade_height)
        
        # Simulasi kurva dengan beberapa line segment
        points = []
        for t in range(11):
            t = t / 10.0
            # Quadratic bezier curve
            px = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
            py = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
            points.append((px, py))
        
        pygame.draw.lines(surface, color, False, points, 2)


def draw_flower(surface, x, y, size=1, petal_color=(255, 100, 150), center_color=(255, 200, 50)):
    """
    Menggambar bunga sederhana
    
    Args:
        surface: pygame surface
        x, y: posisi tengah bunga
        size: skala ukuran
        petal_color: warna kelopak
        center_color: warna tengah bunga
    """
    # Gambar 5 kelopak
    petal_radius = int(15 * size)
    center_radius = int(10 * size)
    
    for i in range(5):
        angle = (360 / 5) * i - 90
        rad = math.radians(angle)
        petal_x = x + math.cos(rad) * center_radius
        petal_y = y + math.sin(rad) * center_radius
        pygame.draw.circle(surface, petal_color, (int(petal_x), int(petal_y)), petal_radius)
    
    # Tengah bunga
    pygame.draw.circle(surface, center_color, (int(x), int(y)), center_radius)


def draw_water_drop(surface, x, y, size=1, color=(100, 180, 255)):
    """
    Menggambar tetesan air
    
    Args:
        surface: pygame surface
        x, y: posisi tengah tetesan
        size: skala ukuran
        color: warna air
    """
    # Bentuk tetesan menggunakan polygon
    points = [
        (x, y - 15 * size),  # Atas (runcing)
        (x + 8 * size, y - 5 * size),  # Kanan atas
        (x + 10 * size, y + 5 * size),  # Kanan bawah
        (x, y + 12 * size),  # Bawah
        (x - 10 * size, y + 5 * size),  # Kiri bawah
        (x - 8 * size, y - 5 * size),  # Kiri atas
    ]
    
    pygame.draw.polygon(surface, color, points)
    
    # Highlight
    highlight_color = (200, 230, 255)
    pygame.draw.circle(surface, highlight_color, (int(x - 3 * size), int(y - 3 * size)), int(3 * size))


def draw_sparkle(surface, x, y, size=1, color=(255, 255, 200)):
    """
    Menggambar efek kilauan bintang
    
    Args:
        surface: pygame surface
        x, y: posisi tengah sparkle
        size: skala ukuran
        color: warna sparkle
    """
    length = int(10 * size)
    
    # Garis vertikal
    pygame.draw.line(surface, color, (x, y - length), (x, y + length), 2)
    
    # Garis horizontal
    pygame.draw.line(surface, color, (x - length, y), (x + length, y), 2)
    
    # Diagonal
    diag_offset = int(length * 0.7)
    pygame.draw.line(surface, color, 
                    (x - diag_offset, y - diag_offset), 
                    (x + diag_offset, y + diag_offset), 2)
    pygame.draw.line(surface, color, 
                    (x + diag_offset, y - diag_offset), 
                    (x - diag_offset, y + diag_offset), 2)
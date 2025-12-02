import pygame
import sys
# from scenes.homepage import Homepage
# from scenes.pilih_kategori import PilihKategori
from scenes.pilih_buah import PilihBuah
from scenes.pilih_sayur import PilihSayur
from scenes.strawberry import GrowthStroberi
from scenes.bayam import GrowthBayam
from scenes.apel import GrowthApel
from scenes.seledri import GrowthSeledri
from scenes.apresiasi import Apresiasi

class SceneManager:
    """Manager untuk mengelola perpindahan scene"""
    def __init__(self, screen):
        self.screen = screen
        self.scenes = {}
        self.current_scene_name = None
        self.current_scene = None
        
    def register_scene(self, name, scene_class):
        """Register scene baru"""
        self.scenes[name] = scene_class
        
    def change_scene(self, scene_name, **kwargs):
        """Ganti ke scene baru"""
        print(f"Changing to scene: {scene_name}")
        if scene_name in self.scenes:
            self.current_scene_name = scene_name
            self.current_scene = self.scenes[scene_name](self.screen, self, **kwargs)
        else:
            print(f"Warning: Scene '{scene_name}' not found!")
            
    def get_current_scene(self):
        """Ambil scene yang sedang aktif"""
        return self.current_scene

def main():
    # Inisialisasi Pygame
    pygame.init()
    
    # Setup layar
    WIDTH, HEIGHT = 1200, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bloomio - Educational Plant Game")
    
    clock = pygame.time.Clock()
    FPS = 60
    
    # Scene manager
    scene_manager = SceneManager(screen)
    
    # Register semua scene
    # scene_manager.register_scene("homepage", Homepage)
    # scene_manager.register_scene("pilih_kategori", PilihKategori)
    scene_manager.register_scene("pilih_buah", PilihBuah)
    scene_manager.register_scene("pilih_sayur", PilihSayur)
    scene_manager.register_scene("strawberry", GrowthStroberi)
    scene_manager.register_scene("bayam", GrowthBayam)
    scene_manager.register_scene("apel", GrowthApel)
    scene_manager.register_scene("seledri", GrowthSeledri)
    scene_manager.register_scene("apresiasi", Apresiasi)

    # Mulai dari homepage
    # scene_manager.change_scene("homepage")
    scene_manager.change_scene("pilih_buah")
    
    running = True
    
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time dalam detik
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # Pass event ke scene aktif
            current_scene = scene_manager.get_current_scene()
            if current_scene:
                current_scene.handle_event(event)
        
        # Update scene
        current_scene = scene_manager.get_current_scene()
        if current_scene:
            current_scene.update(dt)
            current_scene.draw()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
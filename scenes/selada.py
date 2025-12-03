import pygame # type: ignore
import math
import random
import os

class GrowthLettuce:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Background
        bg_path = os.path.join("assets", "images", "bg-buah.png")
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Fonts
        font_path = os.path.join("assets", "fonts", "Heyam.ttf")
        digits_path = os.path.join("assets", "fonts", "Super Joyful.ttf")
        try:
            self.font_stage = pygame.font.Font(font_path, 40)
            self.font_button = pygame.font.Font(font_path, 30)
            self.font_small = pygame.font.Font(font_path, 24)
            self.font_digits = pygame.font.Font(digits_path, 28)
        except:
            self.font_stage = pygame.font.Font(None, 40)
            self.font_button = pygame.font.Font(None, 30)
            self.font_small = pygame.font.Font(None, 24)
            self.font_digits = pygame.font.Font(digits_path, 28)

        # Colors
        self.WHITE = (255, 255, 255)
        self.WATER_BLUE = (135, 206, 250)
        self.BUTTON_GREEN = (126, 176, 105)

        self.LEAF_LIGHT = (120, 230, 120)
        self.LEAF_MEDIUM = (80, 190, 80)
        self.LEAF_DARK = (50, 150, 60)

        self.SOIL_BROWN = (101, 67, 33)
        self.SOIL_DARK = (76, 50, 25)

        # Growth stages
        self.stages = [
            "Biji",
            "Kecambah",
            "Vegetatif",
            "Generatif",
            "Panen"
        ]

        # Fun Fact System
        self.show_fact = False
        self.funfact_shown = False   
        self.fact_text = [
            "Selada adalah sayuran berdaun yang pertama kali dibudidayakan oleh bangsa Mesir.",
            "Selada mengandung 95% air, sehingga sangat menyegarkan!",
            "Selada kaya vitamin A dan K, baik untuk kulit dan tulang.",
            "Selada tumbuh paling baik pada suhu 15-20°C."
        ]
        self.current_fact = ""

        self.current_stage = 0
        self.growth_progress = 0

        self.stage_requirements = [12, 25, 40, 55]  

        # Nutrients
        self.water_level = 30
        self.sunlight_level = 30
        self.fertilizer_level = 30

        self.water_consumption = 2
        self.sunlight_consumption = 2
        self.fertilizer_consumption = 2

        self.fertilizer_used = False

        self.fruit_positions = []       
        self.harvested_fruits = []      
        self.total_harvested = 0        

        # Cloud
        self.cloud = {
            'x': self.width//4,
            'y': 100,
            'width': 150,
            'height': 80,
            'dragging': False,
            'raining': False,
            'rain_drops': []
        }

        # Sun
        self.sun = {
            'x': self.width - 150,
            'y': 100,
            'radius': 50,
            'glow': 0
        }

        # Fertilizer bag
        self.fertilizer_bag = {
            'x': self.width - 200,
            'y': self.height - 200,
            'width': 80,
            'height': 100
        }

        self.message = ""
        self.message_timer = 0

        self.time = 0
        self.plant_sway = 0

    def draw_funfact_popup(self):
        if not self.show_fact:
            return

        # Background popup
        box_w, box_h = 600, 200
        box = pygame.Rect(
            self.width//2 - box_w//2,
            self.height//2 - box_h//2,
            box_w, box_h
        )

        pygame.draw.rect(self.screen, (0,0,0,180), box, border_radius=20)
        pygame.draw.rect(self.screen, self.WHITE, box, 3, border_radius=20)

        # Text
        fact = self.font_button.render("Fun Fact:", True, self.WHITE)
        self.screen.blit(fact, (box.x + 20, box.y + 20))

        wrapped = []
        words = self.current_fact.split(" ")
        line = ""

        for w in words:
            test = line + w + " "
            if self.font_small.size(test)[0] > box_w - 40:
                wrapped.append(line)
                line = w + " "
            else:
                line = test
        wrapped.append(line)

        y_offset = 70
        for ln in wrapped:
            txt = self.font_small.render(ln, True, self.WHITE)
            self.screen.blit(txt, (box.x + 20, box.y + y_offset))
            y_offset += 28

        # Close button
        close = pygame.Rect(box.centerx - 60, box.bottom - 55, 120, 40)
        pygame.draw.rect(self.screen, self.BUTTON_GREEN, close, border_radius=12)
        pygame.draw.rect(self.screen, self.WHITE, close, 2, border_radius=12)

        t = self.font_button.render("Tutup", True, self.WHITE)
        self.screen.blit(t, (close.centerx - t.get_width()//2,
                            close.centery - t.get_height()//2))

        self.close_button_rect = close

    def draw_sky(self):
        cx, cy = self.cloud['x'], self.cloud['y']

        # cloud
        pygame.draw.ellipse(self.screen, (200,200,200), (cx+5,cy+5,60,40))
        pygame.draw.ellipse(self.screen, self.WHITE, (cx,cy,60,40))
        pygame.draw.ellipse(self.screen, self.WHITE, (cx+40,cy,70,50))
        pygame.draw.ellipse(self.screen, self.WHITE, (cx+80,cy,60,40))

        if self.cloud['raining']:
            for d in self.cloud['rain_drops']:
                pygame.draw.line(self.screen, self.WATER_BLUE,
                                 (d['x'], d['y']),
                                 (d['x'], d['y']+8), 2)

        # sun
        sx, sy = self.sun['x'], self.sun['y']
        r = self.sun['radius']

        glow_intensity = int(self.sun['glow'])
        for i in range(3):
            glow_radius = r + 20 - (i * 7)
            glow_alpha = 30 - (i * 10)
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 0, glow_alpha),
                              (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surf, (sx - glow_radius, sy - glow_radius))

        for i in range(12):
            ang = math.radians(i*30 + self.time*10)
            pygame.draw.line(self.screen, (255,220,0),
                             (sx + math.cos(ang)*r, sy + math.sin(ang)*r),
                             (sx + math.cos(ang)*(r+25), sy + math.sin(ang)*(r+25)), 4)

        pygame.draw.circle(self.screen, (255,200,0), (sx,sy), r)
        pygame.draw.circle(self.screen, (255,230,90), (sx,sy), r-5)
        pygame.draw.circle(self.screen, (255,255,200), (sx - 10,sy - 10), 15)

    def draw_lettuce_harvest(self, x, y):
        # posisi "buah" selada yang bisa diklik
        self.fruit_positions = [
            (x - 40, y - 80),
            (x,      y - 100),
            (x + 40, y - 85),
        ]

        for i, (fx, fy) in enumerate(self.fruit_positions):

            if i in [f['id'] for f in self.harvested_fruits]:
                continue

            # buah selada (simbol mini lettuce) → PAKAI fx, fy
            pygame.draw.circle(self.screen, (120,230,120), (fx, fy), 15)
            pygame.draw.circle(self.screen, (80,160,80), (fx-5, fy-5), 8)

    def draw_soil(self):
        self.soil_y = self.height - 170
        pygame.draw.rect(self.screen, self.SOIL_DARK,
                         (0, self.soil_y+45, self.width, 300))
        pygame.draw.rect(self.screen, self.SOIL_BROWN,
                         (0, self.soil_y, self.width, 45))

    def draw_plant(self):
        cx = self.width // 2
        soil_y = self.soil_y
        sway = math.sin(self.plant_sway) * 3

        # Tahap 0 — Biji
        if self.current_stage == 0:
            pygame.draw.ellipse(self.screen, (80, 50, 20),
                                (cx-8, soil_y+18, 16, 10))
            return

        # Tahap 1 — Kecambah
        if self.current_stage == 1:
            pygame.draw.line(self.screen, (60, 150, 70),
                            (cx, soil_y), (cx + sway, soil_y - 25), 4)
            self.draw_lettuce_leaf(cx - 12, soil_y - 32, size=18, angle=-15)
            self.draw_lettuce_leaf(cx + 12, soil_y - 32, size=18, angle=15)
            return

        # Tahap 2 — Vegetatif Awal
        if self.current_stage == 2:
            pygame.draw.line(self.screen, (60, 150, 70),
                            (cx, soil_y), (cx + sway, soil_y - 30), 4)
            for dx in [-35, 35]:
                self.draw_lettuce_leaf(cx + dx, soil_y - 50, size=28, angle=dx)
            return

        # Tahap 3 — Vegetatif Besar (perbaiki batang biar nggak LDR)
        if self.current_stage == 3:
            stem_top_y = soil_y - 55  # sebelumnya -25 (terlalu pendek)
            pygame.draw.line(self.screen, (60, 150, 70),
                            (cx, soil_y), (cx + sway, stem_top_y), 4)
            for dx in [-60, -30, 0, 30, 60]:
                self.draw_lettuce_leaf(cx + dx, soil_y - 70, size=40, angle=dx//2)
            return

        # Tahap 4 — PANEN → daun + buah panen (batang juga dipanjangkan)
        if self.current_stage == 4:
            stem_top_y = soil_y - 70   # dekat dengan daun besar
            pygame.draw.line(self.screen, (60, 150, 70),
                            (cx, soil_y), (cx + sway, stem_top_y), 4)

            for dx in [-80, -50, -20, 0, 20, 50, 80]:
                self.draw_lettuce_leaf(cx + dx, soil_y - 85, size=55, angle=dx//2)

            # *** Gambar buah untuk dipanen ***
            self.draw_lettuce_harvest(cx, soil_y)

    def draw_lettuce_leaf(self, x, y, size=40, angle=0):
        """Daun selada keriting berbentuk roset."""
        leaf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)

        pts = []
        for i in range(36):
            ang = math.radians(i * 10)
            r = size * (0.85 + 0.15 * math.sin(i * 2))
            px = size + math.cos(ang) * r
            py = size + math.sin(ang) * r
            pts.append((px, py))

        pygame.draw.polygon(leaf, (140, 240, 120), pts)
        pygame.draw.polygon(leaf, (80, 170, 70), pts, 2)

        cx0, cy0 = size, size
        for i in range(6):
            a = math.radians(i * 60)
            ex = cx0 + math.cos(a) * size * 0.6
            ey = cy0 + math.sin(a) * size * 0.6
            pygame.draw.line(leaf, (90, 160, 90), (cx0, cy0), (ex, ey), 2)

        leaf = pygame.transform.rotate(leaf, angle)
        rect = leaf.get_rect(center=(x, y))
        self.screen.blit(leaf, rect)

    def draw_fertilizer_bag(self):
        bag = self.fertilizer_bag
        x, y, w, h = bag['x'], bag['y'], bag['width'], bag['height']

        pygame.draw.rect(self.screen, (60, 40, 20), (x+4, y+4, w, h), border_radius=10)
        pygame.draw.rect(self.screen, (190, 140, 70), (x, y, w, h), border_radius=10)
        pygame.draw.rect(self.screen, (90, 50, 20), (x, y, w, h), 3, border_radius=10)

        txt = self.font_small.render("PUPUK", True, (60,30,10))
        self.screen.blit(txt, (x + w//2 - txt.get_width()//2, y + h//2 - txt.get_height()//2))

    def harvest_fruit(self, mouse):
        if self.current_stage < len(self.stages) - 1:
            return

        for i, (fx, fy) in enumerate(self.fruit_positions):
            if i in [f['id'] for f in self.harvested_fruits]:
                continue

            if math.dist(mouse, (fx, fy)) < 35:
                # animasi jatuh
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
                self.show_message(f"Panen {self.total_harvested}/3")

                # FUN FACT: hanya sekali (panen pertama)
                if not self.funfact_shown:
                    self.current_fact = random.choice(self.fact_text)
                    self.show_fact = True
                    self.funfact_shown = True

                # Jika sudah panen semua → pindah ke apresiasi
                if self.total_harvested >= 3:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
                    self.show_message("Semua buah berhasil dipanen!")

                break

    def draw_ui(self):
        bg = pygame.Rect(self.width//2-200, 20, 400, 25)
        pygame.draw.rect(self.screen, (40,40,40), bg, border_radius=12)

        if self.current_stage < 4:
            req = self.stage_requirements[self.current_stage]
            pw = int((self.growth_progress/req)*380)
            pygame.draw.rect(self.screen, (80,220,90),
                             (self.width//2-190,25,pw,15), border_radius=8)

        pygame.draw.rect(self.screen, self.WHITE, bg, 2, border_radius=12)

        txt = self.font_stage.render(self.stages[self.current_stage], True, self.WHITE)
        self.screen.blit(txt, (self.width//2 - txt.get_width()//2, 55))

        labels = [("Air", self.water_level, self.WATER_BLUE),
                  ("Cahaya", self.sunlight_level, (255,230,90)),
                  ("Pupuk", self.fertilizer_level, (120,200,120))]

        bx = 30
        by = 120
        bw = 200

        for i,(name,val,col) in enumerate(labels):
            y = by + i*45

            lb = self.font_button.render(name, True, self.WHITE)
            self.screen.blit(lb, (bx, y-5))

            pygame.draw.rect(self.screen, (50,50,50), (bx+120,y,bw,25), border_radius=12)
            pygame.draw.rect(self.screen, self.WHITE, (bx+120,y,bw,25),2,border_radius=12)

            fw = int((val/100)*bw)
            pygame.draw.rect(self.screen, col, (bx+120,y,fw,25), border_radius=12)

            pct = self.font_digits.render(f"{int(val)}%", True, self.WHITE)
            self.screen.blit(pct, (bx+120 + bw + 10, y))

        # back button
        back = pygame.Rect(self.width-150, self.height-70, 120, 50)
        pygame.draw.rect(self.screen, self.BUTTON_GREEN, back, border_radius=12)
        pygame.draw.rect(self.screen, self.WHITE, back, 2, border_radius=12)

        bt = self.font_button.render("Kembali", True, self.WHITE)
        self.screen.blit(bt, (back.centerx - bt.get_width()//2,
                               back.centery - bt.get_height()//2))
        
        # POPUP message
        if self.message_timer > 0:
            msg = self.font_digits.render(self.message, True, self.WHITE)
            self.screen.blit(msg, (
                self.width//2 - msg.get_width()//2,
                300
            ))

    def show_message(self, text):
        self.message = text
        self.message_timer = 2.0  # tampil selama 2 detik

    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.scene_manager.change_scene("apresiasi")
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            # kalau sudah tahap Panen → klik buat panen
            if self.current_stage == len(self.stages) - 1:
                self.harvest_fruit(event.pos)

            # kalau lagi buka fun fact → hanya handle tombol tutup
            if self.show_fact:
                if hasattr(self, "close_button_rect") and self.close_button_rect.collidepoint(event.pos):
                    self.show_fact = False
                return

            m = pygame.mouse.get_pos()

            back = pygame.Rect(self.width-150, self.height-70, 120, 50)
            if back.collidepoint(m):
                self.scene_manager.change_scene("pilih_buah")
                return

            # cloud
            r = pygame.Rect(self.cloud['x'],self.cloud['y'],
                            self.cloud['width'],self.cloud['height'])
            if r.collidepoint(m):
                self.cloud['dragging'] = True
                self.cloud['raining'] = True

            # sun
            if math.dist(m, (self.sun['x'],self.sun['y'])) < self.sun['radius']+30:
                self.sunlight_level = min(100, self.sunlight_level+25)
                self.sun['glow'] = 50
                self.show_message("Cahaya +25%!")

            # fertilizer
            bag = self.fertilizer_bag
            b = pygame.Rect(bag['x'], bag['y'], bag['width'], bag['height'])
            if b.collidepoint(m):
                self.fertilizer_level = min(100, self.fertilizer_level+25)
                self.fertilizer_used = True
                self.show_message("Pupuk +25%!")

        elif event.type == pygame.MOUSEMOTION:
            if self.cloud['dragging']:
                x = pygame.mouse.get_pos()[0]
                self.cloud['x'] = max(40, min(self.width-200, x-70))

        elif event.type == pygame.MOUSEBUTTONUP:
            self.cloud['dragging'] = False
            self.cloud['raining'] = False
            self.cloud['rain_drops'].clear()

    def update(self, dt):
        self.time += dt
        self.plant_sway += dt*2

        # RAIN / WATER 
        if self.cloud['raining']:
            if random.random() < 0.5:
                self.cloud['rain_drops'].append({
                    'x': self.cloud['x']+random.uniform(20,130),
                    'y': self.cloud['y']+70,
                    'vy': random.uniform(8,12)
                })

            for d in self.cloud['rain_drops'][:]:
                d['y'] += d['vy']
                if d['y'] > self.soil_y:

                    before = self.water_level
                    self.water_level = min(100, self.water_level+1.2)
                    self.cloud['rain_drops'].remove(d)

                    if self.water_level > before:
                        self.show_message("Air bertambah!")

        if self.message_timer > 0:
            self.message_timer -= dt

        # GROWTH CONDITIONS 
        enough = (
            self.water_level >= 60 and
            self.sunlight_level >= 60 and
            self.fertilizer_level >= 60
        )

        if enough and self.current_stage < len(self.stages) - 1:

            # Tambah progress
            self.growth_progress += 3 * dt  

            # CEK indeks sebelum akses requirement
            if self.current_stage < len(self.stage_requirements):

                req = self.stage_requirements[self.current_stage]

                if self.growth_progress >= req:
                    self.current_stage += 1
                    self.growth_progress = 0

            # Jika sudah masuk stage terakhir (Panen), stop perhitungan req
            else:
                self.growth_progress = 0

        # update animasi buah yang jatuh
        for fruit in self.harvested_fruits[:]:
            fruit['x'] += fruit['vx']
            fruit['y'] += fruit['vy']
            fruit['vy'] += 0.5
            fruit['rotation'] += fruit['rot_speed']

            if fruit['y'] > self.height + 50:
                self.harvested_fruits.remove(fruit)

        # ====== NUTRIENT DECAY ======
        self.water_level = max(0, self.water_level - 1 * dt)
        self.sunlight_level = max(0, self.sunlight_level - 1 * dt)
        self.fertilizer_level = max(0, self.fertilizer_level - 1 * dt)

        self.sun['glow'] = max(0, self.sun['glow'] - dt*50)

    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.draw_sky()
        self.draw_soil()
        self.draw_plant()
        self.draw_fertilizer_bag() # type: ignore

        # gambar buah yang jatuh (hasil panen)
        for fruit in self.harvested_fruits:
            fx, fy = int(fruit['x']), int(fruit['y'])
            surf = pygame.Surface((60,60), pygame.SRCALPHA)

            pygame.draw.circle(surf, (120,230,120), (30,30), 20)
            pygame.draw.circle(surf, (80,160,80), (25,25), 10)

            rot = pygame.transform.rotate(surf, fruit['rotation'])
            rect = rot.get_rect(center=(fx, fy))
            self.screen.blit(rot, rect)

        self.draw_ui()
        self.draw_funfact_popup()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 650))
    pygame.display.set_caption("TEST LETTUCE")

    class DummyManager:
        def change_scene(self, x):
            print("Change scene:", x)

    scene = GrowthLettuce(screen, DummyManager())
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            scene.handle_event(e)  # type: ignore

        scene.update(dt)
        scene.draw()
        pygame.display.flip()

    pygame.quit()

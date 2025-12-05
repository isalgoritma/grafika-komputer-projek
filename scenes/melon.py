import pygame # type: ignore
import math
import random
import os

class GrowthMelon:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.width = screen.get_width()
        self.height = screen.get_height()

        #Background
        bg_path = os.path.join("assets", "images", "bg-select.png")
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        #Fonts
        font_path = os.path.join("assets", "fonts", "Heyam.ttf")
        digits_path = os.path.join("assets", "fonts", "Super Joyful.ttf")
        try:
            self.font_title = pygame.font.Font(font_path, 60)
            self.font_stage = pygame.font.Font(font_path, 40)
            self.font_button = pygame.font.Font(font_path, 30)
            self.font_small = pygame.font.Font(font_path, 24)
            self.font_digits = pygame.font.Font(digits_path, 28)
        except:
            self.font_title = pygame.font.Font(None, 60)
            self.font_stage = pygame.font.Font(None, 40)
            self.font_button = pygame.font.Font(None, 30)
            self.font_small = pygame.font.Font(None, 24)
            self.font_digits = pygame.font.Font(digits_path, 28)

        #Colors
        self.SOIL_BROWN = (101, 67, 33)
        self.SOIL_DARK = (76, 50, 25)

        self.MELON_LEAF = (60, 170, 80)
        self.MELON_LEAF_DARK = (30, 120, 40)
        self.MELON_GREEN = (180, 250, 160)
        self.MELON_RIPE = (255, 230, 150)

        self.WHITE = (255, 255, 255)
        self.WATER_BLUE = (135, 206, 250)
        self.BUTTON_GREEN = (126, 176, 105)

        #Stages
        self.stages = [
            "Biji", "Kecambah", "Daun Awal", "Daun Besar",
            "Vegetatif", "Bunga", "Buah Muda", "Buah Matang", "Siap Panen"
        ]

        self.current_stage = 0
        self.growth_progress = 0
        self.stage_requirements = [18, 25, 35, 45, 55, 65, 75, 85]

        # Nutrients
        self.water_level = 30
        self.sunlight_level = 30
        self.fertilizer_level = 30

        self.water_consumption = 2
        self.sunlight_consumption = 2
        self.fertilizer_consumption = 2

        # Cloud
        self.cloud = {
            'x': self.width // 4,
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

        # Funfact sekali saja
        self.show_fact = False
        self.funfact_shown = False
        self.fact_text = [
            "Melon kaya vitamin C dan sangat menyegarkan!",
            "Melon pertama dibudidayakan di Persia!",
            "Melon matang punya aroma manis alami dari kulitnya."
        ]
        self.current_fact = ""

        # Panen sistem
        self.fruit_positions = []
        self.harvested_fruits = []
        self.total_harvested = 0

        self.message = ""
        self.message_timer = 0

        self.time = 0
        self.plant_sway = 0

    #SKY 
    def draw_sky_elements(self):
        cx, cy = int(self.cloud['x']), int(self.cloud['y'])

        pygame.draw.ellipse(self.screen, (200,200,200), (cx+5, cy+5, 60, 40))
        pygame.draw.ellipse(self.screen, self.WHITE, (cx, cy, 60, 40))
        pygame.draw.ellipse(self.screen, self.WHITE, (cx+40, cy, 70, 50))
        pygame.draw.ellipse(self.screen, self.WHITE, (cx+80, cy, 60, 40))

        if self.cloud['raining']:
            for d in self.cloud['rain_drops']:
                pygame.draw.line(self.screen, self.WATER_BLUE,
                                 (int(d['x']), int(d['y'])),
                                 (int(d['x']), int(d['y'])+8), 2)

        # SUN
        sx, sy = self.sun['x'], self.sun['y']
        r = self.sun['radius']

        # glow
        for i in range(3):
            glow_radius = r + 20 - i * 7
            glow_alpha = 30 - i * 10
            surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255,255,0,glow_alpha),
                               (glow_radius, glow_radius), glow_radius)
            self.screen.blit(surf, (sx - glow_radius, sy - glow_radius))

        # rays
        for i in range(12):
            ang = math.radians(i*30 + self.time*10)
            pygame.draw.line(
                self.screen, (255,223,0),
                (sx + math.cos(ang)*r, sy + math.sin(ang)*r),
                (sx + math.cos(ang)*(r+25), sy + math.sin(ang)*(r+25)), 4
            )

        # main sun body
        pygame.draw.circle(self.screen, (255,200,0), (sx,sy), r)
        pygame.draw.circle(self.screen, (255,230,90), (sx,sy), r-5)

        # WHITE HIGHLIGHT (DITAMBAHKAN)
        pygame.draw.circle(self.screen, (255,255,200), (sx-10, sy-10), 15)

    def draw_soil(self):
        self.soil_y = self.height - 170
        pygame.draw.rect(self.screen, self.SOIL_DARK, (0, self.soil_y+45, self.width, 300))
        pygame.draw.rect(self.screen, self.SOIL_BROWN, (0, self.soil_y, self.width, 45))

    def draw_leaf(self, x, y, size=55, angle=0):
        leaf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pts = []

        for i in range(28):
            ang = math.radians(i * (360 / 28))
            r = size * (1.0 if i%2 else 0.85)
            pts.append((size + math.cos(ang)*r, size + math.sin(ang)*r*0.8))

        pygame.draw.polygon(leaf, self.MELON_LEAF, pts)
        pygame.draw.polygon(leaf, self.MELON_LEAF_DARK, pts, 3)

        leaf = pygame.transform.rotate(leaf, angle)
        rect = leaf.get_rect(center=(x,y))
        self.screen.blit(leaf, rect)

    def draw_melon_harvest_positions(self, x, y):
        self.fruit_positions = [
            (x - 60, y - 120),
            (x,      y - 145),
            (x + 60, y - 120),
        ]

        for i, (fx, fy) in enumerate(self.fruit_positions):
            if i in [f['id'] for f in self.harvested_fruits]:
                continue

            pygame.draw.ellipse(self.screen, self.MELON_RIPE, (fx-20, fy-15, 40, 30))

    def draw_plant(self):
        cx = self.width // 2
        y = self.soil_y
        sway = math.sin(self.plant_sway) * 3

        if self.current_stage == 0:
            pygame.draw.ellipse(self.screen, (80,50,20),(cx-10, y+20, 20, 12))
            return

        if self.current_stage >= 1:
            pygame.draw.line(self.screen, (70,150,80),(cx, y),(cx+sway, y-25),5)

        if self.current_stage >= 2:
            self.draw_leaf(cx-30, y-55, size=40)
            self.draw_leaf(cx+30, y-55, size=40)

        if self.current_stage >= 3:
            self.draw_leaf(cx-60, y-80, size=55)
            self.draw_leaf(cx+60, y-80, size=55)

        if self.current_stage >= 4:
            for dx in [-110,-70,-30,0,30,70,110]:
                self.draw_leaf(cx+dx, y-110, size=60)

        if self.current_stage >= 5:
            pygame.draw.circle(self.screen, (255,240,120), (cx, y-140), 14)

        if self.current_stage >= 6:
            pygame.draw.ellipse(self.screen, self.MELON_GREEN,(cx-25, y-125, 50, 36))

        if self.current_stage >= 7:
            pygame.draw.ellipse(self.screen, self.MELON_RIPE,(cx-35, y-140, 70, 50))

        if self.current_stage >= 8:
            self.draw_melon_harvest_positions(cx, y)

    def draw_fertilizer_bag(self):
        bag = self.fertilizer_bag
        x,y,w,h = bag['x'], bag['y'], bag['width'], bag['height']
        pygame.draw.rect(self.screen, (50,35,20),(x+4,y+4,w,h),border_radius=10)
        pygame.draw.rect(self.screen, (190,140,70),(x,y,w,h),border_radius=10)
        pygame.draw.rect(self.screen, (90,50,20),(x,y,w,h),3,border_radius=10)
        txt = self.font_small.render("PUPUK",True,(60,30,10))
        self.screen.blit(txt,(x+w//2 - txt.get_width()//2, y+40))

    def draw_ui(self):
        bg = pygame.Rect(self.width//2-200,20,400,25)
        pygame.draw.rect(self.screen,(40,40,40),bg,border_radius=12)

        if self.current_stage < len(self.stages)-1:
            req = self.stage_requirements[self.current_stage]
            pw = int((self.growth_progress/req)*380)
            pygame.draw.rect(self.screen,(80,220,90),(self.width//2-190,25,pw,15),border_radius=8)

        pygame.draw.rect(self.screen,self.WHITE,bg,2,border_radius=12)

        txt = self.font_stage.render(self.stages[self.current_stage],True,self.WHITE)
        self.screen.blit(txt,(self.width//2 - txt.get_width()//2, 55))

        bar_x = 30
        bar_y = 120
        bar_w = 200

        items = [
            ("Air", self.water_level, self.WATER_BLUE),
            ("Cahaya", self.sunlight_level, (255,230,90)),
            ("Pupuk", self.fertilizer_level, (80,200,120)),
        ]

        for i,(name,val,col) in enumerate(items):
            y = bar_y + i*45
            lb = self.font_button.render(name,True,self.WHITE)
            self.screen.blit(lb,(bar_x,y-5))

            pygame.draw.rect(self.screen,(50,50,50),
                    (bar_x+120,y,bar_w,25),border_radius=12)
            pygame.draw.rect(self.screen,self.WHITE,
                    (bar_x+120,y,bar_w,25),2,border_radius=12)

            fw = int((val/100)*bar_w)
            pygame.draw.rect(self.screen,col,(bar_x+120,y,fw,25),border_radius=12)

            pct = self.font_digits.render(f"{int(val)}%", True, self.WHITE)
            self.screen.blit(pct,(bar_x+120+bar_w+10, y))

        back = pygame.Rect(self.width-150,self.height-70,120,50)
        pygame.draw.rect(self.screen,self.BUTTON_GREEN,back,border_radius=12)
        pygame.draw.rect(self.screen,self.WHITE,back,2,border_radius=12)
        bt = self.font_button.render("Kembali",True,self.WHITE)
        self.screen.blit(bt,(back.centerx - bt.get_width()//2,
                             back.centery - bt.get_height()//2))

        if self.message_timer > 0:
            msg = self.font_digits.render(self.message,True,self.WHITE)
            self.screen.blit(msg,(self.width//2-msg.get_width()//2,300))

    def show_message(self, text):
        self.message = text
        self.message_timer = 2.0

    def harvest_fruit(self, mouse):
        if self.current_stage < len(self.stages)-1:
            return

        for i, (fx,fy) in enumerate(self.fruit_positions):
            if i in [f['id'] for f in self.harvested_fruits]:
                continue

            if math.dist(mouse, (fx,fy)) < 40:

                self.harvested_fruits.append({
                    'id': i,
                    'x': fx,
                    'y': fy,
                    'vx': random.uniform(-4,4),
                    'vy': random.uniform(-12,-8),
                    'rotation': 0,
                    'rot_speed': random.uniform(-5,5)
                })

                self.total_harvested += 1
                self.show_message(f"Panen {self.total_harvested}/3")

                if not self.funfact_shown:
                    self.current_fact = random.choice(self.fact_text)
                    self.show_fact = True
                    self.funfact_shown = True

                if self.total_harvested >= 3:
                    pygame.time.set_timer(pygame.USEREVENT+1, 1500)
                    self.show_message("Semua buah berhasil dipanen!")

                break

    def draw_funfact(self):
        if not self.show_fact:
            return

        box = pygame.Rect(self.width//2 - 260, 200, 520, 200)
        pygame.draw.rect(self.screen,(0,0,0,180),box,border_radius=20)
        pygame.draw.rect(self.screen,self.WHITE,box,3,border_radius=20)

        t = self.font_button.render("Fun Fact!",True,self.WHITE)
        self.screen.blit(t,(box.centerx - t.get_width()//2, box.y+20))

        fact = self.font_small.render(self.current_fact,True,self.WHITE)
        self.screen.blit(fact,(box.centerx - fact.get_width()//2, box.y+90))

        self.fact_close_rect = pygame.Rect(box.centerx-60, box.bottom-60, 120, 40)
        pygame.draw.rect(self.screen,self.BUTTON_GREEN,self.fact_close_rect,border_radius=12)
        pygame.draw.rect(self.screen,self.WHITE,self.fact_close_rect,2,border_radius=12)

        t2 = self.font_button.render("Tutup",True,self.WHITE)
        self.screen.blit(t2,(self.fact_close_rect.centerx-t2.get_width()//2,
                             self.fact_close_rect.centery-t2.get_height()//2))

    def handle_event(self, event):

        if event.type == pygame.USEREVENT+1:
            self.scene_manager.change_scene("apresiasi", plant_type="melon")
            pygame.time.set_timer(pygame.USEREVENT+1,0)
            return

        if self.show_fact:
            if event.type == pygame.MOUSEBUTTONDOWN and self.fact_close_rect.collidepoint(event.pos):
                self.show_fact = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            m = event.pos

            if self.current_stage == len(self.stages)-1:
                self.harvest_fruit(m)

            cloud_rect = pygame.Rect(self.cloud['x'], self.cloud['y'],
                                     self.cloud['width'], self.cloud['height'])
            if cloud_rect.collidepoint(m):
                self.cloud['dragging'] = True
                self.cloud['raining'] = True
                self.show_message("Air bertambah!")

            if math.dist(m,(self.sun['x'],self.sun['y'])) < self.sun['radius']+30:
                self.sunlight_level = min(100, self.sunlight_level+25)
                self.sun['glow'] = 50
                self.show_message("Cahaya +25%!")

            bag = self.fertilizer_bag
            if pygame.Rect(bag['x'],bag['y'],bag['width'],bag['height']).collidepoint(m):
                self.fertilizer_level = min(100,self.fertilizer_level+25)
                self.show_message("Pupuk +25%!")

            if pygame.Rect(self.width-150,self.height-70,120,50).collidepoint(m):
                self.scene_manager.change_scene("pilih_buah")

        elif event.type == pygame.MOUSEMOTION:
            if self.cloud['dragging']:
                x = event.pos[0]
                self.cloud['x'] = max(40, min(self.width-200, x-70))

        elif event.type == pygame.MOUSEBUTTONUP:
            self.cloud['dragging'] = False
            self.cloud['raining'] = False
            self.cloud['rain_drops'].clear()

    def update(self, dt):
        self.time += dt
        self.plant_sway += dt*2

        if self.cloud['raining']:
            if random.random() < 0.5:
                self.cloud['rain_drops'].append({
                    'x': self.cloud['x'] + random.uniform(20,130),
                    'y': self.cloud['y'] + 70,
                    'vy': random.uniform(8,12)
                })

            soil_y = self.height - 210
            for d in self.cloud['rain_drops'][:]:
                d['y'] += d['vy']
                if d['y'] >= soil_y:
                    self.water_level = min(100, self.water_level + 1.5)
                    self.cloud['rain_drops'].remove(d)

        if (self.water_level > 60 and 
            self.sunlight_level > 50 and 
            self.fertilizer_level > 40):

            self.growth_progress += 3*dt

            if (self.current_stage < len(self.stage_requirements) and
                self.growth_progress >= self.stage_requirements[self.current_stage]):

                self.current_stage += 1
                self.growth_progress = 0

        for fruit in self.harvested_fruits[:]:
            fruit['x'] += fruit['vx']
            fruit['y'] += fruit['vy']
            fruit['vy'] += 0.4
            fruit['rotation'] += fruit['rot_speed']

            if fruit['y'] > self.height + 50:
                self.harvested_fruits.remove(fruit)

        self.water_level = max(0, self.water_level - self.water_consumption * dt)
        self.sunlight_level = max(0, self.sunlight_level - self.sunlight_consumption * dt)
        self.fertilizer_level = max(0, self.fertilizer_level - self.fertilizer_consumption * dt)

        self.sun['glow'] = max(0, self.sun['glow'] - dt*50)

        if self.message_timer > 0:
            self.message_timer -= dt

    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.draw_sky_elements()
        self.draw_soil()
        self.draw_plant()
        self.draw_fertilizer_bag()

        for fruit in self.harvested_fruits:
            fx, fy = int(fruit['x']), int(fruit['y'])
            surf = pygame.Surface((60,60), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, self.MELON_RIPE, (10,15,40,30))
            rot = pygame.transform.rotate(surf, fruit['rotation'])
            rect = rot.get_rect(center=(fx,fy))
            self.screen.blit(rot, rect)

        self.draw_ui()
        self.draw_funfact()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 650))
    pygame.display.set_caption("TEST MELON")

    class DummyManager:
        def change_scene(self, x):
            print("Change scene:", x)

    scene = GrowthMelon(screen, DummyManager())
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60)/1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            scene.handle_event(e)

        scene.update(dt)
        scene.draw()
        pygame.display.flip()

    pygame.quit()

import tkinter as tk
import math

class GrafikaMini:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Scene 2D - Rumah & Danau")
        
        # Canvas setup
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='lightblue')
        self.canvas.pack()
        
        # Pixel grid untuk menggambar
        self.pixels = {}
        
        # Parameter animasi
        self.cloud_offset = 0
        self.sun_rotation = 0
        self.scale_factor = 1.0
        self.animation_running = True
        self.after_id = None
        
        # Bind keyboard
        self.root.bind('<KeyPress-space>', self.zoom_in)
        self.root.bind('<KeyPress-r>', self.reset_scale)
        
        # Bind close window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Info text
        info = tk.Label(root, text="Tekan SPACE untuk zoom in | Tekan R untuk reset", 
                       font=("Arial", 10))
        info.pack()
        
        # Mulai animasi
        self.animate()
    
    # ==================== ALGORITMA GARIS DDA ====================
    def draw_line_dda(self, x1, y1, x2, y2, color='black'):
        dx = x2 - x1
        dy = y2 - y1
        
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            self.put_pixel(int(x1), int(y1), color)
            return
        
        x_inc = dx / steps
        y_inc = dy / steps
        
        x, y = x1, y1
        for i in range(int(steps) + 1):
            self.put_pixel(int(x), int(y), color)
            x += x_inc
            y += y_inc
    
    # ==================== ALGORITMA LINGKARAN MIDPOINT ====================
    def draw_circle_midpoint(self, xc, yc, r, color='black', fill=False):
        x = 0
        y = r
        d = 1 - r
        
        points = []
        
        while x <= y:
            # 8 titik simetri
            pts = [
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ]
            
            if fill:
                points.extend(pts)
            else:
                for px, py in pts:
                    self.put_pixel(px, py, color)
            
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
        
        # Fill circle
        if fill and points:
            for py in range(int(yc - r), int(yc + r) + 1):
                x_vals = [p[0] for p in points if abs(p[1] - py) < 1]
                if x_vals:
                    x_min, x_max = min(x_vals), max(x_vals)
                    for px in range(int(x_min), int(x_max) + 1):
                        self.put_pixel(px, py, color)
    
    # ==================== ALGORITMA POLIGON ====================
    def draw_polygon(self, points, color='black', fill=False):
        # Gambar garis tepi
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            self.draw_line_dda(x1, y1, x2, y2, color)
        
        # Fill polygon (scan line algorithm sederhana)
        if fill:
            min_y = int(min(p[1] for p in points))
            max_y = int(max(p[1] for p in points))
            
            for y in range(min_y, max_y + 1):
                intersections = []
                for i in range(len(points)):
                    x1, y1 = points[i]
                    x2, y2 = points[(i + 1) % len(points)]
                    
                    if y1 != y2:
                        if min(y1, y2) <= y < max(y1, y2):
                            x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                            intersections.append(x)
                
                intersections.sort()
                for i in range(0, len(intersections), 2):
                    if i + 1 < len(intersections):
                        x_start = int(intersections[i])
                        x_end = int(intersections[i + 1])
                        for x in range(x_start, x_end + 1):
                            self.put_pixel(x, y, color)
    
    # ==================== TRANSFORMASI GEOMETRIS ====================
    def translate(self, points, tx, ty):
        return [(x + tx, y + ty) for x, y in points]
    
    def scale(self, points, sx, sy, pivot_x, pivot_y):
        result = []
        for x, y in points:
            new_x = pivot_x + (x - pivot_x) * sx
            new_y = pivot_y + (y - pivot_y) * sy
            result.append((new_x, new_y))
        return result
    
    def rotate(self, points, angle, pivot_x, pivot_y):
        result = []
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        for x, y in points:
            # Translasi ke origin
            tx = x - pivot_x
            ty = y - pivot_y
            
            # Rotasi
            new_x = tx * cos_a - ty * sin_a
            new_y = tx * sin_a + ty * cos_a
            
            # Translasi kembali
            result.append((new_x + pivot_x, new_y + pivot_y))
        
        return result
    
    def reflect_y(self, points, axis_y):
        return [(x, 2 * axis_y - y) for x, y in points]
    
    # ==================== PIXEL RENDERING ====================
    def put_pixel(self, x, y, color):
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[(x, y)] = color
    
    def render_pixels(self):
        self.canvas.delete("all")
        for (x, y), color in self.pixels.items():
            self.canvas.create_line(x, y, x+1, y+1, fill=color)
    
    # ==================== GAMBAR OBJEK ====================
    def draw_sun(self):
        sun_x, sun_y = 650, 80
        sun_r = 30
        
        # Matahari (lingkaran kuning)
        self.draw_circle_midpoint(sun_x, sun_y, sun_r, 'yellow', fill=True)
        self.draw_circle_midpoint(sun_x, sun_y, sun_r, 'orange', fill=False)
        
        # Sinar matahari yang berputar
        num_rays = 12
        ray_length = 50
        
        for i in range(num_rays):
            angle = (360 / num_rays) * i + self.sun_rotation
            rad = math.radians(angle)
            
            # Titik awal sinar (di tepi matahari)
            x1 = sun_x + sun_r * math.cos(rad)
            y1 = sun_y + sun_r * math.sin(rad)
            
            # Titik akhir sinar
            x2 = sun_x + (sun_r + ray_length) * math.cos(rad)
            y2 = sun_y + (sun_r + ray_length) * math.sin(rad)
            
            self.draw_line_dda(x1, y1, x2, y2, 'orange')
    
    def draw_cloud(self, x_offset):
        # Awan 1
        cloud_x = 150 + x_offset
        cloud_y = 100
        
        self.draw_circle_midpoint(cloud_x, cloud_y, 20, 'white', fill=True)
        self.draw_circle_midpoint(cloud_x + 25, cloud_y, 25, 'white', fill=True)
        self.draw_circle_midpoint(cloud_x + 50, cloud_y, 20, 'white', fill=True)
        
        # Awan 2
        cloud2_x = 400 + x_offset
        cloud2_y = 120
        
        self.draw_circle_midpoint(cloud2_x, cloud2_y, 18, 'white', fill=True)
        self.draw_circle_midpoint(cloud2_x + 22, cloud2_y, 22, 'white', fill=True)
        self.draw_circle_midpoint(cloud2_x + 45, cloud2_y, 18, 'white', fill=True)
    
    def draw_house(self, scale=1.0):
        pivot_x, pivot_y = 200, 480
        
        # Badan rumah (persegi panjang)
        house_body = [
            (150, 380), (250, 380),
            (250, 480), (150, 480)
        ]
        
        # Atap rumah (segitiga)
        house_roof = [
            (140, 380), (200, 310), (260, 380)
        ]
        
        # Pintu
        door = [
            (180, 430), (220, 430),
            (220, 480), (180, 480)
        ]
        
        # Jendela
        window = [
            (160, 400), (185, 400),
            (185, 420), (160, 420)
        ]
        
        # Apply scale
        house_body = self.scale(house_body, scale, scale, pivot_x, pivot_y)
        house_roof = self.scale(house_roof, scale, scale, pivot_x, pivot_y)
        door = self.scale(door, scale, scale, pivot_x, pivot_y)
        window = self.scale(window, scale, scale, pivot_x, pivot_y)
        
        # Gambar
        self.draw_polygon(house_body, 'saddlebrown', fill=True)
        self.draw_polygon(house_roof, 'darkred', fill=True)
        self.draw_polygon(door, 'brown', fill=True)
        self.draw_polygon(window, 'lightblue', fill=True)
        
        # Refleksi rumah di tanah
        water_y = 480
        house_body_reflect = self.reflect_y(house_body, water_y)
        house_roof_reflect = self.reflect_y(house_roof, water_y)
        door_reflect = self.reflect_y(door, water_y)
        
        self.draw_polygon(house_body_reflect, 'darkgray', fill=True)
        self.draw_polygon(house_roof_reflect, 'darkgray', fill=True)
        self.draw_polygon(door_reflect, 'darkgray', fill=True)
    
    def draw_lake(self):
        # Danau (poligon)
        lake = [
            (300, 480), (800, 480),
            (800, 600), (300, 600)
        ]
        self.draw_polygon(lake, 'steelblue', fill=True)
    
    def draw_flowers(self, scale=1.0):
        flower_positions = [(330, 460), (380, 465), (430, 458), (480, 462)]
        water_y = 480
        
        for fx, fy in flower_positions:
            pivot_x, pivot_y = fx, fy
            
            # Batang bunga
            stem_start = (fx, fy)
            stem_end = (fx, fy + 30)
            
            stem_start = self.scale([stem_start], scale, scale, pivot_x, pivot_y)[0]
            stem_end = self.scale([stem_end], scale, scale, pivot_x, pivot_y)[0]
            
            self.draw_line_dda(stem_start[0], stem_start[1], stem_end[0], stem_end[1], 'green')
            
            # Kepala bunga (lingkaran)
            flower_center = self.scale([(fx, fy)], scale, scale, pivot_x, pivot_y)[0]
            radius = int(8 * scale)
            
            self.draw_circle_midpoint(int(flower_center[0]), int(flower_center[1]), 
                                     radius, 'pink', fill=True)
            self.draw_circle_midpoint(int(flower_center[0]), int(flower_center[1]), 
                                     radius//2, 'yellow', fill=True)
            
            # Refleksi bunga di danau
            reflect_stem_start = self.reflect_y([stem_start], water_y)[0]
            reflect_stem_end = self.reflect_y([stem_end], water_y)[0]
            reflect_center = self.reflect_y([flower_center], water_y)[0]
            
            self.draw_line_dda(reflect_stem_start[0], reflect_stem_start[1],
                             reflect_stem_end[0], reflect_stem_end[1], 'darkgreen')
            self.draw_circle_midpoint(int(reflect_center[0]), int(reflect_center[1]), 
                                     radius, 'gray', fill=True)
    
    def draw_ground(self):
        # Daratan
        ground = [
            (0, 480), (300, 480),
            (300, 600), (0, 600)
        ]
        self.draw_polygon(ground, 'green', fill=True)
    
    # ==================== ANIMASI ====================
    def animate(self):
        if not self.animation_running:
            return
        
        self.pixels.clear()
        
        # Gambar langit (background sudah lightblue)
        
        # Matahari dengan sinar berputar
        self.draw_sun()
        
        # Awan bergerak (translasi)
        self.draw_cloud(self.cloud_offset)
        
        # Daratan
        self.draw_ground()
        
        # Danau
        self.draw_lake()
        
        # Rumah dengan skala
        self.draw_house(self.scale_factor)
        
        # Bunga dengan refleksi
        self.draw_flowers(self.scale_factor)
        
        # Render semua pixel
        self.render_pixels()
        
        # Update parameter animasi
        self.cloud_offset += 1
        if self.cloud_offset > self.width:
            self.cloud_offset = -100
        
        self.sun_rotation += 2
        if self.sun_rotation >= 360:
            self.sun_rotation = 0
        
        # Loop animasi
        self.after_id = self.root.after(1, self.animate)
    
    def zoom_in(self, event):
        self.scale_factor = min(self.scale_factor + 0.1, 2.0)
    
    def reset_scale(self, event):
        self.scale_factor = 1.0
    
    def on_closing(self):
        self.animation_running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.root.destroy()

# ==================== MAIN ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = GrafikaMini(root)
    root.mainloop()
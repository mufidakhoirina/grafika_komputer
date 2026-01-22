import tkinter as tk
import math

# --- Configuration ---
WIDTH, HEIGHT = 1000, 700
BG_COLOR = "#ECEFF1"  # Soft Blue-Grey Background
FOV = 900
FLOOR_Y = 150         # Y coordinate of the floor (ground level)
LIGHT_DIR = None      # Will initialize later

# --- 3D Vector Math ---
class Vector3:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    
    def __repr__(self): return f"V({self.x:.1f}, {self.y:.1f}, {self.z:.1f})"

    def add(self, v): return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)
    def sub(self, v): return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)
    def mul(self, s): return Vector3(self.x * s, self.y * s, self.z * s)
    
    def dot(self, v): return self.x*v.x + self.y*v.y + self.z*v.z
    
    def cross(self, v):
        return Vector3(
            self.y*v.z - self.z*v.y,
            self.z*v.x - self.x*v.z,
            self.x*v.y - self.y*v.x
        )
    
    def normalize(self):
        m = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return Vector3(self.x/m, self.y/m, self.z/m) if m else Vector3(0,0,0)

LIGHT_DIR = Vector3(0.5, -0.8, -0.5).normalize()

# --- Object Factory ---
def create_box(w, h, d, color):
    """ Returns (verts, faces) for a box centered at 0,0,0 """
    hw, hh, hd = w/2, h/2, d/2
    verts = [
        Vector3(-hw, -hh, -hd), Vector3(hw, -hh, -hd),
        Vector3(hw, hh, -hd),   Vector3(-hw, hh, -hd),
        Vector3(-hw, -hh, hd),  Vector3(hw, -hh, hd),
        Vector3(hw, hh, hd),    Vector3(-hw, hh, hd)
    ]
    # Faces defined by vertex indices (quads)
    # Order: Front, Back, Left, Right, Top, Bottom
    # Careful with winding order for backface culling (if implemented)
    faces = [
        ([0, 1, 2, 3], color), # Back Face (usually z is negative) - this is actually Front in local coords if z+ is front
        ([5, 4, 7, 6], color), # Front Face (z+)
        ([4, 0, 3, 7], color), # Left
        ([1, 5, 6, 2], color), # Right
        ([3, 2, 6, 7], color), # Top
        ([4, 5, 1, 0], color)  # Bottom
    ]
    return verts, faces

def create_cylinder(radius, height, segments, color):
    """ Returns simple approximation (prism) """
    verts = []
    hh = height / 2
    # Top and Bottom rings
    for i in range(segments):
        theta = (2 * math.pi * i) / segments
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        verts.append(Vector3(x, hh, z))  # Top ring: indices 0 to segments-1
        verts.append(Vector3(x, -hh, z)) # Bottom ring: indices segments to 2*segments-1
    
    faces = []
    # Side faces
    for i in range(0, segments):
        top1 = i
        top2 = (i + 1) % segments
        bot1 = i + segments
        bot2 = ((i + 1) % segments) + segments
        # Properly ordered quad
        faces.append(([top1, bot1, bot2, top2], color))
    
    # Caps
    top_indices = [i for i in range(segments)]
    bot_indices = [i + segments for i in range(segments)]
    bot_indices.reverse() # Flip normal for bottom
    faces.append((top_indices, color))
    faces.append((bot_indices, color))
    return verts, faces

# --- Core Object Class ---
class Object3D:
    def __init__(self, name, verts, faces, pos, is_line=False):
        self.name = name
        self.raw_verts = verts 
        self.faces = faces     
        self.pos = pos        
        self.scale_val = 1.0
        self.selected = False
        self.target_scale = 1.0
        self.is_line = is_line

    def update(self):
        diff = self.target_scale - self.scale_val
        if abs(diff) > 0.01:
            self.scale_val += diff * 0.2
        else:
            self.scale_val = self.target_scale

    def toggle_select(self):
        if self.is_line: return False
        self.selected = not self.selected
        self.target_scale = 1.1 if self.selected else 1.0
        return self.selected

    def get_world_verts(self):
        res = []
        for v in self.raw_verts:
            sv = v.mul(self.scale_val)
            res.append(sv.add(self.pos))
        return res

    def get_shadow_verts(self, world_verts):
        if self.is_line: return []
        res = []
        # Simple projection shadow: x + constant, y fixed at floor
        for v in world_verts:
            res.append(Vector3(v.x + 30, FLOOR_Y + 1, v.z + 30)) 
        return res

# --- Engine & UI ---
class LivingRoomApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern 3D Interactive Room Concept")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack(fill="both", expand=True)

        self.label_info = tk.Label(self, text="Click objects to interact | Arrow keys to rotate", 
                                 font=("Helvetica", 12), bg="white", relief="solid", padx=10, pady=5)
        self.label_info.place(x=20, y=HEIGHT-50)

        # Camera
        self.cam_angle_y = -0.6 # Initial view angle
        self.cam_angle_x = 0.35 # High angle
        self.keys_pressed = {}

        # Scene Objects
        self.objects = []
        self.init_scene()

        # Input
        self.bind("<KeyPress>", self.on_key)
        self.bind("<KeyRelease>", self.on_key_release)
        self.canvas.bind("<Button-1>", self.on_click)
        self.bind("<MouseWheel>", self.on_zoom) # Windows
        self.bind("<Button-4>", self.on_zoom_up) # Linux
        self.bind("<Button-5>", self.on_zoom_down) # Linux


        # Loop
        self.cam_zoom = 1.0
        self.update_loop()

    def init_scene(self):
        # Palette - Modern Scandi
        C_WALL_BACK = "#B0BEC5"   # Cool Grey
        C_WALL_SIDE = "#CFD8DC"   # Lighter Grey
        C_FLOOR = "#D7CCC8"       # Light Wood
        C_SOFA_MAIN = "#263238"   # Dark Blue/Grey
        C_SOFA_ACCENT = "#546E7A" # Lighter Blue/Grey
        C_TABLE_TOP = "#ECEFF1"   # White Marble
        C_LEG = "#3E2723"         # Dark Wood
        C_LAMP_SHADE = "#FFECB3"  # Warm Light
        C_PLANT_POT = "#EFEBE9"   

        # 1. Room Shell
        # Floor (Large plate)
        v, f = create_box(1200, 20, 1000, C_FLOOR)
        self.objects.append(Object3D("Floor", v, f, Vector3(0, FLOOR_Y+10, 0)))
        
        # Walls
        v, f = create_box(1200, 600, 20, C_WALL_BACK) 
        self.objects.append(Object3D("Back Wall", v, f, Vector3(0, -150, -400))) # Back

        v, f = create_box(20, 600, 1000, C_WALL_SIDE)
        self.objects.append(Object3D("Left Wall", v, f, Vector3(-600, -150, 0))) # Left

        # Baseboards (Skirtings)
        v, f = create_box(1200, 15, 5, "#FFFFFF")
        self.objects.append(Object3D("Baseboard Back", v, f, Vector3(0, FLOOR_Y-5, -390)))

        # 2. Main Sofa (3-Seater) - Centered
        # Seat Base
        v, f = create_box(320, 45, 100, C_SOFA_MAIN)
        self.objects.append(Object3D("Sofa Base", v, f, Vector3(0, FLOOR_Y-30, -100)))
        # Backrest
        v, f = create_box(320, 90, 30, C_SOFA_MAIN)
        self.objects.append(Object3D("Sofa Back", v, f, Vector3(0, FLOOR_Y-70, -145)))
        # Armrests
        v, f = create_box(30, 70, 105, C_SOFA_ACCENT)
        self.objects.append(Object3D("Arm Left", v, f, Vector3(-175, FLOOR_Y-50, -100)))
        self.objects.append(Object3D("Arm Right", v, f, Vector3(175, FLOOR_Y-50, -100)))
        # Cushions
        v, f = create_box(280, 15, 80, C_SOFA_ACCENT)
        self.objects.append(Object3D("Cushion", v, f, Vector3(0, FLOOR_Y-55, -100)))

        # 3. Modern Coffee Table - In front of Sofa
        # Top
        v, f = create_box(160, 5, 90, C_TABLE_TOP)
        self.objects.append(Object3D("Table Top", v, f, Vector3(0, FLOOR_Y-50, 50)))
        # Legs
        leg_geom = create_box(8, 45, 8, "#37474F") # Metal legs
        for lx in [-70, 70]:
            for lz in [20, 80]:
                self.objects.append(Object3D("Table Leg", leg_geom[0], leg_geom[1], Vector3(lx, FLOOR_Y-25, lz)))

        # 4. Standing Art/Decor (Right Side)
        v, f = create_box(80, 120, 5, "#4E342E") # Frame
        self.objects.append(Object3D("Art Frame", v, f, Vector3(300, FLOOR_Y-60, -380)))
        v, f = create_box(70, 110, 2, "#FFCC80") # Canvas
        self.objects.append(Object3D("Art Canvas", v, f, Vector3(300, FLOOR_Y-60, -376)))

        # 5. Plant / Tall Vase (Left Corner)
        # Pot
        v, f = create_cylinder(25, 60, 12, C_PLANT_POT)
        self.objects.append(Object3D("Vase", v, f, Vector3(-350, FLOOR_Y-30, -320)))
        # Plant Stem
        v, f = create_box(5, 120, 5, "#2E7D32")
        self.objects.append(Object3D("Plant", v, f, Vector3(-350, FLOOR_Y-90, -320)))
        # Leaves
        v, f = create_box(60, 2, 40, "#4CAF50")
        self.objects.append(Object3D("Leaf", v, f, Vector3(-330, FLOOR_Y-130, -320)))
        self.objects.append(Object3D("Leaf", v, f, Vector3(-370, FLOOR_Y-110, -320)))

        # 6. Floor Lamp (Right Front)
        v, f = create_cylinder(5, 200, 6, "#BDBDBD") # Pole
        self.objects.append(Object3D("Lamp Pole", v, f, Vector3(400, FLOOR_Y-100, 100)))
        v, f = create_cylinder(30, 5, 10, "#424242") # Base
        self.objects.append(Object3D("Lamp Base", v, f, Vector3(400, FLOOR_Y-2, 100)))
        v, f = create_cylinder(40, 50, 12, C_LAMP_SHADE) # Shade
        self.objects.append(Object3D("Lamp Shade", v, f, Vector3(400, FLOOR_Y-200, 100)))
        
        # 7. Rug
        v, f = create_box(400, 2, 250, "#B0BEC5")
        self.objects.append(Object3D("Rug", v, f, Vector3(0, FLOOR_Y+1, 0)))


    def on_key(self, event):
        self.keys_pressed[event.keysym] = True
    def on_key_release(self, event):
        self.keys_pressed[event.keysym] = False

    def on_zoom(self, event):
        if event.delta > 0: self.cam_zoom *= 1.1
        else: self.cam_zoom *= 0.9
        
    def on_zoom_up(self, event): self.cam_zoom *= 1.1
    def on_zoom_down(self, event): self.cam_zoom *= 0.9

    def on_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if not item: return

        tags = self.canvas.gettags(item[0])
        
        name_found = None
        for tag in tags:
            if tag.startswith("obj:"):
                idx = int(tag.split(":")[1])
                obj = self.objects[idx]
                is_sel = obj.toggle_select()
                name_found = obj.name
                
                status = "Active" if is_sel else "Inactive"
                self.label_info.config(text=f"Selected: {name_found}")
                return 

        if not name_found:
            self.label_info.config(text="Empty Space")

    def update_loop(self):
        # Scale/Rotate Controls
        if self.keys_pressed.get("Left"): self.cam_angle_y -= 0.05
        if self.keys_pressed.get("Right"): self.cam_angle_y += 0.05
        if self.keys_pressed.get("Up"): self.cam_angle_x -= 0.05
        if self.keys_pressed.get("Down"): self.cam_angle_x += 0.05

        for obj in self.objects:
            obj.update()

        self.draw()
        self.after(30, self.update_loop)

    def draw(self):
        self.canvas.delete("all")
        cx, cy = WIDTH / 2, HEIGHT / 2
        
        cos_y, sin_y = math.cos(self.cam_angle_y), math.sin(self.cam_angle_y)
        cos_x, sin_x = math.cos(self.cam_angle_x), math.sin(self.cam_angle_x)

        render_list = [] 

        for i, obj in enumerate(self.objects):
            # 1. World Transform
            world_verts = obj.get_world_verts()
            
            # 2. Camera Transform
            cam_verts = []
            for v in world_verts:
                # Rotate Y
                x = v.x * cos_y - v.z * sin_y
                z = v.x * sin_y + v.z * cos_y
                # Rotate X
                y = v.y * cos_x - z * sin_x
                z = v.y * sin_x + z * cos_x
                
                # Zoom effect
                x *= self.cam_zoom
                y *= self.cam_zoom
                z *= self.cam_zoom
                
                cam_verts.append(Vector3(x, y, z))

            # 3. Faces Processing
            for sub_indices, color_arg in obj.faces:
                sub_verts = [cam_verts[idx] for idx in sub_indices]
                
                points_2d = []
                depth_sum = 0
                visible = True
                
                for v in sub_verts:
                    dist = FOV + v.z # Moving camera back by FOV
                    if dist < 10: 
                        visible = False; break
                    factor = FOV / dist
                    px = cx + v.x * factor
                    py = cy + v.y * factor
                    points_2d.append((px, py))
                    depth_sum += dist
                
                if visible and len(sub_verts) > 1:
                    avg_depth = depth_sum / len(sub_verts)
                    
                    if obj.is_line:
                         render_list.append((avg_depth, 2, points_2d, color_arg, f"obj:{i}"))
                    else:
                        # Lighting
                        v0, v1, v2 = sub_verts[0], sub_verts[1], sub_verts[2]
                        edge1, edge2 = v1.sub(v0), v2.sub(v0)
                        normal = edge1.cross(edge2).normalize()
                        
                        # Backface Culling (Simple Check)
                        # Eye vector is approx (0,0,-1) in camera space
                        # If Normal.z < 0 it faces camera? Or > 0. 
                        # Normals pointing towards camera have negative Z component in this system usually? 
                        # Let's trust Z-sorting for now, but Culling helps perfs.
                        # Cross product order matters.
                        
                        L_SOURCE = Vector3(0.4, -0.8, 0.4).normalize()
                        intensity = normal.dot(L_SOURCE)
                        val = 0.5 + (intensity * 0.5)
                        val = max(0.3, min(1.0, val))

                        # Color calc
                        try:
                            if color_arg.startswith("#"):
                                r = int(int(color_arg[1:3], 16) * val)
                                g = int(int(color_arg[3:5], 16) * val)
                                b = int(int(color_arg[5:7], 16) * val)
                                shade_col = f"#{r:02x}{g:02x}{b:02x}"
                            else:
                                shade_col = color_arg
                        except ValueError:
                            shade_col = color_arg

                        render_list.append((avg_depth, 1, points_2d, shade_col, f"obj:{i}"))

        # Sort by depth (Furthest first)
        render_list.sort(key=lambda x: x[0], reverse=True)

        for _, r_type, pts, col, tag in render_list:
            if r_type == 1: # Poly
                self.canvas.create_polygon(pts, fill=col, outline="", tags=tag)
            elif r_type == 2: # Line
                self.canvas.create_line(pts, fill=col, width=1, tags=tag)

if __name__ == "__main__":
    app = LivingRoomApp()
    app.mainloop()

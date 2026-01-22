import tkinter as tk
import math

# --- Configuration ---
WIDTH, HEIGHT = 900, 600
BG_COLOR = "#f5f5f5"  # Light/White background
FOV = 600
FLOOR_Y = 100         # Y coordinate of the floor (ground level)
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

LIGHT_DIR = Vector3(0.6, -0.8, -0.4).normalize()

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
    faces = [
        ([0, 1, 2, 3], color), ([5, 4, 7, 6], color), # Front, Back
        ([4, 0, 3, 7], color), ([1, 5, 6, 2], color), # Left, Right
        ([3, 2, 6, 7], color), ([4, 5, 1, 0], color)  # Top, Bottom (Top is 3,2,6,7 usually y-up)
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
    for i in range(0, segments*2, 2):
        top1 = i
        top2 = (i + 2) % (segments*2)
        bot1 = i + 1
        bot2 = (i + 3) % (segments*2)
        faces.append(([top1, bot1, bot2, top2], color))
    
    # Caps (Fan style for simplicity, or just one poly if renderer supports >4 verts)
    top_indices = [i for i in range(0, segments*2, 2)]
    bot_indices = [i for i in range(1, segments*2, 2)]
    bot_indices.reverse() # Flip normal for bottom
    faces.append((top_indices, color))
    faces.append((bot_indices, color))
    return verts, faces

def create_grid(size, step, color):
    """ Creates a wireframe grid (lines) """
    verts = []
    lines = [] # Pairs of indices
    
    half = size / 2
    # Lines parallel to X and Z
    # -half to half
    count = int(size / step)
    
    idx = 0
    # Z-lines (vary X)
    for i in range(count + 1):
        x = -half + i * step
        verts.append(Vector3(x, 0, -half))
        verts.append(Vector3(x, 0, half))
        lines.append(([idx, idx+1], color))
        idx += 2
        
    # X-lines (vary Z)
    for i in range(count + 1):
        z = -half + i * step
        verts.append(Vector3(-half, 0, z))
        verts.append(Vector3(half, 0, z))
        lines.append(([idx, idx+1], color))
        idx += 2
        
    return verts, lines

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
        self.is_line = is_line # New flag for lines vs polygons

    def update(self):
        diff = self.target_scale - self.scale_val
        if abs(diff) > 0.01:
            self.scale_val += diff * 0.2
        else:
            self.scale_val = self.target_scale

    def toggle_select(self):
        if self.is_line: return False
        self.selected = not self.selected
        self.target_scale = 1.25 if self.selected else 1.0
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
        for v in world_verts:
            res.append(Vector3(v.x + 10, FLOOR_Y + 1, v.z + 10)) 
        return res

# --- Engine & UI ---
class LivingRoomApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("3D Living Room - Interactive")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack(fill="both", expand=True)

        self.label_info = tk.Label(self, text="Click on objects!", font=("Arial", 14), bg="white", relief="solid")
        self.label_info.place(x=20, y=20)

        # Camera
        self.cam_angle_y = -0.5 # Look slightly right
        self.cam_angle_x = 0.2  # Look slightly down
        self.keys_pressed = {}

        # Scene Objects
        self.objects = []
        self.init_scene()

        # Input
        self.bind("<KeyPress>", self.on_key)
        self.bind("<KeyRelease>", self.on_key_release)
        self.canvas.bind("<Button-1>", self.on_click)

        # Loop
        self.update_loop()

    def init_scene(self):
        # Reference colors
        C_WALL = "#1565C0"    # Deep Blue
        C_SOFA = "#FFD700"    # Gold/Yellow
        C_FLOOR = "#F5F5F5"   # Brighter White Floor
        C_TABLE_TOP = "#81D4FA" # Glassy Blue
        C_WOOD = "#5D4037"

        # 0. Perspective Grid (The "Box" look)
        # Floor Grid
        gx, gl = create_grid(800, 100, "#CCCCCC") 
        self.objects.append(Object3D("Grid Floor", gx, gl, Vector3(0, FLOOR_Y, 0), is_line=True))
        
        # Wall Grids (Rotated manually or just created as lines)
        # Back Wall Grid (Vertical lines only for panel look?) No, full grid for "Box Perspective"
        # We can reuse create_grid and rotate points? Or just make new lines.
        # Let's just create a big wireframe box for the room limits
        room_w, room_h, room_d = 800, 500, 800
        # Vertices for room corners
        c1 = Vector3(-room_w/2, -room_h + FLOOR_Y, -room_d/2)
        c2 = Vector3(room_w/2, -room_h + FLOOR_Y, -room_d/2)
        c3 = Vector3(room_w/2, FLOOR_Y, -room_d/2)
        c4 = Vector3(-room_w/2, FLOOR_Y, -room_d/2)
        
        c5 = Vector3(-room_w/2, -room_h + FLOOR_Y, room_d/2)
        c6 = Vector3(room_w/2, -room_h + FLOOR_Y, room_d/2)
        c7 = Vector3(room_w/2, FLOOR_Y, room_d/2)
        c8 = Vector3(-room_w/2, FLOOR_Y, room_d/2)
        
        box_verts = [c1, c2, c3, c4, c5, c6, c7, c8]
        # Lines connecting them
        box_lines = [
            ([0, 1], "black"), ([1, 2], "black"), ([2, 3], "black"), ([3, 0], "black"), # Back Face
            ([4, 5], "black"), ([5, 6], "black"), ([6, 7], "black"), ([7, 4], "black"), # Front Face
            ([0, 4], "black"), ([1, 5], "black"), ([2, 6], "black"), ([3, 7], "black")  # Connecting
        ]
        # Add Room Wireframe to make it "Kotak"
        self.objects.append(Object3D("Room Box", box_verts, box_lines, Vector3(0,0,0), is_line=True))

        # 1. Room Shell
        # Floor
        v, f = create_box(800, 10, 800, C_FLOOR)
        self.objects.append(Object3D("Floor", v, f, Vector3(0, FLOOR_Y+5, 0)))
        
        # Back Wall (Blue with "Panels")
        v, f = create_box(800, 500, 10, C_WALL) 
        self.objects.append(Object3D("Back Wall", v, f, Vector3(0, -150, -300)))
        
        # Panels (Decor)
        for x in [-250, -100, 50, 200]:
            v, f = create_box(40, 400, 20, "#0D47A1") 
            self.objects.append(Object3D("Wall Decor", v, f, Vector3(x, -150, -290)))

        # 2. Yellow Sofa
        # Main Body
        v, f = create_box(260, 40, 80, C_SOFA)
        self.objects.append(Object3D("Yellow Sofa", v, f, Vector3(-50, FLOOR_Y-20, -50)))
        # Backrest
        v, f = create_box(260, 60, 20, "#FBC02D")
        self.objects.append(Object3D("Sofa Back", v, f, Vector3(-50, FLOOR_Y-60, -90)))
        # Armrests
        v, f = create_box(30, 60, 90, "#FBC02D")
        self.objects.append(Object3D("Sofa Arm Left", v, f, Vector3(-170, FLOOR_Y-40, -50)))
        self.objects.append(Object3D("Sofa Arm Right", v, f, Vector3(70, FLOOR_Y-40, -50)))

        # 3. Coffee Table (Hexagonal prism)
        v, f = create_cylinder(60, 10, 8, C_TABLE_TOP)
        self.objects.append(Object3D("Coffee Table", v, f, Vector3(-50, FLOOR_Y-10, 80)))
        # Legs
        v, f = create_box(10, 40, 10, "#444444")
        self.objects.append(Object3D("Table Leg", v, f, Vector3(-80, FLOOR_Y, 80)))
        self.objects.append(Object3D("Table Leg", v, f, Vector3(-20, FLOOR_Y, 80)))

        # 4. Dining Set (Right side)
        v, f = create_box(100, 10, 100, C_WOOD)
        self.objects.append(Object3D("Dining Table", v, f, Vector3(250, FLOOR_Y-30, 50)))
        # Chair
        v, f = create_box(30, 40, 30, "#FFEB3B") # Yellow Chair
        self.objects.append(Object3D("Chair", v, f, Vector3(320, FLOOR_Y-20, 50)))

        # 5. Hanging Lamp (Cone approx)
        v, f = create_cylinder(40, 40, 10, "#607D8B") # Metal Grey
        # Cylinder helper creates centered, we need to flip it visually or just place high
        self.objects.append(Object3D("Hanging Lamp", v, f, Vector3(250, -180, 50)))

    def on_key(self, event):
        self.keys_pressed[event.keysym] = True
    def on_key_release(self, event):
        self.keys_pressed[event.keysym] = False

    def on_click(self, event):
        # We use Tkinter tags to identify logic
        # item id closest to click returns a tuple
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
                
                # Feedback text
                status = "SELECTED" if is_sel else "Deselected"
                self.label_info.config(text=f"{name_found} - {status}")
                return # Only handle first hit

        if not name_found:
            self.label_info.config(text="Background")

    def update_loop(self):
        # Controls
        if self.keys_pressed.get("Left"): self.cam_angle_y -= 0.05
        if self.keys_pressed.get("Right"): self.cam_angle_y += 0.05
        if self.keys_pressed.get("Up"): self.cam_angle_x -= 0.05
        if self.keys_pressed.get("Down"): self.cam_angle_x += 0.05

        # Update Anim
        for obj in self.objects:
            obj.update()

        self.draw()
        self.after(30, self.update_loop)

    def draw(self):
        self.canvas.delete("all")
        
        cx, cy = WIDTH / 2, HEIGHT / 2
        
        # Precompute Rotation Matrix
        cos_y, sin_y = math.cos(self.cam_angle_y), math.sin(self.cam_angle_y)
        cos_x, sin_x = math.cos(self.cam_angle_x), math.sin(self.cam_angle_x)

        render_list = [] # Stores (depth, type, coords, color, tag)

        for i, obj in enumerate(self.objects):
            # 1. Transform Vertices to World Space
            world_verts = obj.get_world_verts()
            
            # 2. Camera Transform (Rotate world around camera)
            cam_verts = []
            for v in world_verts:
                # Rotate Y
                x = v.x * cos_y - v.z * sin_y
                z = v.x * sin_y + v.z * cos_y
                # Rotate X
                y = v.y * cos_x - z * sin_x
                z = v.y * sin_x + z * cos_x
                cam_verts.append(Vector3(x, y, z))

            # 3. Faces Processing
            for sub_indices, color_arg in obj.faces:
                # Get Face Vertices
                sub_verts = [cam_verts[idx] for idx in sub_indices]
                
                # Project to 2D
                points_2d = []
                depth_sum = 0
                visible = True
                
                for v in sub_verts:
                    dist = 800 + v.z # offset cam back
                    if dist < 10: 
                        visible = False; break
                    factor = FOV / dist
                    px = cx + v.x * factor
                    py = cy + v.y * factor
                    points_2d.append((px, py))
                    depth_sum += dist
                
                if visible and len(sub_verts) > 1: # Line has 2 verts, Poly >2
                    avg_depth = depth_sum / len(sub_verts)
                    
                    if obj.is_line:
                        # Type 2: Line/Grid
                        render_list.append((avg_depth, 2, points_2d, color_arg, f"obj:{i}"))
                    else:
                        # Normal Calculation
                        v0, v1, v2 = sub_verts[0], sub_verts[1], sub_verts[2]
                        edge1, edge2 = v1.sub(v0), v2.sub(v0)
                        normal = edge1.cross(edge2).normalize()

                        # Lighting Fix:
                        # Assume Light comes from Top-Right-Front relative to CAMERA view
                        # Light Vector pointing TO the light source
                        L_SOURCE = Vector3(0.5, -1.0, 0.5).normalize() 
                        # Note: If Y is down in 2D, in 3D usually Y is Up or Down depending on coord system.
                        # Here projection: py = cy + v.y. Height is Y.
                        # In create_box, Top is -h/2 (if y is down?) no, usually -y is up in screen coords.
                        # Let's just use the observed normal.
                        
                        # Dot Product:
                        # If Normal points at Light, brightness is high.
                        intensity = normal.dot(L_SOURCE)
                        
                        # If Faces are defined CCW, normal points out.
                        # Let's map [-1, 1] to [0.3, 1.0]
                        # Intensity 1.0 (Facing Light) -> Brightest
                        # Intensity -1.0 (Facing Away) -> Darkest
                        
                        val = 0.6 + (intensity * 0.4) # Base 0.6 + up to 0.4
                        val = max(0.4, min(1.0, val))
                        
                        # Apply color brightness
                        try:
                            r = int(int(color_arg[1:3], 16) * val)
                            g = int(int(color_arg[3:5], 16) * val)
                            b = int(int(color_arg[5:7], 16) * val)
                            shade_col = f"#{r:02x}{g:02x}{b:02x}"
                        except ValueError:
                            shade_col = color_arg

                        # Type 1: Object Face
                        render_list.append((avg_depth, 1, points_2d, shade_col, f"obj:{i}"))

            # 4. Shadow Render (Fake)
            # Create a simplified shadow blob (convex hull or just face projection)
            # We skip culling for shadows, just project all floor-facing faces?
            # Simpler: Project ALL vertices to floor, draw a single polygon for 'bottom' faces?
            # Let's just project faces that face 'down' or all faces
            if not obj.is_line and obj.name != "Floor" and obj.name != "Back Wall":
                shad_verts = obj.get_shadow_verts(world_verts)
                # Rotate Shadow Verts for Camera
                shad_cam_verts = []
                for v in shad_verts:
                    x = v.x * cos_y - v.z * sin_y
                    z = v.x * sin_y + v.z * cos_y
                    y = v.y * cos_x - z * sin_x
                    z = v.y * sin_x + z * cos_x
                    shad_cam_verts.append(Vector3(x, y, z))
                
                # Just draw the "Bottom" face or a bounding box shadow for performance
                # Draw the first face as shadow (hacky but works for boxes)
                if len(obj.faces) > 0:
                    sf_indices = obj.faces[0][0] # Just use first face for blob
                    sf_verts = [shad_cam_verts[idx] for idx in sf_indices]
                    
                    sp_2d = []
                    s_depth = 0
                    for v in sf_verts:
                        dist = 800 + v.z
                        f = FOV/dist
                        sp_2d.append((cx + v.x*f, cy + v.y*f))
                        s_depth += dist
                    
                    # Type 0: Shadow (Furthest usually, but we sort anyway)
                    # We use stipple for transparency simulation
                    render_list.append((s_depth/len(sf_verts) + 50, 0, sp_2d, "gray80", "")) 

        # Sort: Furthest First (Painter's Algo)
        # Depth is distance FROM camera (larger = further)
        render_list.sort(key=lambda x: x[0], reverse=True)

        for _, r_type, pts, col, tag in render_list:
            if r_type == 0: # Shadow
                 # No outline for shadow
                 if len(pts) > 2:
                    self.canvas.create_polygon(pts, fill="#BBBBBB", outline="", stipple="gray50") 
            elif r_type == 2: # Line/Grid
                 self.canvas.create_line(pts, fill=col, width=1, tags=tag)
            else: # Polygon
                if len(pts) > 2:
                    self.canvas.create_polygon(pts, fill=col, outline="black", width=1, tags=tag)

if __name__ == "__main__":
    app = LivingRoomApp()
    app.mainloop()

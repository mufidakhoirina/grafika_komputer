
You said:
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Import our new modules
from camera import Camera
from lighting import setup_lighting
from room import draw_floor, draw_walls
from furniture import (
    draw_bed, draw_wardrobe,
    draw_study_desk, draw_chair, draw_window,
    draw_ceiling_lamp, draw_picture_frame
)

# Selection IDs
ID_NOTHING = 0
ID_BED = 1
ID_WARDROBE = 2
ID_DESK = 3
ID_CHAIR = 4
ID_WINDOW = 5
ID_LAMP = 6
ID_FRAME_1 = 7
ID_FRAME_2 = 8

FURNITURE_NAMES = {
    ID_NOTHING: "",
    ID_BED: "Kasur",
    ID_WARDROBE: "Lemari Pakaian",
    ID_DESK: "Meja Belajar",
    ID_CHAIR: "Kursi",
    ID_WINDOW: "Jendela",
    ID_LAMP: "Lampu Plafon",
    ID_FRAME_1: "Lukisan 1",
    ID_FRAME_2: "Lukisan 2"
}

    # Furniture Positions (Mutable)
FURNITURE_POSITIONS = {
        ID_BED: [-2.5, -2.8, 1.5],
        ID_WARDROBE: [6.0, -0.5, -4.5],
        ID_DESK: [-5.5, -2.7, -4],
        ID_CHAIR: [-5.5, -2.8, -2.2],
        ID_WINDOW: [-8.85, 2.5, 2.5],
        ID_LAMP: [0, 6, 0],
        ID_FRAME_1: [3.5, 2.5, -8.8],
        ID_FRAME_2: [-3.5, 2.0, -8.8]
    }

    def draw_scene(select_mode=False, selected_id=ID_NOTHING):
        # Floor and Walls (Not selectable)
        if not select_mode:
            draw_floor()
            draw_walls()
        
        # Helper to handle positioning, selection
        def draw_object(draw_func, obj_id, *args):
            pos = FURNITURE_POSITIONS.get(obj_id, [0,0,0])
            glPushMatrix()
            glTranslatef(pos[0], pos[1], pos[2])
            
            # REMOVED SCALING
            # if not select_mode and obj_id == selected_id:
            #    glScalef(1.2, 1.2, 1.2)
            
            if select_mode:
                glPushName(obj_id)
            
            draw_func(*args)
            
            if select_mode:
                glPopName()
                
            glPopMatrix()

        # Draw Furniture with their positions
        draw_scene.draw_object = draw_object # Hack to use inner helper? No, just keep it linear or use closure
        
        # Redefining helper inside here is fine, but let's use the local dict
        draw_object(draw_bed, ID_BED)
        draw_object(draw_wardrobe, ID_WARDROBE)
        draw_object(draw_study_desk, ID_DESK)
        draw_object(draw_chair, ID_CHAIR)
        draw_object(draw_window, ID_WINDOW)
        draw_object(draw_ceiling_lamp, ID_LAMP)
        
        # Frames special case (args)
        # We need to pass args to draw_object
        def draw_object_args(draw_func, obj_id, *args):
            pos = FURNITURE_POSITIONS.get(obj_id, [0,0,0])
            glPushMatrix()
            glTranslatef(pos[0], pos[1], pos[2])
            if select_mode: glPushName(obj_id)
            draw_func(*args)
            if select_mode: glPopName()
            glPopMatrix()

        draw_object_args(draw_picture_frame, ID_FRAME_1, 0, 0, 0, 1.1, 1.3)
        draw_object_args(draw_picture_frame, ID_FRAME_2, 0, 0, 0, 1.3, 0.9)

    def get_clicked_object(x, y, camera, display):
        viewport = glGetIntegerv(GL_VIEWPORT)
        glSelectBuffer(512)
        glRenderMode(GL_SELECT)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        
        gluPickMatrix(x, viewport[3] - y, 5, 5, viewport)
        gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera.apply()
        
        draw_scene(select_mode=True)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glFlush()
        
        hits = glRenderMode(GL_RENDER)
        
        if hits:
            hits.sort(key=lambda x: x[0])
            closest_hit = hits[0]
            if closest_hit[2]:
                return closest_hit[2][0]
                
        return ID_NOTHING

    # ... CONSTANTS ...

    # ... MAIN ...
    camera = Camera()
    clock = pygame.time.Clock()
    selected_id = ID_NOTHING
    
    # Instructions
    print("\n" + "="*65)
    print("               KAMAR TIDUR 3D - GRAFIKA KOMPUTER")
    print("="*65)
    print("UPDATE KONTROL:")
    print("  * Klik Kiri Object : Pilih Object (Highlight di Console)")
    print("  * ARAH PANAH       : Geser Object Terpilih (X/Z)")
    print("  * PgUp / PgDn      : Geser Object Naik/Turun (Y)")
    print("  * W / S            : Zoom In / Out")
    print("  * A / D            : Putar Kamera (Kiri/Kanan)")
    print("  * Q / E            : Putar Kamera (Atas/Bawah)")
    print("  * R                : Reset Kamera")
    print("  * ESC              : Keluar")
    print("="*65 + "\n")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    camera = Camera()
                elif event.key == pygame.K_SPACE: # Deselect
                    selected_id = ID_NOTHING
                    pygame.display.set_caption("Kamar Tidur 3D")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    selected_id = get_clicked_object(mouse_pos[0], mouse_pos[1], camera, display)
                    
                    obj_name = FURNITURE_NAMES.get(selected_id, "")
                    caption = f"Terpilih: {obj_name} [Gunakan Panah utk Geser]" if obj_name else "Kamar Tidur 3D"
                    pygame.display.set_caption(caption)
                    if obj_name: print(f"Selected: {obj_name}")

        keys = pygame.key.get_pressed()
        
        # CAMERA CONTROLS (WASD + Q/E)
        if keys[pygame.K_w]: camera.distance = max(10, camera.distance - 0.5)
        if keys[pygame.K_s]: camera.distance = min(55, camera.distance + 0.5)
        if keys[pygame.K_a]: camera.rotation_y += 1.5
        if keys[pygame.K_d]: camera.rotation_y -= 1.5
        if keys[pygame.K_q]: camera.rotation_x += 1.5
        if keys[pygame.K_e]: camera.rotation_x -= 1.5

        # OBJECT MOVEMENT (Arrow Keys)
        if selected_id != ID_NOTHING:
            move_speed = 0.1
            pos = FURNITURE_POSITIONS[selected_id]
            # Movement relative to camera view roughly? Or absolute limits?
            # Absolute is easier for now.
            if keys[pygame.K_LEFT]:  pos[0] -= move_speed
            if keys[pygame.K_RIGHT]: pos[0] += move_speed
            if keys[pygame.K_UP]:    pos[2] -= move_speed # Forward (-Z)
            if keys[pygame.K_DOWN]:  pos[2] += move_speed # Backward (+Z)
            if keys[pygame.K_PAGEUP]: pos[1] += move_speed
            if keys[pygame.K_PAGEDOWN]: pos[1] -= move_speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        camera.apply()
        draw_scene(select_mode=False, selected_id=selected_id)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
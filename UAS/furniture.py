from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslate, glColor3f, glRotatef, glTranslatef, glDisable, glEnable, GL_LIGHTING, glBegin, glEnd, GL_LINES, glVertex3f
from shapes import draw_cube, draw_cylinder, draw_sphere

def draw_bed():
    """Kasur + bantal + headboard"""
    glPushMatrix()
    # Position moved to main scene

    # bed frame
    glPushMatrix()
    glTranslatef(0, 0.4, 0)
    draw_cube(5.5, 0.8, 3.2, (0.75, 0.70, 0.80))
    glPopMatrix()

    # mattress
    glPushMatrix()
    glTranslatef(0, 0.9, 0)
    draw_cube(5.2, 0.6, 3.0, (0.96, 0.96, 0.98))
    glPopMatrix()

    # blanket
    glPushMatrix()
    glTranslatef(0.2, 1.1, -0.2)
    draw_cube(5.0, 0.25, 2.6, (0.60, 0.75, 0.90))
    glPopMatrix()

    # pillows
    for px in [-1.2, 1.2]:
        glPushMatrix()
        glTranslatef(px, 1.15, -1.1)
        draw_cube(1.6, 0.35, 0.8, (0.95, 0.92, 0.90))
        glPopMatrix()

    # headboard
    glPushMatrix()
    glTranslatef(0, 1.2, -1.6)
    draw_cube(5.6, 1.6, 0.3, (0.55, 0.45, 0.55))
    glPopMatrix()

    # bed legs (4)
    for lx in [-2.4, 2.4]:
        for lz in [-1.3, 1.3]:
            glPushMatrix()
            glTranslatef(lx, 0.0, lz)
            glColor3f(0.25, 0.20, 0.15)
            draw_cylinder(0.08, 0.4, 10)
            glPopMatrix()

    glPopMatrix()

def draw_nightstand():
    """Meja samping kasur + lampu kecil"""
    glPushMatrix()
    glTranslatef(3.2, -2.5, 0.8)

    # nightstand body
    draw_cube(1.2, 1.0, 1.1, (0.45, 0.35, 0.25))

    # drawer
    glPushMatrix()
    glTranslatef(0, 0.15, 0.56)
    draw_cube(1.05, 0.35, 0.1, (0.55, 0.42, 0.30))
    glPopMatrix()

    # knob
    glPushMatrix()
    glTranslatef(0, 0.15, 0.65)
    glColor3f(0.9, 0.85, 0.6)
    draw_sphere(0.06, 12, 12)
    glPopMatrix()

    # lamp base
    glPushMatrix()
    glTranslatef(0, 0.7, 0)
    glColor3f(0.75, 0.75, 0.78)
    draw_cylinder(0.12, 0.35, 12)
    glPopMatrix()

    # lamp shade
    glPushMatrix()
    glTranslatef(0, 1.05, 0)
    draw_cube(0.6, 0.5, 0.6, (1.0, 0.95, 0.7))
    glPopMatrix()

    glPopMatrix()

def draw_wardrobe():
    """Lemari besar"""
    glPushMatrix()
    # Position moved to main scene

    # main body
    draw_cube(2.8, 5.0, 2.0, (0.70, 0.60, 0.50))

    # doors
    for dx in [-0.7, 0.7]:
        glPushMatrix()
        glTranslatef(dx, 0.2, 1.02)
        draw_cube(1.25, 4.6, 0.08, (0.78, 0.68, 0.58))
        glPopMatrix()

    # handles
    for hx in [-0.35, 0.35]:
        glPushMatrix()
        glTranslatef(hx, 0.3, 1.12)
        glColor3f(0.9, 0.85, 0.7)
        draw_cylinder(0.05, 0.6, 10)
        glPopMatrix()

    glPopMatrix()

def draw_study_desk():
    """Meja belajar + laptop"""
    glPushMatrix()
    # Position moved to main scene

    # desk top
    glPushMatrix()
    glTranslatef(0, 1.1, 0)
    draw_cube(3.2, 0.15, 1.4, (0.55, 0.40, 0.25))
    glPopMatrix()

    # legs
    for lx in [-1.4, 1.4]:
        for lz in [-0.6, 0.6]:
            glPushMatrix()
            glTranslatef(lx, 0.4, lz)
            draw_cube(0.15, 1.4, 0.15, (0.25, 0.25, 0.25))
            glPopMatrix()

    # laptop base
    glPushMatrix()
    glTranslatef(0, 1.25, 0)
    draw_cube(1.0, 0.05, 0.7, (0.15, 0.15, 0.15))
    glPopMatrix()

    # laptop screen
    glPushMatrix()
    glTranslatef(0, 1.55, -0.25)
    glRotatef(-70, 1, 0, 0)
    draw_cube(1.0, 0.7, 0.05, (0.05, 0.05, 0.05))
    glPopMatrix()

    # screen glow
    glPushMatrix()
    glTranslatef(0, 1.55, -0.22)
    glRotatef(-70, 1, 0, 0)
    draw_cube(0.9, 0.6, 0.02, (0.2, 0.35, 0.55))
    glPopMatrix()

    glPopMatrix()

def draw_chair():
    """Kursi meja belajar"""
    glPushMatrix()
    # Position moved to main scene

    # seat
    glPushMatrix()
    glTranslatef(0, 0.9, 0)
    draw_cube(1.0, 0.2, 1.0, (0.85, 0.75, 0.35))
    glPopMatrix()

    # backrest
    glPushMatrix()
    glTranslatef(0, 1.5, -0.4)
    draw_cube(1.0, 1.2, 0.2, (0.80, 0.70, 0.30))
    glPopMatrix()

    # legs
    for lx in [-0.4, 0.4]:
        for lz in [-0.4, 0.4]:
            glPushMatrix()
            glTranslatef(lx, 0.3, lz)
            draw_cube(0.12, 1.0, 0.12, (0.2, 0.2, 0.2))
            glPopMatrix()

    glPopMatrix()

def draw_window():
    """Jendela + kaca"""
    glPushMatrix()
    # Position moved to main scene

    # frame
    glPushMatrix()
    draw_cube(0.12, 3.0, 3.5, (0.9, 0.85, 0.6))
    glPopMatrix()

    # glass
    glPushMatrix()
    glTranslatef(0.08, 0, 0)
    draw_cube(0.02, 2.7, 3.2, (0.65, 0.85, 0.95))
    glPopMatrix()

    # grid lines
    glDisable(GL_LIGHTING)
    glColor3f(0.65, 0.55, 0.3)
    glBegin(GL_LINES)
    # vertical line
    glVertex3f(0.09, -1.2, 0)
    glVertex3f(0.09, 1.2, 0)
    # horizontal line
    glVertex3f(0.09, 0, -1.4)
    glVertex3f(0.09, 0, 1.4)
    glEnd()
    glEnable(GL_LIGHTING)

    glPopMatrix()

def draw_ceiling_lamp():
    """Lampu plafon"""
    glPushMatrix()
    # Position moved to main scene

    # cable
    glPushMatrix()
    glColor3f(0.15, 0.15, 0.15)
    draw_cylinder(0.04, 1.5, 10)
    glPopMatrix()

    # holder
    glPushMatrix()
    glTranslatef(0, -1, 0)
    draw_cube(0.6, 0.3, 0.6, (0.85, 0.85, 0.9))
    glPopMatrix()

    # lamp bulb
    glPushMatrix()
    glTranslatef(0, -1.6, 0)
    glColor3f(1, 0.95, 0.75)
    draw_sphere(0.45, 18, 18)
    glPopMatrix()

    glPopMatrix()

def draw_picture_frame(x, y, z, width, height):
    glPushMatrix()
    # Position handled externally now
    # glTranslatef(x, y, z) 

    # frame
    draw_cube(width + 0.2, height + 0.2, 0.08, (0.85, 0.75, 0.35))
    # picture
    glPushMatrix()
    glTranslatef(0, 0, 0.05)
    draw_cube(width, height, 0.02, (0.35, 0.55, 0.45))
    glPopMatrix()

    glPopMatrix()

def draw_plant():
    """Tanaman kecil"""
    glPushMatrix()
    glTranslatef(5.5, -2.7, 5.5)

    # pot
    glPushMatrix()
    glColor3f(0.7, 0.4, 0.3)
    draw_cylinder(0.35, 0.6, 16)
    glPopMatrix()

    # stem
    glPushMatrix()
    glTranslatef(0, 0.7, 0)
    glColor3f(0.2, 0.45, 0.15)
    draw_cylinder(0.08, 0.8, 10)
    glPopMatrix()

    # leaves
    for i, angle in enumerate([0, 120, 240]):
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glTranslatef(0.2, 1.2 + i*0.1, 0)
        glRotatef(45, 0, 0, 1)
        draw_cube(0.5, 0.05, 0.3, (0.25, 0.75, 0.25))
        glPopMatrix()

    glPopMatrix()

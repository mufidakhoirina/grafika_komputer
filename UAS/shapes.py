from OpenGL.GL import (
    glColor3fv, glBegin, glNormal3fv, glVertex3fv, glEnd, GL_QUADS, GL_QUAD_STRIP,
    GL_TRIANGLE_FAN, glNormal3f, glVertex3f
)
from OpenGL.GLU import gluNewQuadric, gluSphere
import math

def draw_cube(width, height, depth, color):
    w, h, d = width/2, height/2, depth/2
    glColor3fv(color)

    faces = [
        ([(-w,-h,d), (w,-h,d), (w,h,d), (-w,h,d)], (0,0,1)),       # front
        ([(-w,-h,-d), (-w,h,-d), (w,h,-d), (w,-h,-d)], (0,0,-1)),  # back
        ([(-w,h,-d), (-w,h,d), (w,h,d), (w,h,-d)], (0,1,0)),       # top
        ([(-w,-h,-d), (w,-h,-d), (w,-h,d), (-w,-h,d)], (0,-1,0)),  # bottom
        ([(-w,-h,-d), (-w,-h,d), (-w,h,d), (-w,h,-d)], (-1,0,0)),  # left
        ([(w,-h,-d), (w,h,-d), (w,h,d), (w,-h,d)], (1,0,0))        # right
    ]

    for vertices, normal in faces:
        glBegin(GL_QUADS)
        glNormal3fv(normal)
        for v in vertices:
            glVertex3fv(v)
        glEnd()

def draw_sphere(radius, slices=20, stacks=20):
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)

def draw_cylinder(radius, height, slices=20):
    # body
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        angle = 2 * math.pi * i / slices
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        glNormal3f(x/radius, 0, z/radius)
        glVertex3f(x, height/2, z)
        glVertex3f(x, -height/2, z)
    glEnd()

    # caps
    for y_pos, normal_y in [(height/2, 1), (-height/2, -1)]:
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, normal_y, 0)
        glVertex3f(0, y_pos, 0)
        for i in range(slices + 1):
            angle = 2 * math.pi * i / slices
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glVertex3f(x, y_pos, z)
        glEnd()

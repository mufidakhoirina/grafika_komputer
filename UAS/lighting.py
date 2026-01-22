from OpenGL.GL import (
    glEnable, GL_LIGHTING, GL_LIGHT0, GL_COLOR_MATERIAL,
    glColorMaterial, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glLightfv, GL_POSITION, GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR
)

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    light_position = [2, 8, 3, 1]
    light_ambient = [0.35, 0.35, 0.35, 1]
    light_diffuse = [1, 1, 1, 1]
    light_specular = [0.8, 0.8, 0.8, 1]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

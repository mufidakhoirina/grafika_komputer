from OpenGL.GL import glTranslatef, glRotatef

class Camera:
    def __init__(self):
        self.rotation_x = 25
        self.rotation_y = -45
        self.distance = 22
        self.pos_x = 0
        self.pos_y = -1

    def apply(self):
        glTranslatef(self.pos_x, self.pos_y, -self.distance)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

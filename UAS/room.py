from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef
from shapes import draw_cube

def draw_floor():
    # parquet style
    tile_size = 1.5
    tiles = 12

    for i in range(-tiles//2, tiles//2):
        for j in range(-tiles//2, tiles//2):
            if (i + j) % 2 == 0:
                color = (0.65, 0.50, 0.35)
            else:
                color = (0.60, 0.45, 0.30)

            glPushMatrix()
            glTranslatef(i * tile_size + tile_size/2, -3, j * tile_size + tile_size/2)
            draw_cube(tile_size, 0.08, tile_size, color)
            glPopMatrix()

def draw_walls():
    # back wall
    glPushMatrix()
    glTranslatef(0, 2, -9)
    draw_cube(18, 10, 0.2, (0.92, 0.90, 0.95))  # soft purple-white
    glPopMatrix()

    # left wall
    glPushMatrix()
    glTranslatef(-9, 2, 0)
    draw_cube(0.2, 10, 18, (0.88, 0.92, 0.95))  # light blue
    glPopMatrix()

    # right wall - REMOVED
    # glPushMatrix()
    # glTranslatef(9, 2, 0)
    # draw_cube(0.2, 10, 18, (0.95, 0.95, 0.95))  # white
    # glPopMatrix()

    # ceiling
    glPushMatrix()
    glTranslatef(0, 7, 0)
    draw_cube(18, 0.2, 18, (0.98, 0.98, 0.99))
    glPopMatrix()

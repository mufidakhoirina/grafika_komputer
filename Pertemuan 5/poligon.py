import turtle

def draw_dda_line_segment(t, x1, y1, x2, y2):
    """
    Menggambar SATU segmen garis menggunakan Algoritma DDA.
    """
    dx = x2 - x1
    dy = y2 - y1
    
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)
    if steps == 0:
        return
    
    x_increment = dx / steps
    y_increment = dy / steps
    
    x = float(x1)
    y = float(y1)
    
    t.penup()
    t.goto(round(x), round(y))
    t.pendown()
    
    for i in range(int(steps) + 1):
        pixel_x = round(x)
        pixel_y = round(y)
        
        t.dot(3)
        t.goto(pixel_x, pixel_y)
        
        x += x_increment
        y += y_increment

def draw_polygon_without_math(sides, side_length):
    """
    Menggambar poligon beraturan dengan menentukan titik sudut menggunakan 
    geometri Turtle (tanpa modul math) dan menggunakan DDA.
    """
    
    screen = turtle.Screen()
    screen.title("Poligon DDA Normal (Tepat di Tengah)")
    screen.setup(width=600, height=600)
    
    temp_t = turtle.Turtle() 
    temp_t.speed(0)
    temp_t.hideturtle()
    
    external_angle = 360 / sides
    
    initial_heading = (180 - external_angle) / 2 + 90
    
    temp_t.penup()
    
    if sides == 3:
        R_faktor = 0.8506 * side_length 
        vertical_offset = R_faktor
    else:
        vertical_offset = side_length 
        
    temp_t.goto(0, -vertical_offset / 2) 
    
    temp_t.setheading(initial_heading)

    vertices = []
    
    for i in range(sides):
        temp_t.forward(side_length)
        vertices.append((round(temp_t.xcor()), round(temp_t.ycor())))
        
        temp_t.left(external_angle) 
        
    temp_t.clear() 
    
    final_t = turtle.Turtle()
    final_t.speed(0)
    final_t.color("blue")
    final_t.hideturtle()
    
    num_vertices = len(vertices)
    
    for i in range(num_vertices):
        x_start, y_start = vertices[i]
        x_end, y_end = vertices[(i + 1) % num_vertices] 
        
        draw_dda_line_segment(final_t, x_start, y_start, x_end, y_end)
        
    screen.mainloop()

# --- DEFINISI PARAMETER UNTUK PENTAGON BERATURAN ---
SISI = 3                 
PANJANG_SISI = 50       

draw_polygon_without_math(SISI, PANJANG_SISI)
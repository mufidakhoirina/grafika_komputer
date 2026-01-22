import turtle

def draw_dda_line(x1, y1, x2, y2):
    """
    Menggambar garis dari (0, 0) ke (50, 50) menggunakan DDA.
    """
    print(f"--- Algoritma DDA ---")
    print(f"Titik Awal: ({x1}, {y1}) | Titik Akhir: ({x2}, {y2})")

    # 1. Hitung selisih
    dx = x2 - x1
    dy = y2 - y1
    
    # 2. Tentukan jumlah langkah (steps). Karena dx=dy, steps=50.
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)
    if steps == 0:
        return
    
    # 3. Hitung penambahan (increment). Karena dx=dy, x_inc=y_inc=1.
    x_increment = dx / steps
    y_increment = dy / steps
    
    # Inisialisasi posisi saat ini (floating point)
    x = float(x1)
    y = float(y1)
    
    # Setup Turtle
    screen = turtle.Screen()
    screen.title(f"Garis DDA: ({x1},{y1}) ke ({x2},{y2})")
    # Atur jendela agar dapat menampilkan koordinat 50
    screen.setup(width=400, height=400) 
    
    t = turtle.Turtle()
    t.speed(0)
    t.color("blue")
    t.hideturtle()
    t.penup()
    
    # Pindahkan ke posisi awal
    t.goto(round(x), round(y))
    t.pendown()
    
    print(f"Piksel yang digambar (total {int(steps) + 1} piksel):")
    
    # 4. Loop sebanyak 'steps' kali
    for i in range(int(steps) + 1):
        # Koordinat piksel yang digambar (bilangan bulat)
        pixel_x = round(x)
        pixel_y = round(y)
        
        # Pada kasus slope=1, piksel yang digambar adalah (0,0), (1,1), ..., (50,50)
        # print(f"({pixel_x}, {pixel_y})") 
        
        t.dot(3) 
        t.goto(pixel_x, pixel_y)
        
        # Hitung posisi baru (floating point)
        x += x_increment
        y += y_increment
        
    print(f"Garis DDA selesai digambar dalam {int(steps)} langkah.")
    screen.mainloop()

# --- Titik yang Anda definisikan ---
start_x = 50
start_y = 100
end_x = 250
end_y = 100

draw_dda_line(start_x, start_y, end_x, end_y)
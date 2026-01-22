import turtle

def plot_points(t, xpusat, ypusat, x, y):
    # 8 titik simetri lingkaran
    t.goto(xpusat + x, ypusat + y); t.dot(2)
    t.goto(xpusat - x, ypusat + y); t.dot(2)
    t.goto(xpusat + x, ypusat - y); t.dot(2)
    t.goto(xpusat - x, ypusat - y); t.dot(2)
    t.goto(xpusat + y, ypusat + x); t.dot(2)
    t.goto(xpusat - y, ypusat + x); t.dot(2)
    t.goto(xpusat + y, ypusat - x); t.dot(2)
    t.goto(xpusat - y, ypusat - x); t.dot(2)


def midpoint_circle(xpusat, ypusat, r):
    t = turtle.Turtle()
    t.penup()
    t.speed(10)
    t.hideturtle()

    x = 0
    y = r
    p = 1 - r   # nilai awal decision parameter

    plot_points(t, xpusat, ypusat, x, y)

    while x < y:
        x += 1
        if p < 0:
            p = p + 2*x + 1
        else:
            y -= 1
            p = p + 2*(x - y) + 1

        plot_points(t, xpusat, ypusat, x, y)

    turtle.done()


# ---- JALANKAN ----
midpoint_circle(0, 0, 50)

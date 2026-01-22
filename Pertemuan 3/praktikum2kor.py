# Ukuran layar 10x5 piksel(point 1)
lebar = 10
tinggi = 5

# Titik yang akan ditampilkan(point2)
x = 3
y = 2

for y in range(tinggi):
    for x in range(lebar):
        if x ==3 and y == 2:
            print("X", end=" ")
        else :
            print(".", end =" ")
    print()


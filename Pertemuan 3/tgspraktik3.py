   
lebar = 10
tinggi = 10

# Titik yang akan ditampilkan(point2)
x = 4
y = 6

for y in range(tinggi):
    for x in range(lebar):
        if x ==4 and y == 6:
            print("X", end=" ")
        else :
            print(".", end =" ")
    print()


import math
print("=== SOAL 1: Hitung Jarak dan Kuadran ===")

x1 = float(input("Masukkan x1: "))
y1 = float(input("Masukkan y1: "))
x2 = float(input("Masukkan x2: "))
y2 = float(input("Masukkan y2: "))

# Hitung jarak antara dua titik
jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Tentukan kuadran titik pertama
if x1 > 0 and y1 > 0:
    kuadran = "Kuadran I"
elif x1 < 0 and y1 > 0:
    kuadran = "Kuadran II"
elif x1 < 0 and y1 < 0:
    kuadran = "Kuadran III"
elif x1 > 0 and y1 < 0:
    kuadran = "Kuadran IV"
elif x1 == 0 and y1 == 0:
    kuadran = "Titik pusat (0,0)"
elif x1 == 0:
    kuadran = "Sumbu Y"
else:
    kuadran = "Sumbu X"

# Hasil output
print("\n=== HASIL ===")
print(f"Titik pertama: ({x1}, {y1})")
print(f"Titik kedua  : ({x2}, {y2})")
print(f"Jarak antar titik: {jarak:.2f}")
print(f"Titik pertama berada di: {kuadran}")

print("\n=== SOAL 2: Simulasi Layar Koordinat ===")

# Ukuran layar (lebar x tinggi)
lebar = 10
tinggi = 5

# Titik yang ingin ditampilkan
x = 3
y = 2

# Gambar layar 10x5
for j in range(tinggi):
    for i in range(lebar):
        if i == x and j == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()

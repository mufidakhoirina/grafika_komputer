Modern 3D Interactive Room Concept (Tkinter)

Project ini merupakan simulasi mini scene ruangan 3D interaktif menggunakan Python Tkinter Canvas dengan sistem rendering 3D sederhana berbasis perspective projection.
Scene menampilkan konsep ruang tamu modern (sofa, meja, karpet, dinding, lantai, dekorasi, tanaman, dan lampu) yang dapat diputar menggunakan tombol keyboard dan dapat di-zoom menggunakan mouse.

Scene 3D menampilkan:

✅ Ruangan (floor + wall + baseboard)
✅ Sofa modern + armrest + cushion
✅ Coffee table (top + legs)
✅ Karpet (rug)
✅ Wall decor / frame (art)
✅ Tanaman dalam vas
✅ Lampu berdiri (standing lamp)
✅ Shading sederhana menggunakan perhitungan normal dan dot product (ilusi pencahayaan)

Kontrol Interaksi
Input	Fungsi
Klik objek	Select / Interact (objek membesar sedikit)
Arrow Keys (← → ↑ ↓)	Rotasi kamera (sumbu X dan Y)
Scroll Mouse Wheel	Zoom in / Zoom out
Tombol X (Close window)	Keluar program
 Cara Menjalankan Program
1) Pastikan Python sudah terinstall
python --version

2) Jalankan file program

Misal nama file: living_room_3d.py

python living_room_3d.py
 Tidak membutuhkan library tambahan (Tkinter sudah bawaan Python).

 Konsep dan Teknik yang Digunakan
1) Representasi Objek 3D (Vertex & Face)

Objek dibangun dari kumpulan titik 3D (vertex) dan kumpulan bidang (faces).

Contoh:

create_box(w, h, d, color) untuk membuat balok/kubus

create_cylinder(radius, height, segments, color) untuk membuat silinder (pendekatan polygon)

2) Transformasi Geometri 3D

Setiap objek memiliki:

posisi (Vector3 pos)

skala (scale_val) yang berubah saat objek dipilih

Scaling dilakukan terhadap pusat objek dan dibuat smooth memakai transisi ke target_scale.

3) Kamera dan Rotasi View

Kamera disimulasikan dengan rotasi global semua vertex:

Rotasi terhadap sumbu Y → cam_angle_y

Rotasi terhadap sumbu X → cam_angle_x

Rotasi dikontrol menggunakan tombol panah.

4) Perspective Projection (Proyeksi Perspektif)

Titik 3D diproyeksikan ke layar 2D menggunakan rumus perspektif:

factor = FOV / (FOV + z)

px = cx + x * factor

py = cy + y * factor

Dengan konsep ini, objek yang lebih jauh terlihat lebih kecil (kedalaman terasa 3D).

5) Lighting & Shading (Ilusi Kedalaman)

Program menggunakan shading sederhana berbasis:

 Normal vector (cross product)
 Dot product dengan arah cahaya (light direction)
 Mengubah brightness warna berdasarkan intensitas

Ini menghasilkan efek gelap-terang yang membuat objek terlihat lebih realistis.

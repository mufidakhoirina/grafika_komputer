Pac-Man Clone (Pygame)

Project ini adalah game Pac-Man Clone sederhana yang dibuat menggunakan Python + Pygame.
Game memiliki fitur maze, pellet, power pellet, serta 4 ghost dengan mode AI dasar seperti pada Pac-Man klasik.

📌 Fitur Utama

✅ Maze (labirin) dengan wall collision
✅ Pac-Man dapat bergerak menggunakan keyboard
✅ Sistem pellet (+10 poin)
✅ Sistem power pellet (+50 poin) yang membuat ghost menjadi frightened
✅ 4 Ghost:

Blinky (Red)

Pinky (Pink)

Inky (Cyan)

Clyde (Orange)

✅ Ghost memiliki mode:

scatter (menuju titik pojok masing-masing)

chase (mengejar Pac-Man)

frightened (gerak random dan bisa dimakan)

✅ Sistem nyawa (Lives)
✅ Sistem level (naik level jika semua pellet habis)
✅ Tampilan UI: Score, Level, Lives, dan status ghost

🖼️ Screenshot Hasil Program

Tampilan game akan mirip seperti ini:

Score di kiri atas

Level di tengah atas

Lives di kanan atas

Informasi mode ghost di sisi kanan

(bisa ditambahkan screenshot dari folder jika kamu mau)

🎮 Kontrol Game
Tombol	Fungsi
Arrow Keys / WASD	Bergerak
ESC	Keluar dari game
R	Restart (saat game over)
⚙️ Cara Menjalankan Program
1) Install Python

Pastikan Python sudah terinstall. Cek dengan:

python --version

2) Install Pygame

Install pygame menggunakan pip:

pip install pygame

3) Jalankan Program

Misal nama file kamu pacman_clone.py, jalankan:

python pacman_clone.py

🧠 Penjelasan Singkat Cara Kerja Program
1. PacMan Class

Memiliki posisi grid (grid_x, grid_y) dan posisi pixel (x, y)

Bisa bergerak jika tidak ada wall

Memiliki mode:

normal

power_mode (aktif 10 detik)

2. Ghost Class

Setiap ghost memiliki:

Warna dan nama

Mode:

scatter

chase

frightened

AI sederhana memilih arah yang paling dekat menuju target (jarak Euclidean)

3. Maze Class

Menyimpan struktur labirin walls

Membuat pellet otomatis di semua jalur kosong

Menentukan lokasi power pellet (4 titik sudut)

4. Game Loop

Game berjalan dengan loop:

Input pemain

Update pacman dan ghost

Perhitungan pellet/power pellet

Collision pacman vs ghost

Render tampilan

✅ Sistem Skor & Nyawa
Skor

Makan pellet: +10

Makan power pellet: +50

Makan ghost saat frightened: +200

Nyawa

Awal nyawa: 3

Jika tertabrak ghost saat ghost tidak frightened → nyawa berkurang 1

Jika lives = 0 → Game Over

🚀 Pengembangan Lanjutan (Opsional)

Jika ingin dikembangkan lebih lanjut, bisa ditambahkan:

Sound effect dan background music

Animasi Pac-Man lebih halus

Ghost AI lebih akurat (Blinky, Pinky, Inky, Clyde sesuai versi asli)

Menu awal dan pause menu

High score system

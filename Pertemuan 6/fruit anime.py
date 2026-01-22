import pygame
import math
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta game
WIDTH, HEIGHT = 800, 600
FPS = 60
GRID_SIZE = 32

# Warna pixel art
BACKGROUND = (25, 25, 40)
PLATFORM_COLOR = (70, 60, 90)
PLAYER_BODY = (220, 60, 60)  # Warna merah Bakugo
PLAYER_HAIR = (255, 220, 0)  # Warna kuning Bakugo
PLAYER_OUTFIT = (40, 40, 60)  # Warna hitam
PLAYER_EYES = (30, 180, 255)  # Warna mata biru

# Warna buah-buahan
FRUIT_COLORS = [
    (255, 100, 100),    # Strawberry merah
    (255, 180, 50),     # Jeruk
    (255, 255, 100),    # Lemon
    (150, 255, 150),    # Melon hijau
    (255, 150, 255),    # Anggur ungu
    (100, 200, 255),    # Blueberry
    (255, 200, 100),    # Persik
]

# Warna power-up
POWERUP_COLOR = (255, 215, 0)  # Emas
POWERUP_GLOW = (255, 240, 180)

class Player:
    def __init__(self):
        # Posisi awal dalam grid
        self.grid_x = 1
        self.grid_y = 10
        self.x = self.grid_x * GRID_SIZE
        self.y = self.grid_y * GRID_SIZE
        
        # Status game
        self.score = 0
        self.fruits_eaten = 0
        self.has_powerup = False
        self.powerup_timer = 0
        self.speed_boost = False
        self.is_mirror_world = False
        
        # Animasi
        self.animation_frame = 0
        self.direction = 1  # 1 kanan, -1 kiri
        self.mouth_open = False
        self.mouth_timer = 0
        
        # Transformasi untuk ability
        self.scale = 1.0
        self.dash_cooldown = 0
        
    def update(self, dt):
        # Update animasi
        self.animation_frame += dt * 10
        if self.animation_frame > 4:
            self.animation_frame = 0
            
        # Update power-up timer
        if self.has_powerup:
            self.powerup_timer -= dt
            if self.powerup_timer <= 0:
                self.end_powerup()
                
        # Update dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
            
        # Update mouth animation
        if self.mouth_timer > 0:
            self.mouth_timer -= dt
            self.mouth_open = True
        else:
            self.mouth_open = False
            
    def move(self, dx, dy):
        # Normal movement
        move_speed = 5 if self.speed_boost else 3
        
        # Apply mirror world if active
        if self.is_mirror_world:
            dx *= -1
            
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        # Boundary check
        if 0 <= new_x < 24 and 0 <= new_y < 18:
            self.grid_x = new_x
            self.grid_y = new_y
            self.x = self.grid_x * GRID_SIZE
            self.y = self.grid_y * GRID_SIZE
            
            # Update direction
            if dx != 0:
                self.direction = 1 if dx > 0 else -1
                
    def dash(self):
        if self.dash_cooldown <= 0:
            # Dash ability (translasi cepat)
            dash_distance = 4 if self.speed_boost else 3
            self.move(dash_distance * self.direction, 0)
            self.dash_cooldown = 0.5  # 0.5 detik cooldown
            return True
        return False
        
    def eat_fruit(self, is_powerup=False):
        self.mouth_timer = 0.3  # Animasi mulut terbuka
        self.fruits_eaten += 1
        self.score += 100 if is_powerup else 10
        
        # Check for special fruit every 15 fruits
        if not is_powerup and self.fruits_eaten % 15 == 0:
            return "spawn_powerup"
            
        return "normal"
        
    def activate_powerup(self):
        # Power-up effect (scaling 1.5x dan speed boost)
        self.has_powerup = True
        self.powerup_timer = 5.0  # 5 detik
        self.scale = 1.5
        self.speed_boost = True
        
    def end_powerup(self):
        # Kembali ke ukuran normal setelah 5 detik
        self.has_powerup = False
        self.scale = 1.0
        self.speed_boost = False
        
    def toggle_mirror_world(self):
        # Refleksi terhadap sumbu-Y (dunia cermin)
        self.is_mirror_world = not self.is_mirror_world
        
    def draw(self, screen):
        # Hitung posisi pixel
        pixel_x = self.x + GRID_SIZE // 2
        pixel_y = self.y + GRID_SIZE // 2
        
        # Buat surface untuk karakter
        char_size = int(GRID_SIZE * 1.5 * self.scale)
        char_surface = pygame.Surface((char_size, char_size), pygame.SRCALPHA)
        
        # Gambar tubuh (pixel art Bakugo)
        body_rect = pygame.Rect(
            char_size // 2 - 6,
            char_size // 2 - 8,
            12,
            16
        )
        
        # Gambar baju
        pygame.draw.rect(char_surface, PLAYER_OUTFIT, body_rect)
        
        # Gambar kepala
        head_radius = 8
        head_x = char_size // 2
        head_y = char_size // 2 - 10
        
        pygame.draw.circle(char_surface, (255, 220, 180), (head_x, head_y), head_radius)
        
        # Gambar rambut (spiky hair Bakugo)
        hair_points = [
            (head_x - 8, head_y - 5),
            (head_x - 6, head_y - 10),
            (head_x, head_y - 12),
            (head_x + 6, head_y - 10),
            (head_x + 8, head_y - 5),
        ]
        pygame.draw.polygon(char_surface, PLAYER_HAIR, hair_points)
        
        # Gambar mata
        eye_offset = 3
        eye_y = head_y + 1
        
        # Mata biru khas
        pygame.draw.circle(char_surface, PLAYER_EYES, 
                          (head_x - eye_offset, eye_y), 3)
        pygame.draw.circle(char_surface, PLAYER_EYES, 
                          (head_x + eye_offset, eye_y), 3)
        
        # Pupil
        pygame.draw.circle(char_surface, (30, 30, 40), 
                          (head_x - eye_offset, eye_y), 1)
        pygame.draw.circle(char_surface, (30, 30, 40), 
                          (head_x + eye_offset, eye_y), 1)
        
        # Gambar mulut (animasi makan)
        if self.mouth_open:
            mouth_rect = pygame.Rect(head_x - 3, head_y + 5, 6, 3)
            pygame.draw.rect(char_surface, (200, 100, 100), mouth_rect)
        else:
            pygame.draw.line(char_surface, (150, 70, 70),
                            (head_x - 3, head_y + 5),
                            (head_x + 3, head_y + 5), 2)
        
        # Apply mirror jika di mirror world
        if self.is_mirror_world:
            char_surface = pygame.transform.flip(char_surface, True, False)
            
        # Gambar ke screen
        screen.blit(char_surface, (pixel_x - char_size // 2, pixel_y - char_size // 2))
        
        # Gambar efek power-up
        if self.has_powerup:
            # Efek glow
            glow_radius = int(math.sin(pygame.time.get_ticks() * 0.01) * 2 + char_size // 1.5)
            pygame.draw.circle(screen, POWERUP_GLOW + (50,), 
                             (pixel_x, pixel_y), glow_radius, 2)

class Fruit:
    def __init__(self, x, y, is_powerup=False):
        self.grid_x = x
        self.grid_y = y
        self.x = x * GRID_SIZE + GRID_SIZE // 2
        self.y = y * GRID_SIZE + GRID_SIZE // 2
        self.is_powerup = is_powerup
        self.color = POWERUP_COLOR if is_powerup else random.choice(FRUIT_COLORS)
        self.animation = random.random() * math.pi * 2
        self.collected = False
        self.radius = 10 if is_powerup else 6
        
    def update(self, dt):
        self.animation += dt * 3
        
    def draw(self, screen):
        if self.collected:
            return
            
        # Posisi dengan efek mengambang
        float_y = self.y + math.sin(self.animation) * 3
        
        # Gambar buah
        if self.is_powerup:
            # Buah power-up (berkelap-kelip)
            pulse = math.sin(self.animation * 2) * 0.3 + 0.7
            current_color = tuple(int(c * pulse) for c in self.color)
            
            # Gambar buah emas dengan efek khusus
            pygame.draw.circle(screen, current_color, (int(self.x), int(float_y)), self.radius)
            pygame.draw.circle(screen, (255, 255, 200), (int(self.x), int(float_y)), self.radius - 2)
            
            # Efek bintang
            for i in range(8):
                angle = self.animation + i * math.pi / 4
                star_x = self.x + math.cos(angle) * self.radius
                star_y = float_y + math.sin(angle) * self.radius
                pygame.draw.circle(screen, (255, 255, 255), (int(star_x), int(star_y)), 2)
        else:
            # Buah biasa
            pygame.draw.circle(screen, self.color, (int(self.x), int(float_y)), self.radius)
            
            # Detail buah (tangkai kecil)
            pygame.draw.circle(screen, (100, 150, 100), (int(self.x), int(float_y - 4)), 2)
            
            # Highlight
            highlight_x = self.x - 2
            highlight_y = float_y - 2
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(highlight_x), int(highlight_y)), 2)

class FruitAnimeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fruit Anime - Pixel Adventure")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.player = Player()
        self.fruits = []
        self.powerup_fruit = None
        
        # Game state
        self.game_over = False
        self.level = 1
        self.total_fruits = 0
        
        # UI Font
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Load pixel art platform
        self.platform_pattern = self.create_platform_pattern()
        
        # Setup level
        self.setup_level()
        
    def create_platform_pattern(self):
        """Buat pola pixel untuk platform"""
        pattern = pygame.Surface((GRID_SIZE, GRID_SIZE))
        pattern.fill(PLATFORM_COLOR)
        
        # Tambahkan detail pixel
        for x in range(0, GRID_SIZE, 4):
            for y in range(0, GRID_SIZE, 4):
                if (x + y) % 8 == 0:
                    color_variation = random.randint(-10, 10)
                    pixel_color = (
                        max(50, min(200, PLATFORM_COLOR[0] + color_variation)),
                        max(50, min(200, PLATFORM_COLOR[1] + color_variation)),
                        max(50, min(200, PLATFORM_COLOR[2] + color_variation))
                    )
                    pygame.draw.rect(pattern, pixel_color, (x, y, 2, 2))
                    
        return pattern
        
    def setup_level(self):
        """Setup level dengan buah-buahan berjajar"""
        self.fruits.clear()
        
        # Buat grid buah berjajar
        fruit_positions = []
        
        # Baris buah di tengah layar
        for row in range(3, 15):
            for col in range(3, 21):
                if (col + row) % 3 == 0:  # Pola teratur
                    fruit_positions.append((col, row))
                    
        # Tambahkan buah di posisi acak
        for _ in range(30):
            x = random.randint(2, 22)
            y = random.randint(2, 16)
            fruit_positions.append((x, y))
            
        # Buat buah-buahan
        for pos in fruit_positions:
            self.fruits.append(Fruit(pos[0], pos[1]))
            self.total_fruits += 1
            
        # Reset player position
        self.player.grid_x = 1
        self.player.grid_y = 10
        self.player.x = self.player.grid_x * GRID_SIZE
        self.player.y = self.player.grid_y * GRID_SIZE
        
    def spawn_powerup_fruit(self):
        """Spawn buah power-up khusus"""
        # Cari posisi yang tidak ada buah lain
        while True:
            x = random.randint(5, 20)
            y = random.randint(5, 15)
            
            # Cek tabrakan dengan buah lain
            collision = False
            for fruit in self.fruits:
                if fruit.grid_x == x and fruit.grid_y == y:
                    collision = True
                    break
                    
            if not collision:
                self.powerup_fruit = Fruit(x, y, True)
                break
                
    def handle_input(self):
        """Handle input dari keyboard"""
        keys = pygame.key.get_pressed()
        
        # Movement
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            
        if dx != 0 or dy != 0:
            self.player.move(dx, dy)
            
        # Dash ability
        if keys[pygame.K_SPACE]:
            self.player.dash()
            
        # Mirror world (untuk testing/debug)
        if keys[pygame.K_m] and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.player.toggle_mirror_world()
            
    def check_collisions(self):
        """Cek tabrakan dengan buah"""
        # Cek buah biasa
        for fruit in self.fruits[:]:
            if (not fruit.collected and 
                abs(self.player.grid_x - fruit.grid_x) < 1 and 
                abs(self.player.grid_y - fruit.grid_y) < 1):
                
                fruit.collected = True
                result = self.player.eat_fruit()
                
                if result == "spawn_powerup":
                    self.spawn_powerup_fruit()
                    
        # Cek power-up fruit
        if self.powerup_fruit and not self.powerup_fruit.collected:
            if (abs(self.player.grid_x - self.powerup_fruit.grid_x) < 1 and 
                abs(self.player.grid_y - self.powerup_fruit.grid_y) < 1):
                
                self.powerup_fruit.collected = True
                self.player.eat_fruit(True)
                self.player.activate_powerup()
                
    def update(self, dt):
        """Update game logic"""
        if self.game_over:
            return
            
        # Update player
        self.player.update(dt)
        
        # Update fruits
        for fruit in self.fruits:
            fruit.update(dt)
            
        if self.powerup_fruit:
            self.powerup_fruit.update(dt)
            
        # Check collisions
        self.check_collisions()
        
        # Check win condition
        fruits_left = sum(1 for f in self.fruits if not f.collected)
        if fruits_left == 0 and not self.powerup_fruit:
            self.level += 1
            self.setup_level()
            
    def draw_grid_background(self):
        """Gambar background grid pixel"""
        # Gambar platform utama
        for x in range(0, WIDTH, GRID_SIZE):
            for y in range(HEIGHT - GRID_SIZE * 3, HEIGHT, GRID_SIZE):
                self.screen.blit(self.platform_pattern, (x, y))
                
        # Gambar platform floating
        platforms = [
            (100, 300, 5, 1),
            (400, 250, 4, 1),
            (600, 350, 6, 1),
            (200, 150, 3, 1),
        ]
        
        for px, py, width, height in platforms:
            for wx in range(width):
                for wy in range(height):
                    self.screen.blit(self.platform_pattern, 
                                   (px + wx * GRID_SIZE, py + wy * GRID_SIZE))
                    
        # Gambar grid lines (untuk visual)
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 60, 50), 
                           (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 60, 50), 
                           (0, y), (WIDTH, y), 1)
            
    def draw_ui(self):
        """Gambar UI"""
        # Score
        score_text = self.font_medium.render(f"Score: {self.player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Fruits collected
        fruits_text = self.font_small.render(f"Fruits: {self.player.fruits_eaten}/15", True, (200, 200, 255))
        self.screen.blit(fruits_text, (10, 50))
        
        # Level
        level_text = self.font_small.render(f"Level: {self.level}", True, (255, 200, 200))
        self.screen.blit(level_text, (WIDTH - 120, 10))
        
        # Power-up timer
        if self.player.has_powerup:
            timer_text = self.font_small.render(
                f"Power: {self.player.powerup_timer:.1f}s", 
                True, POWERUP_COLOR
            )
            self.screen.blit(timer_text, (WIDTH - 150, 50))
            
        # Controls hint
        controls = [
            "ARROWS/WASD: Move",
            "SPACE: Dash",
            "Eat 15 fruits for special fruit!"
        ]
        
        for i, text in enumerate(controls):
            control_text = self.font_small.render(text, True, (180, 180, 200))
            self.screen.blit(control_text, (10, HEIGHT - 80 + i * 25))
            
        # Mirror world indicator
        if self.player.is_mirror_world:
            mirror_text = self.font_small.render("MIRROR WORLD", True, (255, 100, 255))
            self.screen.blit(mirror_text, (WIDTH // 2 - 70, 10))
            
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(BACKGROUND)
        
        # Draw background
        self.draw_grid_background()
        
        # Draw fruits
        for fruit in self.fruits:
            fruit.draw(self.screen)
            
        if self.powerup_fruit:
            self.powerup_fruit.draw(self.screen)
            
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_large.render("GAME OVER", True, (255, 100, 100))
            score_text = self.font_medium.render(f"Final Score: {self.player.score}", True, (255, 255, 255))
            
            self.screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 60))
            self.screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
            
        # Update display
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and self.game_over:
                        # Restart game
                        self.__init__()
                        
            # Game logic
            if not self.game_over:
                self.handle_input()
                self.update(dt)
                
            # Drawing
            self.draw()
            
        pygame.quit()
        sys.exit()

# Jalankan game
if __name__ == "__main__":
    game = FruitAnimeGame()
    game.run()
import pygame
import math
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta game
WIDTH, HEIGHT = 800, 600
FPS = 60
GRID_SIZE = 20
MAZE_WIDTH = 28
MAZE_HEIGHT = 31

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
POWER_PELLET_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 150)

class PacMan:
    def __init__(self):
        self.grid_x = 13
        self.grid_y = 23
        self.x = self.grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = self.grid_y * GRID_SIZE + GRID_SIZE // 2
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up
        self.next_direction = 0
        self.speed = 2
        self.radius = GRID_SIZE // 2 - 2
        self.mouth_angle = 0
        self.mouth_speed = 0.3
        self.is_alive = True
        self.power_mode = False
        self.power_timer = 0
        self.score = 0
        self.lives = 3
        
    def update(self, dt, maze):
        # Update mouth animation
        self.mouth_angle = (self.mouth_angle + self.mouth_speed) % 360
        
        # Update power mode
        if self.power_mode:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.power_mode = False
        
        # Try to change direction
        if self.can_move(self.next_direction, maze):
            self.direction = self.next_direction
        
        # Move in current direction
        if self.can_move(self.direction, maze):
            if self.direction == 0:  # Right
                self.x += self.speed
            elif self.direction == 1:  # Down
                self.y += self.speed
            elif self.direction == 2:  # Left
                self.x -= self.speed
            elif self.direction == 3:  # Up
                self.y -= self.speed
            
            # Update grid position
            self.grid_x = int(self.x // GRID_SIZE)
            self.grid_y = int(self.y // GRID_SIZE)
            
            # Tunnel wrap-around
            if self.grid_x < 0:
                self.x = (MAZE_WIDTH - 1) * GRID_SIZE + GRID_SIZE // 2
                self.grid_x = MAZE_WIDTH - 1
            elif self.grid_x >= MAZE_WIDTH:
                self.x = GRID_SIZE // 2
                self.grid_x = 0
    
    def can_move(self, direction, maze):
        next_x, next_y = self.grid_x, self.grid_y
        
        if direction == 0:  # Right
            next_x += 1
        elif direction == 1:  # Down
            next_y += 1
        elif direction == 2:  # Left
            next_x -= 1
        elif direction == 3:  # Up
            next_y -= 1
        
        # Check bounds
        if next_x < 0 or next_x >= MAZE_WIDTH or next_y < 0 or next_y >= MAZE_HEIGHT:
            return False
        
        # Check wall collision
        if next_y < len(maze) and next_x < len(maze[next_y]):
            return not maze[next_y][next_x]
        return False
    
    def set_direction(self, direction):
        self.next_direction = direction
    
    def eat_pellet(self, pellets, power_pellets):
        # Check for regular pellets
        if (self.grid_y < len(pellets) and self.grid_x < len(pellets[self.grid_y]) and 
            pellets[self.grid_y][self.grid_x]):
            pellets[self.grid_y][self.grid_x] = False
            self.score += 10
            return "pellet"
        
        # Check for power pellets
        if (self.grid_y < len(power_pellets) and self.grid_x < len(power_pellets[self.grid_y]) and 
            power_pellets[self.grid_y][self.grid_x]):
            power_pellets[self.grid_y][self.grid_x] = False
            self.score += 50
            self.power_mode = True
            self.power_timer = 10  # 10 seconds
            return "power_pellet"
        
        return None
    
    def draw(self, screen):
        if not self.is_alive:
            return
            
        # Calculate mouth opening based on animation
        mouth_open = 30 + 20 * math.sin(self.mouth_angle)
        
        # Draw Pac-Man
        start_angle = math.radians(mouth_open + self.direction * 90)
        end_angle = math.radians(360 - mouth_open + self.direction * 90)
        
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        
        # Create mouth by drawing a pie and then covering part of it
        points = []
        points.append((self.x, self.y))
        
        # First edge of mouth
        points.append((
            self.x + self.radius * math.cos(start_angle),
            self.y + self.radius * math.sin(start_angle)
        ))
        
        # Arc points
        for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1, 5):
            rad = math.radians(angle)
            points.append((
                self.x + self.radius * math.cos(rad),
                self.y + self.radius * math.sin(rad)
            ))
        
        # Second edge of mouth
        points.append((
            self.x + self.radius * math.cos(end_angle),
            self.y + self.radius * math.sin(end_angle)
        ))
        
        # Draw black polygon to create mouth
        if len(points) > 2:
            pygame.draw.polygon(screen, BLACK, points)

class Ghost:
    def __init__(self, color, name, scatter_target):
        self.color = color
        self.name = name
        self.grid_x = 13
        self.grid_y = 11
        self.x = self.grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = self.grid_y * GRID_SIZE + GRID_SIZE // 2
        self.direction = random.randint(0, 3)
        self.speed = 1.5
        self.radius = GRID_SIZE // 2 - 2
        self.mode = "scatter"  # scatter, chase, frightened
        self.mode_timer = 0
        self.scatter_target = scatter_target
        self.is_alive = True
        self.frightened_timer = 0
        self.eye_direction = 2  # Default looking left
        
    def update(self, dt, maze, pacman):
        # Update mode timers
        self.mode_timer -= dt
        
        if self.mode == "frightened":
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.mode = "chase"
                self.speed = 1.5
        
        # Choose target based on mode
        if self.mode == "scatter":
            target_x, target_y = self.scatter_target
        elif self.mode == "chase":
            target_x, target_y = pacman.grid_x, pacman.grid_y
        elif self.mode == "frightened":
            # Random movement when frightened
            target_x = random.randint(0, MAZE_WIDTH - 1)
            target_y = random.randint(0, MAZE_HEIGHT - 1)
        
        # Find best direction
        best_direction = self.find_best_direction(maze, target_x, target_y)
        
        if best_direction is not None:
            self.direction = best_direction
        
        # Move in current direction
        if self.can_move(self.direction, maze):
            if self.direction == 0:  # Right
                self.x += self.speed
                self.eye_direction = 0
            elif self.direction == 1:  # Down
                self.y += self.speed
                self.eye_direction = 1
            elif self.direction == 2:  # Left
                self.x -= self.speed
                self.eye_direction = 2
            elif self.direction == 3:  # Up
                self.y -= self.speed
                self.eye_direction = 3
            
            # Update grid position
            self.grid_x = int(self.x // GRID_SIZE)
            self.grid_y = int(self.y // GRID_SIZE)
            
            # Tunnel wrap-around
            if self.grid_x < 0:
                self.x = (MAZE_WIDTH - 1) * GRID_SIZE + GRID_SIZE // 2
                self.grid_x = MAZE_WIDTH - 1
            elif self.grid_x >= MAZE_WIDTH:
                self.x = GRID_SIZE // 2
                self.grid_x = 0
    
    def can_move(self, direction, maze):
        next_x, next_y = self.grid_x, self.grid_y
        
        if direction == 0:  # Right
            next_x += 1
        elif direction == 1:  # Down
            next_y += 1
        elif direction == 2:  # Left
            next_x -= 1
        elif direction == 3:  # Up
            next_y -= 1
        
        # Check bounds
        if next_x < 0 or next_x >= MAZE_WIDTH or next_y < 0 or next_y >= MAZE_HEIGHT:
            return False
        
        # Check wall collision
        if next_y < len(maze) and next_x < len(maze[next_y]):
            return not maze[next_y][next_x]
        return False
    
    def find_best_direction(self, maze, target_x, target_y):
        # Don't reverse direction unless necessary
        possible_directions = []
        
        for direction in range(4):
            # Don't go back the way we came
            if (direction == 0 and self.direction == 2) or \
               (direction == 2 and self.direction == 0) or \
               (direction == 1 and self.direction == 3) or \
               (direction == 3 and self.direction == 1):
                continue
            
            if self.can_move(direction, maze):
                possible_directions.append(direction)
        
        if not possible_directions:
            # If no other options, allow reversal
            for direction in range(4):
                if self.can_move(direction, maze):
                    possible_directions.append(direction)
        
        if not possible_directions:
            return None
        
        # Find direction that gets closest to target
        best_dir = possible_directions[0]
        best_distance = float('inf')
        
        for direction in possible_directions:
            next_x, next_y = self.grid_x, self.grid_y
            
            if direction == 0:
                next_x += 1
            elif direction == 1:
                next_y += 1
            elif direction == 2:
                next_x -= 1
            elif direction == 3:
                next_y -= 1
            
            distance = math.sqrt((next_x - target_x) ** 2 + (next_y - target_y) ** 2)
            
            if distance < best_distance:
                best_distance = distance
                best_dir = direction
        
        return best_dir
    
    def set_frightened(self):
        self.mode = "frightened"
        self.frightened_timer = 10  # 10 seconds
        self.speed = 1.0
    
    def draw(self, screen):
        if not self.is_alive:
            return
            
        # Draw ghost body
        if self.mode == "frightened":
            color = BLUE
            # Flash when timer is low
            if self.frightened_timer < 3:
                if int(self.frightened_timer * 2) % 2 == 0:
                    color = WHITE
        else:
            color = self.color
        
        # Draw ghost body (rounded rectangle)
        rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        pygame.draw.rect(screen, color, rect, 0, self.radius // 2)
        
        # Draw ghost bottom (wavy)
        points = []
        for i in range(8):
            x = self.x - self.radius + (i * self.radius * 2 / 7)
            y_offset = 5 * math.sin(i + pygame.time.get_ticks() * 0.01)
            points.append((x, self.y + self.radius - y_offset))
        
        # Close the shape
        points.append((self.x + self.radius, self.y + self.radius))
        points.append((self.x - self.radius, self.y + self.radius))
        
        pygame.draw.polygon(screen, color, points)
        
        # Draw eyes
        eye_radius = self.radius // 3
        left_eye_x = self.x - eye_radius
        right_eye_x = self.x + eye_radius
        eye_y = self.y - eye_radius // 2
        
        # Eye whites
        pygame.draw.circle(screen, WHITE, (int(left_eye_x), int(eye_y)), eye_radius)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x), int(eye_y)), eye_radius)
        
        # Eye pupils
        pupil_offset = eye_radius // 2
        pupil_x, pupil_y = left_eye_x, eye_y
        
        if self.eye_direction == 0:  # Right
            pupil_x += pupil_offset
        elif self.eye_direction == 1:  # Down
            pupil_y += pupil_offset
        elif self.eye_direction == 2:  # Left
            pupil_x -= pupil_offset
        elif self.eye_direction == 3:  # Up
            pupil_y -= pupil_offset
        
        pygame.draw.circle(screen, BLUE, (int(pupil_x), int(pupil_y)), eye_radius // 2)
        
        pupil_x, pupil_y = right_eye_x, eye_y
        
        if self.eye_direction == 0:  # Right
            pupil_x += pupil_offset
        elif self.eye_direction == 1:  # Down
            pupil_y += pupil_offset
        elif self.eye_direction == 2:  # Left
            pupil_x -= pupil_offset
        elif self.eye_direction == 3:  # Up
            pupil_y -= pupil_offset
        
        pygame.draw.circle(screen, BLUE, (int(pupil_x), int(pupil_y)), eye_radius // 2)

class Maze:
    def __init__(self):
        self.walls = self.create_maze()
        self.pellets = self.create_pellets()
        self.power_pellets = self.create_power_pellets()
        
    def create_maze(self):
        # Classic Pac-Man maze layout (simplified)
        maze = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
            [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
            [1,0,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,0,1],
            [1,0,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,0,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        
        # Pastikan maze memiliki tinggi yang benar
        if len(maze) != MAZE_HEIGHT:
            # Potong atau tambah baris jika perlu
            maze = maze[:MAZE_HEIGHT]
            while len(maze) < MAZE_HEIGHT:
                maze.append([1] * MAZE_WIDTH)
        
        return maze
    
    def create_pellets(self):
        pellets = []
        for y in range(MAZE_HEIGHT):
            row = []
            for x in range(MAZE_WIDTH):
                # Pastikan koordinat valid
                if y < len(self.walls) and x < len(self.walls[y]):
                    # Don't place pellets on walls or in ghost house
                    if self.walls[y][x] == 0 and not (12 <= x <= 15 and 13 <= y <= 15):
                        row.append(True)
                    else:
                        row.append(False)
                else:
                    row.append(False)
            pellets.append(row)
        return pellets
    
    def create_power_pellets(self):
        power_pellets = [[False for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
        
        # Classic power pellet positions (pastikan dalam bounds)
        positions = [(1, 3), (26, 3), (1, 23), (26, 23)]
        
        for x, y in positions:
            if y < MAZE_HEIGHT and x < MAZE_WIDTH:
                power_pellets[y][x] = True
            
        return power_pellets
    
    def draw(self, screen):
        # Draw walls
        for y in range(min(MAZE_HEIGHT, len(self.walls))):
            for x in range(min(MAZE_WIDTH, len(self.walls[y]))):
                if self.walls[y][x] == 1:
                    rect = pygame.Rect(
                        x * GRID_SIZE,
                        y * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    )
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                    
                    # Add some texture to walls
                    pygame.draw.rect(screen, (0, 0, 100), rect, 1)
        
        # Draw pellets
        for y in range(min(MAZE_HEIGHT, len(self.pellets))):
            for x in range(min(MAZE_WIDTH, len(self.pellets[y]))):
                if self.pellets[y][x]:
                    center_x = x * GRID_SIZE + GRID_SIZE // 2
                    center_y = y * GRID_SIZE + GRID_SIZE // 2
                    pygame.draw.circle(screen, WHITE, (center_x, center_y), 3)
        
        # Draw power pellets
        for y in range(min(MAZE_HEIGHT, len(self.power_pellets))):
            for x in range(min(MAZE_WIDTH, len(self.power_pellets[y]))):
                if self.power_pellets[y][x]:
                    center_x = x * GRID_SIZE + GRID_SIZE // 2
                    center_y = y * GRID_SIZE + GRID_SIZE // 2
                    pygame.draw.circle(screen, POWER_PELLET_COLOR, (center_x, center_y), 8)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man Clone")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.maze = Maze()
        self.pacman = PacMan()
        
        # Create ghosts with their scatter targets
        self.ghosts = [
            Ghost(RED, "Blinky", (25, 0)),
            Ghost(PINK, "Pinky", (2, 0)),
            Ghost(CYAN, "Inky", (27, 30)),
            Ghost(ORANGE, "Clyde", (0, 30))
        ]
        
        # Game state
        self.game_over = False
        self.level = 1
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Ghost mode timers
        self.scatter_timer = 7.0
        self.chase_timer = 20.0
        self.current_mode = "scatter"
        self.mode_timer = self.scatter_timer
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pacman.set_direction(0)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pacman.set_direction(1)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pacman.set_direction(2)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pacman.set_direction(3)
    
    def update_ghost_modes(self, dt):
        self.mode_timer -= dt
        
        if self.mode_timer <= 0:
            if self.current_mode == "scatter":
                self.current_mode = "chase"
                self.mode_timer = self.chase_timer
            else:
                self.current_mode = "scatter"
                self.mode_timer = self.scatter_timer
            
            # Update all ghosts
            for ghost in self.ghosts:
                if ghost.mode != "frightened":
                    ghost.mode = self.current_mode
    
    def check_collisions(self):
        # Check ghost collisions
        for ghost in self.ghosts:
            if (abs(self.pacman.grid_x - ghost.grid_x) < 1 and 
                abs(self.pacman.grid_y - ghost.grid_y) < 1):
                
                if ghost.mode == "frightened":
                    # Pac-Man eats ghost
                    ghost.grid_x = 13
                    ghost.grid_y = 11
                    ghost.x = ghost.grid_x * GRID_SIZE + GRID_SIZE // 2
                    ghost.y = ghost.grid_y * GRID_SIZE + GRID_SIZE // 2
                    ghost.mode = "chase"
                    self.pacman.score += 200
                else:
                    # Ghost catches Pac-Man
                    self.pacman.lives -= 1
                    self.pacman.grid_x = 13
                    self.pacman.grid_y = 23
                    self.pacman.x = self.pacman.grid_x * GRID_SIZE + GRID_SIZE // 2
                    self.pacman.y = self.pacman.grid_y * GRID_SIZE + GRID_SIZE // 2
                    
                    # Reset ghosts
                    for g in self.ghosts:
                        g.grid_x = 13
                        g.grid_y = 11
                        g.x = g.grid_x * GRID_SIZE + GRID_SIZE // 2
                        g.y = g.grid_y * GRID_SIZE + GRID_SIZE // 2
                        if g.mode != "frightened":
                            g.mode = "scatter"
                    
                    if self.pacman.lives <= 0:
                        self.game_over = True
                    break
    
    def update(self, dt):
        if self.game_over:
            return
            
        # Update Pac-Man
        self.pacman.update(dt, self.maze.walls)
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(dt, self.maze.walls, self.pacman)
        
        # Update ghost modes
        self.update_ghost_modes(dt)
        
        # Check pellet eating
        result = self.pacman.eat_pellet(self.maze.pellets, self.maze.power_pellets)
        if result == "power_pellet":
            # Make all ghosts frightened
            for ghost in self.ghosts:
                ghost.set_frightened()
        
        # Check collisions
        self.check_collisions()
        
        # Check win condition
        pellets_left = 0
        for row in self.maze.pellets:
            pellets_left += sum(row)
        
        power_pellets_left = 0
        for row in self.maze.power_pellets:
            power_pellets_left += sum(row)
        
        if pellets_left == 0 and power_pellets_left == 0:
            self.level += 1
            self.maze = Maze()
            self.pacman.grid_x = 13
            self.pacman.grid_y = 23
            self.pacman.x = self.pacman.grid_x * GRID_SIZE + GRID_SIZE // 2
            self.pacman.y = self.pacman.grid_y * GRID_SIZE + GRID_SIZE // 2
            
            # Reset ghosts
            for ghost in self.ghosts:
                ghost.grid_x = 13
                ghost.grid_y = 11
                ghost.x = ghost.grid_x * GRID_SIZE + GRID_SIZE // 2
                ghost.y = ghost.grid_y * GRID_SIZE + GRID_SIZE // 2
                ghost.mode = "scatter"
    
    def draw(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw maze
        self.maze.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw Pac-Man
        self.pacman.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.pacman.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f"Lives: {self.pacman.lives}", True, WHITE)
        self.screen.blit(lives_text, (WIDTH - 150, 10))
        
        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (WIDTH // 2 - 40, 10))
        
        # Draw power mode indicator
        if self.pacman.power_mode:
            power_text = self.small_font.render("POWER MODE!", True, BLUE)
            self.screen.blit(power_text, (WIDTH // 2 - 60, 40))
        
        # Draw controls
        controls = [
            "ARROWS/WASD: Move",
            "ESC: Quit",
            "R: Restart"
        ]
        
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, (150, 150, 150))
            self.screen.blit(control_text, (10, HEIGHT - 80 + i * 25))
        
        # Draw ghost names and status
        ghost_info = []
        for i, ghost in enumerate(self.ghosts):
            if i < len(self.ghosts):
                ghost_info.append(f"{ghost.name}: {ghost.mode}")
        
        for i, info in enumerate(ghost_info):
            color = self.ghosts[i].color if self.ghosts[i].mode != "frightened" else BLUE
            info_text = self.small_font.render(info, True, color)
            self.screen.blit(info_text, (WIDTH - 200, 50 + i * 25))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, RED)
            final_score = self.font.render(f"Final Score: {self.pacman.score}", True, WHITE)
            restart_text = self.small_font.render("Press R to restart", True, YELLOW)
            
            self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
            self.screen.blit(final_score, (WIDTH // 2 - 120, HEIGHT // 2 - 20))
            self.screen.blit(restart_text, (WIDTH // 2 - 80, HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        if self.game_over:
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
    game = Game()
    game.run()
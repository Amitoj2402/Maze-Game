"""
    Maze Game

    Made by Ibraheem & Amitoj
"""

# Import required modules.
import pygame, sys, json

# Initialize pygame.
pygame.init()

# Define default properties.
WIDTH, HEIGHT = 800, 700
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# RGB color definitions.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game variables.
player_pos = [1, 1]  # Player's starting position in the maze grid.
finish_pos = [11, 18]  # Finish position in the maze grid.
move_delay = 200  # Delay between player moves in milliseconds.
last_move_time = 0  # Track the last move time to control move delay.
tile_change_delay = 100  # Delay for changing tiles in the editor mode.
last_tile_change_time = 0  # Track the last tile change time.
editor_mode = False  # Flag to check if the editor mode is active.
enable_editor_mode = True  # Flag to enable/disable editor mode.
running = True  # Flag to control the game loop.
start_time = pygame.time.get_ticks()  # Track the start time of the game.
win_time = None  # Track the time when the player wins.
max_maze_size = 50  # Define the maximum size of the maze.

# Load maze configuration and personal best time from the JSON file.
maze_file = './config.json'
with open(maze_file, 'r') as config:
    data = json.load(config)
    pb_time = data.get("PB", 0)  # Get personal best time, default to 0 if not found.
    maze = data.get("Maze", [[1] * (WIDTH // GRID_SIZE) for _ in range(HEIGHT // GRID_SIZE)])  # Get maze config.

def resize_maze(maze, max_size):
    # Ensure the maze is of the correct size by extending it if necessary.
    current_rows = len(maze)
    current_cols = len(maze[0])
    # Add rows if the current rows are less than the max size.
    if current_rows < max_size:
        for _ in range(max_size - current_rows):
            maze.append([1] * current_cols)
    # Add columns to each row if the current columns are less than the max size.
    if current_cols < max_size:
        for row in maze:
            row.extend([1] * (max_size - current_cols))
    # Trim the maze to ensure it fits within the max size.
    return [row[:max_size] for row in maze[:max_size]]

maze = resize_maze(maze, max_maze_size)

def draw_maze():
    # Draw the maze grid on the screen.
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            # Assign white if the tile is 0 (path) and black if the tile is 1 (wall).
            color = WHITE if maze[row][col] == 0 else BLACK
            # Draw the tile on the screen.
            pygame.draw.rect(screen, color, pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_player():
    # Draw the player on the screen.
    pygame.draw.rect(screen, BLUE, pygame.Rect(player_pos[1] * GRID_SIZE, player_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_finish():
    # Draw the finish tile on the screen.
    pygame.draw.rect(screen, GREEN, pygame.Rect(finish_pos[1] * GRID_SIZE, finish_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def move_player(dx, dy):
    """ Move the player in the specified direction (dx, dy).
        Calculate new player position. """
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    # Check if the new position is within the maze boundaries and not a wall.
    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] == 0:
        # Update player position.
        player_pos[0], player_pos[1] = new_x, new_y

def toggle_wall(pos):
    # Toggle the wall state at the specified position in the maze.
    row, col = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
    # Check if the position is within the maze boundaries.
    if 0 <= row < len(maze) and 0 <= col < len(maze[0]):
        # Toggle between wall (1) and path (0).
        maze[row][col] = 0 if maze[row][col] == 1 else 1

# Main game loop.
while running:
    current_time = pygame.time.get_ticks()  # Get the current time.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the game loop if the window is closed.
        elif enable_editor_mode and event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click toggles editor mode.
            editor_mode = not editor_mode
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pb_time = 0  # Reset the personal best timer if space is pressed.

    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    # If in editor mode and left mouse button is pressed, toggle wall state.
    if editor_mode and mouse_buttons[0] and current_time - last_tile_change_time > tile_change_delay:
        toggle_wall(mouse_pos)
        last_tile_change_time = current_time

    keys = pygame.key.get_pressed()
    # If not in editor mode, check for player movement keys.
    if not editor_mode:
        if keys[pygame.K_UP] and current_time - last_move_time > move_delay:
            move_player(-1, 0)
            last_move_time = current_time
        elif keys[pygame.K_DOWN] and current_time - last_move_time > move_delay:
            move_player(1, 0)
            last_move_time = current_time
        elif keys[pygame.K_LEFT] and current_time - last_move_time > move_delay:
            move_player(0, -1)
            last_move_time = current_time
        elif keys[pygame.K_RIGHT] and current_time - last_move_time > move_delay:
            move_player(0, 1)
            last_move_time = current_time

    # Clear the screen.
    screen.fill(BLACK)
    # Draw maze, player, and finish tile.
    draw_maze()
    draw_player()
    draw_finish()

    # If in editor mode, display "Editor Mode" text.
    if editor_mode:
        font = pygame.font.Font(None, 36)
        text = font.render("Editor Mode", True, GREEN)
        screen.blit(text, (10, 10))

    # Check if player reached the finish position.
    if player_pos == finish_pos:
        if win_time is None:
            win_time = current_time
        # Display "You Win!" text.
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, GREEN)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds before closing the game.
        running = False
    else:
        # Display the elapsed time.
        elapsed_time_ms = current_time - start_time
        elapsed_seconds = elapsed_time_ms // 1000
        elapsed_milliseconds = elapsed_time_ms % 1000
        timer_color = GREEN if pb_time == 0 or elapsed_seconds < pb_time else RED
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {elapsed_seconds}.{elapsed_milliseconds:03}s", True, timer_color)
        screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, HEIGHT - 40))
    
    # Flip screen because pygame flips arrays.
    pygame.display.flip()
    pygame.time.Clock().tick(30)  # Limit the game to 30 frames per second.

# Update personal best time if player won.
if win_time is not None:
    elapsed_time_ms = win_time - start_time
    elapsed_seconds = elapsed_time_ms // 1000
    if pb_time == 0 or elapsed_seconds < pb_time:
        pb_time = elapsed_seconds

# Save maze configuration and personal best time to the JSON file.
data = {
    "PB": pb_time,
    "Maze": maze
}
with open(maze_file, 'w') as config:
    json.dump(data, config, indent=2)

# Quit pygame and exit the program.
pygame.quit()
sys.exit()
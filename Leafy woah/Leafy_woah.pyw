import pygame
import random
import time
import os
import sys

pygame.init()

# Function to get the correct file path for bundled assets
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")  # For normal execution
    return os.path.join(base_path, relative_path)

# Screen dimensions
width = 800
height = 500

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Leafy Woah")  # Change the game title to "Leafy Woah"

# Load the game icon (use resource_path for bundled assets)
icon = pygame.image.load(resource_path('leafy.png'))
pygame.display.set_icon(icon)

# Player
image1_not_scaled = pygame.image.load(resource_path('leafy.png'))
image1 = pygame.transform.scale(image1_not_scaled, (42, 71))  # Player sprite size
playerx = 400
playery = 250
player_speed = 1  # Speed for movement

# Enemy
enemy1_not_scaled = pygame.image.load(resource_path('acid.png'))
enemy1 = pygame.transform.scale(enemy1_not_scaled, (68, 55))  # Enemy sprite size
enemy_speed = 0.5  # Initial speed of the enemies

# Player hitbox (1.5 times smaller than the sprite)
player_hitbox_width = 42 // 1.5
player_hitbox_height = 71 // 1.5
player_hitbox_offset_x = (42 - player_hitbox_width) // 2  # Center the hitbox inside the sprite
player_hitbox_offset_y = (71 - player_hitbox_height) // 2  # Center the hitbox inside the sprite

# Enemy hitbox (1.5 times smaller than the sprite)
enemy_hitbox_width = 68 // 1.5
enemy_hitbox_height = 55 // 1.5
enemy_hitbox_offset_x = (68 - enemy_hitbox_width) // 2  # Center the hitbox inside the sprite
enemy_hitbox_offset_y = (55 - enemy_hitbox_height) // 2  # Center the hitbox inside the sprite

# Player score
score = 0
start_time = time.time()  # Keep track of time since the game started

# Create a list of enemies with random vertical positions
def create_enemies():
    enemies = []
    for i in range(20):  # Create 20 enemies
        enemyx = 800 + i * 80  # Start enemies off-screen to the right, spaced closely
        enemyy = random.randint(0, height - 55)  # Random vertical position within the screen height
        enemies.append([enemyx, enemyy])  # Each enemy is represented as a list of [x, y]
    return enemies

# Game Over screen
def game_over():
    # Display a game over screen and ask to play again
    font = pygame.font.SysFont("arial", 50)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 50))

    play_again_font = pygame.font.SysFont("arial", 30)
    play_again_text = play_again_font.render("Press SPACE to Play Again", True, (255, 255, 255))
    screen.blit(play_again_text, (width // 2 - play_again_text.get_width() // 2, height // 2 + 50))

    pygame.display.flip()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()  # Restart the game

# Countdown before the game starts
def countdown():
    font = pygame.font.SysFont("arial", 100)
    for i in range(5, 0, -1):
        screen.fill((128, 0, 128))  # Purple background
        countdown_text = font.render(str(i), True, (255, 255, 255))
        screen.blit(countdown_text, (width // 2 - countdown_text.get_width() // 2, height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

    # After countdown, show "START"
    screen.fill((128, 0, 128))
    start_text = font.render("START", True, (255, 255, 255))
    screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - start_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

# Function to update enemy speed over time
def update_enemy_speed():
    global enemy_speed
    elapsed_time = time.time() - start_time  # Time elapsed since game started

    # Increase enemy speed after every 30 seconds (this is an example)
    if elapsed_time > 30:
        enemy_speed = 1.0  # Speed up after 30 seconds
    if elapsed_time > 60:
        enemy_speed = 1.5  # Speed up after 60 seconds
    if elapsed_time > 90:
        enemy_speed = 2.0  # Speed up after 90 seconds
    # You can continue to add more conditions to increase speed after more time

# Main game loop
def main():
    global playerx, playery, score, start_time, enemy_speed

    # Reset player position and score
    playerx = 400
    playery = 250
    score = 0
    start_time = time.time()  # Reset the time when the game restarts
    enemy_speed = 0.5  # Initial enemy speed

    # Initialize enemies
    enemies = create_enemies()

    running = True  # running and quit
    while running:
        screen.fill((128, 0, 128))  # Fill the screen with a color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Keystroke handling
        keys = pygame.key.get_pressed()  # Get the state of all keys

        # Movement in all directions
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player_speed  # Move left
        if keys[pygame.K_RIGHT]:
            dx = player_speed  # Move right
        if keys[pygame.K_UP]:
            dy = -player_speed  # Move up
        if keys[pygame.K_DOWN]:
            dy = player_speed  # Move down

        # Apply movement
        playerx += dx
        playery += dy

        # Boundary checks for horizontal movement
        if playerx < 0:  # Stop at the left edge
            playerx = 0
        if playerx > width - 42:  # Stop at the right edge (42 is the width of the player)
            playerx = width - 42

        # Boundary checks for vertical movement
        if playery < 0:  # Stop at the top edge
            playery = 0
        if playery > height - 71:  # Stop at the bottom edge (71 is the height of the player)
            playery = height - 71

        # Update enemy positions and check for collisions
        for enemy_pos in enemies:
            enemy_pos[0] -= enemy_speed  # Move enemy left
            # Reset enemy position if it goes off-screen
            if enemy_pos[0] < -68:  # Off-screen to the left (68 is the width of the enemy)
                enemy_pos[0] = width  # Reset to the right side
                enemy_pos[1] = random.randint(0, height - 55)  # Randomize vertical position when reset

            # Check for collision with the player (based on hitboxes)
            if (playerx + player_hitbox_offset_x < enemy_pos[0] + enemy_hitbox_width and
                playerx + player_hitbox_offset_x + player_hitbox_width > enemy_pos[0] and
                playery + player_hitbox_offset_y < enemy_pos[1] + enemy_hitbox_height and
                playery + player_hitbox_offset_y + player_hitbox_height > enemy_pos[1]):
                game_over()  # Call game_over function if collision occurs

        # Increase score based on time (every second)
        score = int(time.time() - start_time)

        # Speed up the enemies as time goes on
        update_enemy_speed()

        # Draw enemies, player, and score
        draw_enemies(enemies)
        player()  # Draw the player
        display_score()  # Display the score
        pygame.display.flip()  # Update the display

# Function to draw enemies
def draw_enemies(enemies):
    for enemy_pos in enemies:
        screen.blit(enemy1, (enemy_pos[0], enemy_pos[1]))

# Function to draw the player
def player():
    screen.blit(image1, (playerx, playery))

# Function to display the score
def display_score():
    font = pygame.font.SysFont("arial", 30)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Display score at the top left corner

# Start the game with a countdown
countdown()

# Begin the game loop
main()

pygame.quit()

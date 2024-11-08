import pygame
import random
import time

# initialization pygame
pygame.init()

# Set screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set title
pygame.display.set_caption("Car Avoid Obstacles")

# Define color
black = (0, 0, 0)
white = (255, 255, 255)

# Load and scale images
try:
    player_image = pygame.image.load('car.jpg')  # car pictures
    player_image = pygame.transform.scale(player_image, (50, 50))  # Scale to 50x50 pixels
    obstacle_image = pygame.image.load('th.jpg')  # Obstacle pictures
    obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))  # Scale to 50x50 pixels
    background_image = pygame.image.load('background.jpg')  # background image
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale to screen size
except pygame.error as e:
    print(f"Unable to load image:{e}")
    exit()

# Player car settings
player_x = 0  # The player is always on the far left side of the screen
player_y = screen_height / 2  # The initial position is in the middle of the screen

# Obstacle setting
obstacle_speed = 5
obstacles = []  # Obstacle list
game_start_time = time.time()  # Record game start time

# game state
running = True
game_over = False
crashes = 0
max_crashes = 3

# Load font
font = pygame.font.Font(None, 36)

# Generate new obstacles
def generate_obstacle():
    obstacles.append([screen_width, random.randrange(0, screen_height - 50)])

# Game main loop
while running:
    current_time = time.time()
    dt = current_time - game_start_time  # Calculate game running time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and game_over:
                running = False
            elif event.key == pygame.K_c and game_over:
                game_over = False
                crashes = 0
                obstacles.clear()
                generate_obstacle()  # Regenerate obstacles
                player_x = 0
                player_y = screen_height / 2
                game_start_time = current_time  # Reset game start time

    if not game_over:
        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= 5
        if keys[pygame.K_DOWN] and player_y < screen_height - 50:
            player_y += 5

        # Increases obstacle generation speed and movement speed based on game time
        obstacle_speed = 5 + int(dt / 5)  # Every 5 seconds, the speed increases by 1
        generate_obstacle_chance = 50 - int(dt / 10)  # Every 5 seconds, the chance of creating an obstacle increases by 1
        if generate_obstacle_chance > 0 and random.randint(0, generate_obstacle_chance) == 1:  # Generate a new obstacle every once in a while
            generate_obstacle()

        # Obstacle movement
        for i in range(len(obstacles) - 1, -1, -1):
            obstacle = obstacles[i]
            obstacle[0] -= obstacle_speed
            if obstacle[0] < -50:  # Remove off-screen obstructions
                obstacles.pop(i)
            else:
                obstacles[i][0] = obstacle[0]  # Update obstacle location

        # Check for collisions
        collision = False
        for obstacle in obstacles:
            if player_x < obstacle[0] + 50 and player_x + 50 > obstacle[0] and player_y < obstacle[1] + 50 and player_y + 50 > obstacle[1]:
                crashes += 1
                collision = True
                obstacles.remove(obstacle)  # Remove colliding obstacles
                break

        if collision:
            if crashes >= max_crashes:
                game_over = True
            else:
                generate_obstacle()  # Generate new obstacles

        # draw background
        screen.blit(background_image, (0, 0))

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # draw player
        screen.blit(player_image, (player_x, player_y))

    else:
        # game end interface
        screen.fill(white)
        text = font.render("Game over! Press C to start over or Q to exit", True, black)
        text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(text, text_rect)

    # update screen
    pygame.display.flip()

    # Control game refresh speed
    pygame.time.Clock().tick(60)

# Exit game
pygame.quit()

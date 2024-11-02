import pygame
import random
import matplotlib.pyplot as plt
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (169, 169, 169)
yellow = (255, 255, 0)

# Car settings
car_width = 50
car_height = 100
car_speed = 5

# Obstacle settings
obstacle_width = 50
obstacle_height = 100
obstacle_speed = 5  # Define obstacle_speed globally

# Load images
car_image = pygame.Surface((car_width, car_height))
car_image.fill(blue)
obstacle_image = pygame.Surface((obstacle_width, obstacle_height))
obstacle_image.fill(red)

# Fonts
font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 55)

# Functions to display text on screen
def display_message(text, x, y, font, color=white):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

# Function to draw the road and lanes
def draw_road():
    screen.fill(gray)  # Road background
    for i in range(0, screen_height, 40):  # Dashed center line
        pygame.draw.rect(screen, yellow, (screen_width // 2 - 5, i, 10, 20))
    for x in [100, screen_width - 100]:  # Side lane markers
        pygame.draw.rect(screen, white, (x, 0, 5, screen_height))

# Function to draw score history graph
def draw_score_graph(scores):
    plt.figure(figsize=(8, 4))
    plt.plot(np.arange(len(scores)), scores, marker='o', color="blue")
    plt.title("Score History")
    plt.xlabel("Attempts")
    plt.ylabel("Score")
    plt.grid()
    plt.show()

# Game Loop
def game_loop():
    global obstacle_speed  # Declare obstacle_speed as global to modify it

    # Car position
    car_x = screen_width * 0.45
    car_y = screen_height * 0.8

    # Obstacle position
    obstacle_x = random.randint(100, screen_width - 100 - obstacle_width)
    obstacle_y = -600

    # Score and history
    score = 0
    scores = []

    # Game over flag
    game_over = False

    # Main loop
    while True:
        if game_over:
            draw_road()
            display_message("Game Over! Press R to Restart", screen_width // 5, screen_height // 3, big_font, red)
            display_message("Score: " + str(score), screen_width // 3, screen_height // 2, big_font, white)
            draw_score_graph(scores)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return game_loop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Key press handling
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and car_x > 100:
                car_x -= car_speed
            if keys[pygame.K_RIGHT] and car_x < screen_width - car_width - 100:
                car_x += car_speed

            # Move obstacle
            obstacle_y += obstacle_speed

            # Reset obstacle position and update score
            if obstacle_y > screen_height:
                obstacle_y = -obstacle_height
                obstacle_x = random.randint(100, screen_width - 100 - obstacle_width)
                score += 1
                scores.append(score)
                obstacle_speed += 0.5  # Increase speed slightly as score increases

            # Collision detection
            if car_y < obstacle_y + obstacle_height:
                if car_x < obstacle_x + obstacle_width and car_x + car_width > obstacle_x:
                    game_over = True

            # Drawing
            draw_road()
            screen.blit(car_image, (car_x, car_y))
            screen.blit(obstacle_image, (obstacle_x, obstacle_y))
            display_message("Score: " + str(score), 10, 10, font)

            pygame.display.update()

game_loop()

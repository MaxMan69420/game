import pygame
import math
from random import randint
import tkinter as tk

# Initialize pygame
pygame.init()

# Set window size and caption
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Survive")

# Set player starting position
player_x = 350
player_y = 250

# Set player size
player_size = 20

# Set food and poison starting positions
food_x = 50
food_y = 50
poison_x = 600
poison_y = 400

# Set crab starting positions
crab_x = randint(0, size[0]-20)
crab_y = randint(0, size[1]-20)

# Set hunger and health starting values
hunger = 100
health = 100

# Create clock object
clock = pygame.time.Clock()

# Set food count
food_count = 0

# Create an empty list to store crabs
crabs = []

# Create an empty list to store poison
poison = []

# Main game loop
done = False
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= 5
    if keys[pygame.K_s]:
        player_y += 5
    if keys[pygame.K_a]:
        player_x -= 5
    if keys[pygame.K_d]:
        player_x += 5
    if player_x < 0:
        player_x = 0
    if player_x > size[0] - player_size:
        player_x = size[0] - player_size
    if player_y < 0:
        player_y = 0
    if player_y > size[1] - player_size:
        player_y = size[1] - player_size

        
    # Check if hunger is less than 0 and set it to 0
    if hunger < 0:
        hunger = 0
    # Decrement hunger and health every 5 seconds
    hunger -= 0.1
    if hunger <= 0:
        health -= 0.1
    if hunger > 80:
        health += 0.1
    # Cap hunger and health at 100
    if hunger > 100:
        hunger = 100
    if health > 100:
        health = 100
   
    # Check for collision with food
    food_rect = pygame.Rect(food_x, food_y, 20, 20)
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    if player_rect.colliderect(food_rect):
        hunger += 10
        food_count += 1
        food_x = randint(0, size[0]-20)
        food_y = randint(0, size[1]-20)
    # Check if food count reaches 3 and spawn a new crab and poison
    if food_count >= 3:
        new_crab = {"x":randint(0, size[0]-20), "y":randint(0, size[1]-20)}
        crabs.append(new_crab)
        new_poison = {"x":randint(0, size[0]-20), "y":randint(0, size[1]-20)}
        poison.append(new_poison)
        food_count = 0

        # Check for collision with poison
    for i in range(len(poison)):
        poison_rect = pygame.Rect(poison[i]["x"], poison[i]["y"], 20, 20)
        if player_rect.colliderect(poison_rect):
            health -= 5
            del poison[i]
            break

    # Update the position of all the crabs
    for crab in crabs:
        angle = math.atan2(player_y - crab["y"], player_x - crab["x"])
        crab["x"] += math.cos(angle) * 2.5
        crab["y"] += math.sin(angle) * 2.5
        if crab["x"] < 0:
            crab["x"] = 0
        if crab["x"] > size[0] - 20:
            crab["x"] = size[0] - 20
        if crab["y"] < 0:
            crab["y"] = 0
        if crab["y"] > size[1] - 20:
            crab["y"] = size[1] - 20

        
    # Collision detection between player and crabs
    for crab in crabs:
        crab_rect = pygame.Rect(crab["x"], crab["y"], 20, 20)
        if player_rect.colliderect(crab_rect):
            health -= 5

    # Collision detection between crabs
    for i in range(len(crabs)):
        for j in range(i+1,len(crabs)):
            crab_rect_1 = pygame.Rect(crabs[i]["x"], crabs[i]["y"], 20, 20)
            crab_rect_2 = pygame.Rect(crabs[j]["x"], crabs[j]["y"], 20, 20)
            if crab_rect_1.colliderect(crab_rect_2):
                crabs[i]["x"] += 2
                crabs[i]["y"] += 2
                crabs[j]["x"] -= 2
                crabs[j]["y"] -= 2
            
        # Draw crabs on screen
        for crab in crabs:
            pygame.draw.rect(screen, (255, 255, 0), (crab["x"], crab["y"], 20, 20))
            
        # Draw poison on screen
        for poison_obj in poison:
            pygame.draw.rect(screen, (255, 192, 203), (poison_obj["x"], poison_obj["y"], 20, 20))


    # Check for collision with crab
    crab_rect = pygame.Rect(crab_x, crab_y, 20, 20)
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    if player_rect.colliderect(crab_rect):
        health -= 20
        crab_x = randint(0, size[0]-20)
        crab_y = randint(0, size[1]-20)

    # Check for game over
    if health <= 0:
        done = True

    # Draw plain colored player, food, poison, and crab
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, (0, 255, 0), (food_x, food_y, 20, 20))

    # Draw hunger and health bars
    pygame.draw.rect(screen, (255, 0, 0), (50, 450, health, 20))
    pygame.draw.rect(screen, (0, 255, 0), (50, 480, hunger, 20))

    # Update display
    pygame.display.flip()

    # Wait for a while
    clock.tick(30)

#Exit pygame
pygame.quit()

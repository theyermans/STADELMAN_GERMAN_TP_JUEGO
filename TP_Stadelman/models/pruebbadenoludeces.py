import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
main_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Surface Example')

# Create a separate surface for drawing
my_surface = pygame.surface.Surface((100, 50))  # Width and height of the surface

# Fill the surface with a color
my_surface.fill((255, 0, 0))  # Red color

# Get the rect object for the surface
my_surface_rect = my_surface.get_rect()

# Set the position of the surface
my_surface_rect.topleft = (200, 200)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    main_screen.fill((255, 255, 255))  # White background

    # Blit the separate surface onto the main screen at the specified position
    main_screen.blit(my_surface, my_surface_rect.topleft)

    # Update the display
    pygame.display.flip()

pygame.quit()

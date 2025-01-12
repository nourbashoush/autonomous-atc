import pygame

# Initialize Pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([400, 400])

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw the first line from (100, 100) to (100, 200)
    pygame.draw.line(screen, (0, 0, 0), (100, 100), (100, 200), 5)

    # Draw the second line from (100, 200) to (200, 200)
    pygame.draw.line(screen, (0, 0, 0), (100, 200), (200, 200), 5)

    # Draw an arc from (50, 50) to (150, 200)
    pygame.draw.arc(screen, (0, 0, 0), (100, 100, 50, 50), 3.14, 4.71, 5)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

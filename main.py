import pygame

# initializes the pygame library
pygame.init()

# creates the window and dimensions for the game
screen = pygame.display.set_mode((850, 850))
# sets the window caption at the top
pygame.display.set_caption("Rogue Survival")


game = True
while game:
    # the core game loop
    clock = 60
    # sets the fps to 60
    pygame.time.delay(5)
    # adds a very small delay to make it feel more like a game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if the x in the top right corner of game is clicked, the program will close.
            game = False

    pygame.display.update()

pygame.quit()

# Simple pygame program

# Import and initialize the pygame library
import pygame
import UI as ui


def handle(but):
    if but != None:
        but.setText("Hola")

def main():
    
    pygame.init()
    # Define constants for the screen width and height
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    fps = 60
    fpsClock = pygame.time.Clock()

    matSize = (6,7)
    recSize = (700,700)
    pos = (50,50)

    board = ui.Board(matSize, pos, recSize, handle)
    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # Run until the user asks to quit
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()

        # Fill the background with white
        screen.fill((255, 255, 255))
        board.posX = mouse[0]
        board.posY = mouse[1]
        board.update(screen)


        # Flip the display
        pygame.display.flip()
        fpsClock.tick(fps)

    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()



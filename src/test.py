# Simple pygame program

# Import and initialize the pygame library
import pygame
import UI as ui
import cProfile
import numpy as np

selectedNum : str = '0'


def selectNum(but):
    if but != None:
        global selectedNum
        selectedNum = but.buttonText

def handle(but):
    if but != None:
        but.setText(selectedNum)


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func

def main():
    pygame.init()
    pygame.display.set_caption('Connect')
    # Define constants for the screen width and height
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800

    matSize = (10,7)
    recSize = (700,700)
    pos = (50,50)
    
    numbers:list = ["0","1","2","3","4","5","6","7","8","9","-"]
    nums = ui.Board((1,11), (850,75), (60,650), numbers,selectNum)
    board = ui.Board(matSize, pos, recSize,[], handle)
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
        
        board.update(screen)
        nums.update(screen)


        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()



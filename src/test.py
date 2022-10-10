# Simple pygame program

# Import and initialize the pygame library
import pygame
import UI as ui
import numpy as np

selectedNum : str = '0'

def selectNum(but):
    if but != None:
        global selectedNum
        selectedNum = but.buttonText

def handle(but):
    if but != None:
        but.setText(selectedNum)

def cargarMat(path):
    try:
        with open(path) as f:
            lines = f.readlines()
        primera= lines[0]
        primera = primera.split('\n')[0]
        primera_nums = primera.split()
        x = int(primera_nums[0])
        y = int(primera_nums[2])
    except:
        x=7
        y=7
        mat = np.zeros((x,y))
        mat.fill(-np.inf)
        return mat
    mat = np.zeros((x,y))
    mat.fill(-np.inf)
    for line in lines[1:-1]:
        vals = line.split()
        y = int(vals[0])
        x = int(vals[2])
        num = int(vals[4])
        mat[x-1][y-1] = num
    return mat

def resetGame(but):
    global board
    board.reset()
    print("Reset")

def loadGame(but):
    global board
    global path
    print(path)
    mat = cargarMat(path)
    matSize = mat.shape
    recSize = (700,700)
    pos = (50,50)
    board = ui.Board(matSize, pos, recSize,mat, False, handle)
    path = ''

def resolverGame(but):
    print("resolver")

def main():
    pygame.init()
    pygame.display.set_caption('Connect')
    # Define constants for the screen width and height
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    mat = cargarMat("Ejemplo.txt")
    matSize = mat.shape
    recSize = (700,700)
    pos = (50,50)
    
    numbers = np.zeros((1,11))
    for i in range(10):
        numbers[0][i] = i
    numbers[0][10] = -np.inf

    nums = ui.Board((1,11), (850,75), (60,650), numbers,True, selectNum)
    global board 
    board = ui.Board(matSize, pos, recSize,mat, False, handle)
    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    buttons = []

    b = ui.Button("load", 1000, 150, 0,0, 100, 30,20,"Load Game", loadGame, False)
    buttons.append(b)
    b = ui.Button("reset", 1000, 200, 0,0, 100, 30,20,"Reset Game", resetGame, False)
    buttons.append(b)
    b = ui.Button("resolver", 1000, 250, 0,0, 100, 30,20,"Solution", resolverGame, False)
    buttons.append(b)

    #TxtBox attributes
    input_box = pygame.Rect(975, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_txtBox = color_inactive
    active = False
    global path
    path = ''
    font = pygame.font.Font(None, 32)
    
    # Run until the user asks to quit
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #99d17# If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color_txtBox = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        path = path[:-1]
                    else:
                        path += event.unicode

        # Fill the background with white
        screen.fill((255, 255, 255))

        #Txt Box ----------------------------------------
        txt_surface = font.render(path, True, color_txtBox)
       
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color_txtBox, input_box, 2)
        #Txt Box ----------------------------------------
        
        board.update(screen)
        nums.update(screen)
        for but in buttons:
            but.process(screen)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()



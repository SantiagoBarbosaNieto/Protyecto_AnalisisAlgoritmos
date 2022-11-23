# Simple pygame program

# Import and initialize the pygame library
import pygame
import UI as ui
import numpy as np
import pathlib

selectedNum : str = '0'
mat : np.ndarray

matPosibilidades: dict = {}

posibilidades = set()
originales = set()

def selectNum(but):
    if but != None:
        global selectedNum
        selectedNum = but.buttonText

def handle(but):
    if but != None:
        but.setText(selectedNum)

def cargarMat(path):
    global matPosibilidades
    global posibilidades
    global originales
    matPosibilidades = {}
    posibilidades = set()
    originales = set()
    prePath = pathlib.Path(__file__).parent.resolve()
    global mat
    try:
        with open(str(prePath)+"\\"+path) as f:
            lines = f.readlines()
        primera= lines[0]
        primera = primera.split('\n')[0]
        primera_nums = primera.split()
        x = int(primera_nums[0])
        y = int(primera_nums[2])
    except:
        print("No pudo ser leido el archivo.. Cargando matriz default")
        x=7
        y=7
        mat = np.zeros((x,y))
        mat.fill(-np.inf)
        return mat
    mat = np.zeros((x,y))
    mat.fill(-np.inf)
    for i in range(1,len(lines)):
        try:
            line = lines[i]
            vals = line.split()
            y = int(vals[0])
            x = int(vals[2])
            num = int(vals[4])
            mat[x-1][y-1] = num #En ejemplo.txt los indicies deben ser desde 1, no desde 0
            posibilidades.add(num)
            originales.add((x-1, y-1))
        except:
            continue
    print("Cargado")


def resetGame(but):
    global board
    global matPosibilidades
    global posibilidades
    global originales
    global mat
    board.reset()
    matPosibilidades = {}
    posibilidades = set()
    originales = set()
    mat = np.zeros(mat.shape)
    mat.fill(-np.inf)
    print("Reset")

def loadGame(but):
    global board
    global path
    global mat
    print(path)
    cargarMat(path)
    matSize = mat.shape
    recSize = (700,700)
    pos = (50,50)
    board = ui.Board(matSize, pos, recSize,mat, False, handle)
    
def getVecinos(xPos, yPos):
    vecinos = set()
    for i in range(-1,2):
        for j in range(-1,2):
            if not (i == 0 and j == 0) and not(abs(i) == abs(j)):
                global mat
                shape = mat.shape
                if(xPos+i >= 0 and yPos+j >= 0 and xPos+i < shape[0] and yPos+j < shape[1]):
                    vecinos.add((xPos+i,yPos+j))
    return vecinos

def generarMatBot():
    global mat
    global matPosibilidades
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if (i,j) in originales:
                matPosibilidades[(i,j)] = [int(mat[i][j])]
            else:
                matPosibilidades[(i,j)] = list(posibilidades)

def getSalidas(ij):  #Ambos parametros son tuplas
    global matPosibilidades
    vecinos = getVecinos(ij[0], ij[1])
    salidas = set()
    for v in vecinos:
        vPosi = matPosibilidades.get(v)
        ijPosi = matPosibilidades.get(ij)
        if len(vPosi) > 1:
            for p in ijPosi: 
                if p in vPosi:
                    salidas.add(v)
    return salidas

def getFijos(ij):
    global matPosibilidades
    vecinos = getVecinos(ij[0], ij[1])
    fijos = set()
    for v in vecinos:
        vPosi = matPosibilidades.get(v)
        if len(vPosi) == 1:
            fijos.add(v)
    return fijos

def gameFinished():
    finished = True
    for key in matPosibilidades.keys():
        if len(matPosibilidades.get(key)) != 1:
            finished = False
            break
    return finished

def updateMat():
    for key in matPosibilidades.keys():
        i,j = key
        if len(matPosibilidades.get(key)) == 1:
            mat[i][j] = matPosibilidades.get(key)[0]
    global board
    board.generateButtons(mat)

def resolverGame(but):
    generarMatBot()
    global mat
    global matPosibilidades
    
    iter = 0
    while not gameFinished():
        iter+=1
        print("Iteration: ", iter)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                vecinos = getVecinos(i,j)
                salidas = getSalidas((i,j))
                fijos = getFijos((i,j))
                ijPosi = matPosibilidades.get((i,j))
                        
                #Aqui ya sabemso cuantas salidas tiene
                
                if len(ijPosi) == 1: #si es fijo
                    if (i,j) in originales: #Si es original
                    
                        camino = False
                        for v in vecinos:
                            vPosi = matPosibilidades.get(v)
                            if len(vPosi) == 1 and vPosi[0] == ijPosi[0]:
                                camino = True
                                break

                        if camino:   #Si ya tiene su camino (tiene 1 vecino fijo con su mismo #) Se verifica que las salidas al rededor ya no tengan el numero de esta casilla como posibilidad
                            for s in salidas:
                                setPS = set(matPosibilidades.get(s))
                                if ijPosi[0] in setPS:
                                    setPS.remove(ijPosi[0])
                                matPosibilidades[s] = list(setPS)
                        else: #Si no tiene su camino:
                            if len(salidas) == 1: #Si tiene 1 salida:
                                sal = list(salidas)[0]
                                #esa salida se vuelve el mismo #
                                matPosibilidades[sal] = ijPosi.copy()
                    else: #No es original
                        camino = False
                        count = 0
                        for v in vecinos:
                            vPosi = matPosibilidades.get(v)
                            if len(vPosi) == 1 and vPosi[0] == ijPosi[0]:
                                count += 1
                        if count >= 2:
                            camino = True
                        
                        if camino: #Si ya tiene su camnio (tiene 2 vecinos fijos con su mismo #)
                            for s in salidas:
                                setPS = set(matPosibilidades.get(s))
                                if ijPosi[0] in setPS:
                                    setPS.remove(ijPosi[0])
                                matPosibilidades[s] = list(setPS)
                        else: #si no tiene camino
                            if len(salidas) == 1: #Si tiene 1 salida:
                                sal = list(salidas)[0]
                                #esa salida se vuelve el mismo #
                                matPosibilidades[sal] = ijPosi.copy()
                else: #No es fijo
                    if len(salidas) == 0: # si no tiene salidas
                        if len(fijos) == 2: # si tiene 2 fijos alrededor
                            matPosibilidades[(i,j)] = matPosibilidades.get(list(fijos)[0])#La casilla se vuelve el mismo numero que sus dos fijos
                        elif len(fijos) == 3:
                            if matPosibilidades.get(list(fijos)[0])[0] == matPosibilidades.get(list(fijos)[1])[0] or matPosibilidades.get(list(fijos)[0])[0] == matPosibilidades.get(list(fijos)[2])[0]: #Si el primer fijo es igual al segundo o tercer fijo
                                matPosibilidades[(i,j)] = matPosibilidades.get(list(fijos)[0])
                            else: # El segundo fijo y el tercer fijo son iguales, se puede usar cualquiera de esos dos
                                matPosibilidades[(i,j)] = matPosibilidades.get(list(fijos)[1])

                    elif len(salidas) == 1:
                        setPos = set(ijPosi)
                        setFijos = set()
                        for f in fijos:
                            setFijos.add(list(matPosibilidades.get(f))[0])
                        setFinal = setPos.intersection(setFijos)
                        matPosibilidades[(i,j)] = list(setFinal)
                    elif len(salidas) == 2:
                        setFinal = set()
                        setSal1 = set(matPosibilidades.get(list(salidas)[0]))
                        setSal2 = set(matPosibilidades.get(list(salidas)[1]))
                        setFinal = setSal1.intersection(setSal2)
                        matPosibilidades[(i,j)] = list(setFinal)
        print(matPosibilidades)
        if iter == 200:
            print("Ya realizo demasidas iteraciones, debe estar atastcado o es imposible de resolver... saliendo")
            break
    #actualice mat con matPosibilidades que ya estan fijas
    updateMat()

                
def main():
    pygame.init()
    pygame.display.set_caption('Arukone')
    # Define constants for the screen width and height
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    global path
    path = 'Ejemplo3.txt'
    global mat
    cargarMat(path)
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



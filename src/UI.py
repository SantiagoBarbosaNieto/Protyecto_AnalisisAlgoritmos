
import pygame
import cProfile

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

class Button():
    def __init__(self, id, boardX, boardY, xOffset, yOffset, width, height, fontsize = 15,buttonText='Button', onclickFunction=None, onePress=False):
        self.id = id
        self.x = boardX
        self.y = boardY
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.width = width
        self.height = height
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonText = buttonText
        self.onclickFunction = onclickFunction
        self.fontsize = fontsize

        self.fillColors = {
            'normal':  '#ffffff',
            'hover':   '#90f598',
            'pressed': '#333333'
        }
    
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x + self.xOffset, self.y + self.yOffset, self.width, self.height)

        self.buttonSurf =  pygame.font.SysFont('Arial', self.fontsize).render(buttonText, True, (20, 20, 20))

    def process(self, screen):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction(self)
                elif not self.alreadyPressed:
                    self.onclickFunction(self)
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
                
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
    
    def setText(self, text):
        self.buttonText = text
        self.buttonSurf =  pygame.font.SysFont('Arial', self.fontsize).render(self.buttonText, True, (20, 20, 20))
    
    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.buttonRect = pygame.Rect(self.x+self.xOffset, self.y+self.yOffset, self.width, self.height)
    
    def select(self):
        self.fillColors['normal'] = '#0fe21f'

    def unselect(self):
        self.fillColors['normal'] = '#ffffff'


class Board:

    def __init__(self, matSize: tuple, position : tuple, areaSize: tuple, nums:list, handleButs=None):
        self.cols = matSize[0]
        self.rows = matSize[1]
        self.posX = position[0]
        self.posY = position[1]
        self.width = areaSize[0]
        self.height = areaSize[1]
        self.backgroundRect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.buttons = []
        self.butSizeX = (self.width-(self.cols+1))/self.cols
        self.butSizeY = (self.height-(self.rows+1))/self.rows
        self.handleButs = handleButs
        self.generateButtons(nums)
        self.selectedBut = self.buttons[0]

    def generateButtons(self, nums: list):
        for i in range(self.cols):
            for j in range( self.rows):
                if len(nums) > 0:
                    txt = nums[i+j*self.cols]
                else:
                    txt = '-'
                x = 1+i*self.butSizeX+i
                y = 1+ j*self.butSizeY+j
                b = Button(i,self.posX, self.posY, x,y, self.butSizeX, self.butSizeY, 20, str(txt), self.handleButtons)
                self.buttons.append(b)
    
    def handleButtons(self, but):
        self.selectedBut.unselect()
        but.select()
        self.selectedBut = but
        self.handleButs(but)
    
    def updatePos(self, pos):
        self.posX = pos[0]
        self.posY = pos[1]
        self.backgroundRect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        for b in self.buttons:
            b.setPos(pos)

    def update(self, screen):
        pygame.draw.rect(screen, (20,20,20), self.backgroundRect)
        for but in self.buttons:
            but.process(screen)
        
    



from operator import truediv
import pygame
import numpy as np

class Button():
    def __init__(self, id, boardX, boardY, xOffset, yOffset, width, height, fontsize = 15,buttonText='-', onclickFunction=None, selectable = False):
        self.id = id
        self.x = boardX
        self.y = boardY
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.width = width
        self.height = height
        self.onePress = False
        self.alreadyPressed = False
        self.buttonText = buttonText
        self.onclickFunction = onclickFunction
        self.fontsize = fontsize
        self.selectable = selectable
        self.numColors = {
            '-': '#ffffff',
            '0': '#ff0d00',
            '1': '#ff8000',
            '2': '#fbff00',
            '3': '#99d17b',
            '4': '#00ffcc',
            '5': '#008cff',
            '6': '#8800ff',
            '7': '#ff00e6',
            '8': '#734719',
            '9': '#66968a',
        }
        try:
            color = self.numColors[buttonText]
        except:
            color = "#ffffff"
        if selectable:
            color = "#ffffff"
        self.fillColors = {
            'normal':  color,
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
        if(not self.selectable):
            self.fillColors['normal'] = self.numColors[text]

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.buttonRect = pygame.Rect(self.x+self.xOffset, self.y+self.yOffset, self.width, self.height)
    
    def select(self):
        if self.selectable:
            self.fillColors['normal'] = '#0fe21f'

    def unselect(self):
        if self.selectable:
            self.fillColors['normal'] = '#ffffff'


class Board:

    def __init__(self, matSize: tuple, position : tuple, areaSize: tuple, nums:np.mat, selectable, handleButs=None):
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
        self.selectable = selectable
        self.generateButtons(nums)
        if(self.selectable):
            self.buttons[0].select()
            self.selectedBut = self.buttons[0]
   

    def generateButtons(self, nums: np.mat):
        self.buttons.clear()
        for i in range(self.cols):
            for j in range( self.rows):
                if nums[i][j] != -np.inf:
                    txt = int(nums[i][j])
                else:
                    txt = '-'
                x = 1+i*self.butSizeX+i
                y = 1+ j*self.butSizeY+j
                b = Button(i,self.posX, self.posY, x,y, self.butSizeX, self.butSizeY, 20, str(txt), self.handleButtons, self.selectable)
                self.buttons.append(b)
    
    def handleButtons(self, but):
        if self.selectable:
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

    def reset(self):
        mat = np.zeros((self.cols,self.rows))
        mat.fill(-np.inf)
        self.generateButtons(mat)
        
    


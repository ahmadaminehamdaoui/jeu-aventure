import pygame, data_handler
config = data_handler.load_config()

class UI_window:
    def __init__(self, name, position, dimensions, padding):
        self.name = name
        self.position = position
        self.dimensions = dimensions
        self.padding = padding
        self.content = []

    def write(self, txt):
        self.content.insert(0, txt)

# J'ai réutilisé cette classe de mon ancien programme 'pypaint' trouvable sur mon github
class New_Button: 
    def __init__(self, position, dimension, color, action, txt='', image=None):
        self.position = position
        self.dimension = dimension
        self.color = color
        self.txt = txt
        self.action = action
        self.image = image
    
    def draw(self, surface): 
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.dimension[0], self.dimension[1]))

        if self.image != None:
            surface.blit(self.image, (self.position[0] + (self.dimension[0]/2 - self.image.get_width()/2), self.position[1] + (self.dimension[1]/2 - self.image.get_height()/2)))

        if self.txt != '':
            font = pygame.font.SysFont('Consolas', config["text-size"])
            txt = font.render(self.txt, 1, (0,0,0))
            surface.blit(txt, (self.position[0] + (self.dimension[0]/2 - txt.get_width()/2), self.position[1] + (self.dimension[1]/2 - txt.get_height()/2) + 1))

    def is_over(self, pos):
        if pos[0] > self.position[0] and pos[0] < self.position[0] + self.dimension[0]:
            if pos[1] > self.position[1] and pos[1] < self.position[1] + self.dimension[1]:
                return True
        return False

"""
Programme réalisé par HAMDAOUI Ahmad-Amine, 1G7.

A AJOUTER : DYNAMISME DES FENËTRES AVEC LA RÉSOLUTION, SUPPORT D'ÉTAGES, SONS CUSTOM, OPTIONS AVANCÉES (couleurs interface, résolution image, police & taille, etc...)
"""


import pygame, sys # on importe le module system afin de pouvoir fermer la fenêtre sans faire crash le programme
import data_handler
from classes import *
rooms = data_handler.load()

# Initalisation de pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Jeu d'aventure")

# Fonctions 
def stop():
    pygame.quit()
    sys.exit()

def info():
    global win_console, place
    win_console.write(place.description)

def move(direction):
    global place, position, win_console, win_inventory
    counter = 0
    if direction == 'z':
        for element in place.can_go_to:
            for room in rooms:
                if room.name == element and room.position == [position[0], position[1]+1]:    
                    if len(room.conditions) > 0:
                        for i in range(len(room.conditions[0])):
                            if room.conditions[0][i] in win_inventory.content: counter += 1
                        if counter==len(room.conditions[0]):
                            position[1] += 1
                            win_console.write(room.description)
                            counter = 0
                            try: win_console.write(str(room.conditions[2]).strip("[']"))
                            except: pass
                        else:
                            try: win_console.write(str(room.conditions[1]).strip("[']"))
                            except: pass
                    else: 
                        position[1] += 1
                        win_console.write(room.description)
    elif direction == 's':
        for element in place.can_go_to:
            for room in rooms:
                if room.name==element and room.position==[position[0], position[1]-1]: 
                    if len(room.conditions) > 0:
                        for i in range(len(room.conditions[0])):
                            if room.conditions[0][i] in win_inventory.content: counter += 1
                        if counter==len(room.conditions[0]):                       
                            position[1] -= 1
                            win_console.write(room.description)
                            counter = 0
                            try: win_console.write(str(room.conditions[2]).strip("[']"))
                            except: pass
                        else:
                            try: win_console.write(str(room.conditions[1]).strip("[']"))
                            except: pass
                    else: 
                        position[1] -= 1
                        win_console.write(room.description)
    elif direction == 'q':
        for element in place.can_go_to:
            for room in rooms:
                if room.name == element and room.position == [position[0]-1, position[1]]:
                    if len(room.conditions) > 0:
                        for i in range(len(room.conditions[0])):
                            if room.conditions[0][i] in win_inventory.content: counter += 1                          
                        if counter==len(room.conditions[0]):
                            position[0] -= 1
                            win_console.write(room.description)
                            counter = 0
                            try: win_console.write(str(room.conditions[2]).strip("[']"))
                            except: pass
                        else:
                            try: win_console.write(str(room.conditions[1]).strip("[']"))
                            except: pass
                            
                    else: 
                        position[0] -= 1
                        win_console.write(room.description)
    elif direction == 'd':
        for element in place.can_go_to:
            for room in rooms:
                if room.name == element and room.position == [position[0]+1, position[1]]:
                    if len(room.conditions) > 0:
                        for i in range(len(room.conditions[0])):
                            if room.conditions[0][i] in win_inventory.content: 
                                counter += 1
                        if counter==len(room.conditions[0]):
                            position[0] += 1
                            win_console.write(room.description)
                            counter = 0
                            try: win_console.write(str(room.conditions[2]).strip("[\"']"))
                            except: pass
                        else:
                            try: win_console.write(str(room.conditions[1]).strip("[\"']"))
                            except: pass
                    else: 
                        position[0] += 1
                        win_console.write(room.description)

# Variables initiales
font = pygame.font.SysFont('Consolas', 20)

WIDTH, HEIGHT = pygame.display.get_surface().get_size()
DEFAULT_DIMENSIONS = (940,540)
CONSOLE_SECTION = (WIDTH/2-DEFAULT_DIMENSIONS[0]/2, HEIGHT)

position = [0,0]
place = None
is_clicking = False

# fenêtres & boutons
ui_windows = []
win_console = UI_window('console', (0, 0), CONSOLE_SECTION, 20)
win_control = UI_window('contrôle', (CONSOLE_SECTION[0], DEFAULT_DIMENSIONS[1]), (DEFAULT_DIMENSIONS[0]/2, HEIGHT-DEFAULT_DIMENSIONS[1]), 20)
win_minimap = UI_window('minimap', (WIDTH/2, DEFAULT_DIMENSIONS[1]), (DEFAULT_DIMENSIONS[0]/2, HEIGHT-DEFAULT_DIMENSIONS[1]), 20)
win_inventory = UI_window('inventaire', (WIDTH/2+DEFAULT_DIMENSIONS[0]/2, 0), (CONSOLE_SECTION[0], HEIGHT), 20)
ui_windows = [win_console, win_inventory, win_control, win_minimap]

element_center = (win_control.position[0]+win_control.dimensions[0]/2, win_control.position[1]+win_control.dimensions[1]/2)
buttons = []
buttons.append(New_Button((element_center[0]-140, element_center[1]-60), (80,40), (255,255,255), lambda:move('q'), txt='Gauche'))
buttons.append(New_Button((element_center[0]+40, element_center[1]-60), (80,40), (255,255,255), lambda:move('d'), txt='Droite'))
buttons.append(New_Button((element_center[0]-50, element_center[1]-60), (80,40), (255,255,255), lambda:move('s'), txt='Bas'))
buttons.append(New_Button((element_center[0]-50, element_center[1]-110), (80,40), (255,255,255), lambda:move('z'), txt='Haut'))
buttons.append(New_Button((element_center[0]-140, element_center[1]+40), (260,40), (255,255,255), lambda:info(), txt='Décrire'))
buttons.append(New_Button((element_center[0]-140, element_center[1]+90), (260,40), (255,255,255), lambda:stop(), txt='Quitter'))

# Chargement des images & des positions
for room in rooms:
    # images
    room.image = pygame.transform.scale(pygame.image.load(room.image), DEFAULT_DIMENSIONS)
    for element in room.objects:
        element[1] = pygame.image.load(element[1])
    # positions
    for obj in room.objects:
        obj[2] = [obj[2][0]+WIDTH/2-DEFAULT_DIMENSIONS[0]/2, obj[2][1]]

# --------- Logique de jeu ---------#
while True:
    cursor_pos = pygame.mouse.get_pos() # on obtient la position de la souris

    for room in rooms:
        if room.position == position:
            place = room

    # --------- Actions ---------#
    for event in pygame.event.get():
        # Gestion de la fermeture
        if event.type == pygame.QUIT:
            stop()        
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_ESCAPE:
                stop()
            # Touches
            elif event.key == pygame.K_q:
                move('q')
            elif event.key == pygame.K_d:
                move('d')
            elif event.key == pygame.K_z:
                move('z')
            elif event.key == pygame.K_s:
                move('s')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_clicking = True
            for i in buttons: # détection du clic de la souris
                if i.is_over((cursor_pos[0], cursor_pos[1])):
                    i.action()
                    i.color = (170,170,170)      
            for obj in place.objects: # détection du clic d'un objet
                obj_width, obj_height = (obj[1].get_width(), obj[1].get_height())
                if cursor_pos[0] > obj[2][0] and cursor_pos[0] < obj[2][0]+obj_width and cursor_pos[1] > obj[2][1] and cursor_pos[1] < obj[2][1]+obj_height:
                    win_inventory.write(obj[0])
                    place.objects.remove(obj)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            is_clicking = False
    # --------- Affichage ---------#
    screen.fill((0,0,0)) # on efface la fenêtre

    # JEU
    screen.blit(place.image, (WIDTH/2-DEFAULT_DIMENSIONS[0]/2, 0)) # affichage de la pièce
    for element in place.objects: # affichage des objets
        screen.blit(element[1], (element[2][0], element[2][1]))
    
    # UI
    for i in range(len(ui_windows)): # affichage des fenêtres (bordures des fenêtres)
        element = ui_windows[i]
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(element.position[0], element.position[1], element.dimensions[0], element.dimensions[1]))
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(element.position[0], element.position[1], element.dimensions[0], element.dimensions[1]),  5)
        
        for i in range(len(element.content)): # affichage du texte des fenêtres en contenant
            element_ = element.content[i] 
            textsurface = font.render(element_, False, (255,255,255))
            screen.blit(textsurface, (element.position[0]+element.padding, element.position[1]+30+i*30+element.padding))
        
        textsurface = font.render(f'--- {element.name.upper()} ---', False, (255,255,255)) # affichage du titre de la fenêtre
        screen.blit(textsurface, (element.position[0]+element.padding, element.position[1]+element.padding))

    # affichage de la minimap
    minimap_center = (win_minimap.position[0]+win_minimap.dimensions[0]/2, win_minimap.position[1]+win_minimap.dimensions[1]/2)
    for room in rooms:
        room_position = (minimap_center[0]+20*room.position[0], minimap_center[1]+20*-room.position[1])
        for element in room.can_go_to:
            for room_ in rooms:
                    if room_.name == element:         
                        if room_.position == [room.position[0]+1, room.position[1]]:
                            pygame.draw.rect(screen, (100,100,100), pygame.Rect(room_position[0]+5, room_position[1]+5, 20, 1))
                        elif room_.position == [room.position[0]-1, room.position[1]]:                   
                            pygame.draw.rect(screen, (100,100,100), pygame.Rect(room_position[0]-15, room_position[1]+5, 20, 1))
                        elif room_.position == [room.position[0], room.position[1]+1]:                   
                            pygame.draw.rect(screen, (100,100,100), pygame.Rect(room_position[0]+5, room_position[1]+5, 1, -20))
                        elif room_.position == [room.position[0], room.position[1]-1]:                   
                            pygame.draw.rect(screen, (100,100,100), pygame.Rect(room_position[0]+5, room_position[1]+5, 1, 20)) 
    for room in rooms:
        room_position = (minimap_center[0]+20*room.position[0], minimap_center[1]+20*-room.position[1])
        room_color = (255,255,255) if room == place else (100,100,100)
        pygame.draw.rect(screen, room_color, pygame.Rect(room_position[0], room_position[1], 10, 10))
    
    for i in buttons: # on change la couleur des boutons s'ils sont survolés par la souris
        if not is_clicking:
            if i.is_over((cursor_pos[0], cursor_pos[1])):
                    i.color = (220,220,220)
            else:
                    i.color = (255,255,255)

    for i in range(len(buttons)): # affichage des boutons
        buttons[i].draw(screen)

    pygame.display.flip() # actualisation


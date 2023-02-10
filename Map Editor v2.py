# Setup --------------------------------------------------------------------- #
# Import pygame --------------------------------------------------- #
import pygame

# Import other base libraries ------------------------------------- #
import os
import random

# Import tkinter -------------------------------------------------- #
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Import time ----------------------------------------------------- #
import time

# Import custom --------------------------------------------------- #
import Data.Scripts.testing as testing
import Data.Scripts.map as map
import Data.Scripts.image_handling as image_handling
import Data.Scripts.font as font
import Data.Scripts.json_handler as json_handler
import Data.Scripts.entities.entities as entities
import Data.Scripts.entities.particles as particles

from Data.Keybinds import KEYBINDS

# Initialise pygame ----------------------------------------------- #
pygame.init()

# Clock & FPS ----------------------------------------------------- #
clock = pygame.time.Clock()
FPS = 60

# Setup window ---------------------------------------------------- #
screen = pygame.display.set_mode((800, 500), pygame.RESIZABLE)
pygame.display.set_caption("Map Editor")
fullscreen = False

# Font ------------------------------------------------------------ #
large_font = font.Font("Data/Images/Fontsheets/large_font.png", (255, 255, 255), 6, 1)
small_font = font.Font("Data/Images/Fontsheets/small_font.png", (255, 255, 255), 3, 1)

# Controls & file handling ---------------------------------------- #
from Data.Keybinds import KEYBINDS

KEYBINDS["Place tile"] = pygame.mouse.get_pressed()[0]
KEYBINDS["Get hover"] = pygame.mouse.get_pressed()[1]
KEYBINDS["Delete tile"] = pygame.mouse.get_pressed()[2]

CTRL = False
SHIFT = False

filename = "CTRL + o to open a map, CTRL + n to open a new file"

# Map ------------------------------------------------------------- #
X_OFFSET = 170
Y_OFFSET = 70
game_map = map.Map()
save_name = None

# Tilesets -------------------------------------------------------- #
# tile_orders = json_handler.load("Data/Configs/tile_orders.json")
tileset_colours = {"colour 1":(255, 0, 255, 255), "colour 2":(0, 255, 255, 255)}
tilesets = {}
for file in os.listdir("Data/Images/Tilesets"):
    if file.endswith(".png"):
        path = file.split(".")[0]
        tile_order = json_handler.load("Data/Images/Tilesets/" + path + ".json")
        # tilesets[path] = map.Tileset("Data/Images/Tilesets/" + file, tileset_colours, tile_orders[path])
        tilesets[path] = map.Tileset("Data/Images/Tilesets/" + file, tileset_colours, tile_order)

selected_tileset = None
selected_tile = None

# VFX ------------------------------------------------------------- #
vfx = {
    "Square_effects": [],
    "Circle_effects": {
        "Circle_particles": [],
        "Pixel_particles": []
    }
}

# Other ----------------------------------------------------------- #
TILESIZE = 32
LAYER = 0
SPACE = "Tile_space"
GRAVITY = 0.3

# Custom editing -------------------------------------------------- #
editing_surf = pygame.Surface((200, 100))
editing = False
typing_chars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ","_","0","1","2","3","4","5","6","7","8","9","."]
typing = ""
hover_typing = "None"

# Main Game Loop ------------------------------------------------------------ #
running = True
while running:
    # Setup frame ------------------------------------------------- #
    events = pygame.event.get()
    mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
    
    KEYBINDS["Place tile"] = pygame.mouse.get_pressed()[0]
    KEYBINDS["Get hover"] = pygame.mouse.get_pressed()[1]
    KEYBINDS["Delete tile"] = pygame.mouse.get_pressed()[2]
    
    screen.fill((0, 0, 0))

    # VFX --------------------------------------------------------- #
    # Square effects ------------------------------------ #
    for i, square in sorted(enumerate(vfx["Square_effects"]), reverse=True):
        if square.width < 1:
            pygame.draw.rect(screen, square.colour, square.rect)
        else:
            for i in range(int(square.width)):
                pygame.draw.rect(screen, square.colour, pygame.Rect(square.rect.x - i, square.rect.y - i, square.rect.width + i * 2, square.rect.height + i * 2), 1)

        square.update()
        if square.width < 0.3:
            vfx["Square_effects"].pop(i)
        
    # Circle effects ------------------------------------ #
    for i, circle in sorted(enumerate(vfx["Circle_effects"]["Circle_particles"]), reverse=True):
        pygame.draw.circle(screen, circle.colour, circle.rect.center, circle.size)
        circle.update()
        if circle.size < 0.3:
            vfx["Circle_effects"]["Circle_particles"].pop(i)
    
    # Pixel effects ------------------------------------- #
    for i, pixel in sorted(enumerate(vfx["Circle_effects"]["Pixel_particles"]), reverse=True):
        pygame.draw.rect(screen, pixel.colour, pixel.rect)

        pixel.update()
        if pixel.size < 0.3:
            vfx["Circle_effects"]["Pixel_particles"].pop(i)

    # Render Map -------------------------------------------------- #
    # Tile space ---------------------------------------- #
    if game_map.map_data != {}:
        for tile_layer in game_map.map_data["Tile_space"]:
            for pos, tile_data in game_map.map_data["Tile_space"][tile_layer].items():
                positions = [(int(pos.split(",")[0]) * TILESIZE) + X_OFFSET, (int(pos.split(",")[1]) * TILESIZE) + Y_OFFSET]
                screen.blit(tilesets[tile_data["Tileset"]].images[tile_data["Tile"]], positions)
        
    # World space --------------------------------------- #            
        for tile_layer in game_map.map_data["World_space"]:
            for pos, tile_data in game_map.map_data["World_space"][tile_layer].items():
                pos = pos.split(",")
                screen.blit(tilesets[tile_data["Tileset"]].images[tile_data["Tile"]], [int(pos[0]) + X_OFFSET, int(pos[1]) + Y_OFFSET])

    # UI ---------------------------------------------------------- #
    pygame.draw.rect(screen, (10, 15, 20), (0, 0, screen.get_width(), 50))
    pygame.draw.rect(screen, (10, 15, 20), (0, 0, 150, screen.get_height()))
    pygame.draw.rect(screen, (10, 0, 15), (0, screen.get_height() / 2, 150, screen.get_height() / 2))

    large_font.render(screen, f"{filename}", [screen.get_width() / 2 - large_font.get_width(f"{filename}") / 2, (50 - 32) / 2])
    
    small_font.render(screen, f"Layer: {LAYER}", [160, 60])
    small_font.render(screen, f"{SPACE}", [160, 80])
    small_font.render(screen, f"{mouse_pos[0]}, {mouse_pos[1]}", [160, 100])
    
    small_font.render(screen, f"{hover_typing}", [160, 120])

    if filename != "CTRL + o to open a map, CTRL + n to open a new file" or screen.get_width() > 1120:
        small_font.render(screen, f"{time.ctime()}", [screen.get_width() - small_font.get_width(f"{time.ctime()}") - 10, (50 - 16) / 2])
        small_font.render(screen, "Tiles", [75 - small_font.get_width("Tiles") / 2, (50 - 16) / 2])
    
    # Tile types ---------------------------------------- #
    y = 0
    for tileset, value in tilesets.items():
        if ((25 < mouse_pos[0] < 125) and ((50 - 16) / 2 + (25 * (y + 1)) + 17 < mouse_pos[1] < (50 - 16) / 2 + (25 * (y + 1)) + 42)) or selected_tileset == tileset:
            small_font.render(screen, f"{tileset}", [75 - small_font.get_width(f"{tileset}") / 2 + 25, (50 - 16) / 2 + (25 * (y + 1)) + 25])
        else:
            small_font.render(screen, f"{tileset}", [75 - small_font.get_width(f"{tileset}") / 2, (50 - 16) / 2 + (25 * (y + 1)) + 25])

        if selected_tileset == tileset:
            x = 10
            y2 = 10 + (screen.get_height() / 2)
            for tile_name, tile in tilesets[tileset].images.items():
                if selected_tile != tile_name:
                    screen.blit(tile, (x, y2))
                elif selected_tile == tile_name:
                    screen.blit(tile, (x, y2 - 5))
                
                x += tile.get_width() + 10
                if x > 150:
                    y2 += tile.get_height() + 10
                    x = 10
        y += 1
    
    # Tile handling ----------------------------------------------- #
    if selected_tile != None:
    # Tile placing -------------------------------------- #
        if KEYBINDS["Place tile"]:
            if (mouse_pos[0] > 150) and (mouse_pos[1] > 50):
                if SPACE == "Tile_space":
                    if typing != "":
                        new_tile_data = {"Tileset": selected_tileset, "Tile": selected_tile, "Type": "Custom", "Custom": typing}
                    elif typing == "":
                        new_tile_data = {"Tileset": selected_tileset, "Tile": selected_tile, "Type": "Collidable"}

                    # new_tile_data = {"Tileset": selected_tileset, "Tile": selected_tile, "Type": "Custom", "Custom": typing}
                    game_map.add_tile([X_OFFSET, Y_OFFSET], mouse_pos, SPACE, LAYER, new_tile_data)
                    
                    pos = game_map.get_loc([X_OFFSET, Y_OFFSET], mouse_pos)
                    pos = [(int(pos[0]) * TILESIZE) + X_OFFSET + TILESIZE / 2, (int(pos[1]) * TILESIZE) + Y_OFFSET + TILESIZE / 2]
                    vfx["Square_effects"].append(particles.SquareEffects(pos, 50, 6, 0.1, (255, 255, 255)))

                    typing = ""
        
    # Tile deleting ------------------------------------- #
        elif KEYBINDS["Delete tile"]:
            if (mouse_pos[0] > 150) and (mouse_pos[1] > 50):
                if SPACE == "Tile_space":
                    game_map.delete_tile([X_OFFSET, Y_OFFSET], mouse_pos, SPACE, LAYER)

                    # vfx["Circle_effects"]["Pixel_particles"].append(particles.PixelParticle(mouse_pos, random.randint(3, 10), 0.1, 1, GRAVITY, (255, 255, 255)))
                    vfx["Circle_effects"]["Circle_particles"].append(entities.Particle(mouse_pos, colour=(255, 255, 255), gravity= GRAVITY))
    
    # Get custom data ----------------------------------- #
    if KEYBINDS["Get hover"]:
        if (mouse_pos[0] > 150) and (mouse_pos[1] > 50):
            if SPACE == "Tile_space":
                loc = game_map.get_loc([X_OFFSET, Y_OFFSET], mouse_pos)
                try:
                    if game_map.map_data[SPACE][f"Layer_{LAYER}"][f"{loc[0]},{loc[1]}"]["Type"] == "Custom":
                        hover_typing = game_map.map_data[SPACE][f"Layer_{LAYER}"][f"{loc[0]},{loc[1]}"]["Custom"]
                    else:
                        hover_typing = "None"
                except Exception:
                    hover_typing = "None"
    
    # Editing ----------------------------------------------------- #
    if editing:
        editing_surf.fill((20, 50, 30))
        small_font.render(editing_surf, typing, [(editing_surf.get_width() - small_font.get_width(typing)) / 2, (editing_surf.get_height() + small_font.font["A"].get_height()) / 2])

        screen.blit(editing_surf, [(screen.get_width() - 200) / 2, (screen.get_height() - 100) / 2])
    
    # Handle events ----------------------------------------------- #
    for event in events:
        # QUIT ---------------------------------------------------- #
        if event.type == pygame.QUIT:
            running = False
        
        # VIDEORESIZE --------------------------------------------- #
        elif event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            
        # DROPFILE ------------------------------------------------ #
        elif event.type == pygame.DROPFILE:
            if event.file != "":
                game_map.open(event.file)

                dir, filename = os.path.split(event.file)

        # KEYDOWN ------------------------------------------------- #
        elif event.type == pygame.KEYDOWN:
            # K_ESCAPE ---------------------------------- #
            if event.key == KEYBINDS["Quit"]:
                running = False

            # K_CTRL ------------------------------------ #
            elif event.key == KEYBINDS["CTRL"]:
                CTRL = True

            # K_SHIFT ----------------------------------- #
            elif event.key == KEYBINDS["SHIFT"]:
                SHIFT = True
            
            # K_UP -------------------------------------- #
            elif event.key == KEYBINDS["Move map down"]:
                Y_OFFSET += 10
            
            # K_DOWN ------------------------------------ #
            elif event.key == KEYBINDS["Move map up"]:
                Y_OFFSET -= 10

            # K_LEFT ------------------------------------ #
            elif event.key == KEYBINDS["Move map left"]:
                X_OFFSET += 10

            # K_RIGHT ----------------------------------- #
            elif event.key == KEYBINDS["Move map right"]:
                X_OFFSET -= 10

            # K_MINUS ----------------------------------- #
            elif event.key == KEYBINDS["Layer back"]:
                if not editing:
                    LAYER -= 1
            
            # K_INSERT ---------------------------------- #
            elif event.key == KEYBINDS["Toggle typing"]:
                editing = not editing
            
            # SHIFT ------------------------------------- #
            elif SHIFT:
                # K_EQUALS -------------------- #
                if event.key == KEYBINDS["Layer forward"]:
                    LAYER += 1
                
                elif event.key == pygame.K_p:
                    print(game_map.map_data)
            
            # CTRL -------------------------------------- #
            elif CTRL:
                # K_o ------------------------- #
                if event.key == KEYBINDS["Open"]:
                    tkinter.Tk().withdraw()
                    file_path = askopenfilename()
                    # file = open(file_path)

                    if file_path != "":
                        game_map.open(file_path)

                        dir, filename = os.path.split(file_path)

                # K_n ------------------------- #
                elif event.key == KEYBINDS["New"]:
                    game_map.new_map()
                    filename = "New file"

                # K_s ------------------------- #
                elif event.key == KEYBINDS["Save"]:
                    if not SHIFT:
                        if save_name == None:
                            tkinter.Tk().withdraw()
                            file_path = asksaveasfilename()

                            if file_path != "":
                                if file_path.split(".")[-1] != "json":
                                    file_path = file_path + ".json"

                                game_map.save(file_path)

                                dir, filename = os.path.split(file_path)
                                save_name = file_path

                        elif save_name != None:
                            game_map.save(save_name)
                            
                    elif SHIFT:
                        tkinter.Tk().withdraw()
                        file_path = asksaveasfilename()

                        if file_path != "":
                            if file_path.split(".")[-1] != "json":
                                file_path = file_path + ".json"

                            game_map.save(file_path)

                            dir, filename = os.path.split(file_path)
                            save_name = file_path
                
                # K_SLASH --------------------- #
                elif event.key == KEYBINDS["Toggle space"]:
                    if SPACE == "Tile_space":
                        SPACE = "World_space"
                    elif SPACE == "World_space":
                        SPACE = "Tile_space"
            
            # Typing special data ----------------------- #
            if editing:
                for char in typing_chars:
                    if event.unicode == char:
                        typing += char
                if event.key == pygame.K_BACKSPACE:
                    typing = typing[:-1]
        
        # KEYUP --------------------------------------------------- #
        elif event.type == pygame.KEYUP:
            # K_CTRL ------------------------------------ #
            if event.key == KEYBINDS["CTRL"]:
                CTRL = False
            
            # K_SHIFT ----------------------------------- #
            elif event.key == KEYBINDS["SHIFT"]:
                SHIFT = False
        
        # MOUSEBUTTONDOWN ----------------------------------------- #
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Left mouse button ------------------------- #
            if event.button == 1:
                y = 0
                for tileset, value in tilesets.items():
                    if ((25 < mouse_pos[0] < 125) and ((50 - 16) / 2 + (25 * (y + 1)) + 17 < mouse_pos[1] < (50 - 16) / 2 + (25 * (y + 1)) + 42)):
                        if selected_tileset == tileset:
                            selected_tileset = None
                            selected_tile = None
                        elif selected_tileset != tileset:
                            selected_tileset = tileset
                            selected_tile = None
                    y += 1
                        
                x = 10
                y2 = 10 + (screen.get_height() / 2)
                if selected_tileset != None:
                    for tile_name, tile in tilesets[selected_tileset].images.items():
                        if (x < mouse_pos[0] < x + tile.get_width()) and (y2 - 5 < mouse_pos[1] < y2 - 5 + tile.get_height()):
                            if selected_tile != tile_name:
                                selected_tile = tile_name
                            elif selected_tile == tile_name:
                                selected_tile = None
                            typing = ""
                        
                        x += tile.get_width() + 10
                        if x > 150 - TILESIZE - 10:
                            y2 += tile.get_height() + 10
                            x = 10
                
                if (mouse_pos[0] > 150) and (mouse_pos[1] > 50):
                    if SPACE == "World_space":
                        if typing != "":
                            new_tile_data = {"Tileset": selected_tileset, "Tile": selected_tile, "Type": "Custom", "Custom": typing}
                        else:
                            new_tile_data = {"Tileset": selected_tileset, "Tile": selected_tile, "Type": "Collidable"}
                        game_map.add_tile([X_OFFSET, Y_OFFSET], mouse_pos, SPACE, LAYER, new_tile_data)
                        
                        vfx["Square_effects"].append(particles.SquareEffects(mouse_pos, 50, 6, 0.1, (255, 255, 255)))
            
            # Right mouse button ------------------------ #
            elif event.button == 3:
                if (mouse_pos[0] > 150) and (mouse_pos[1] > 50):
                    if SPACE == "World_space":
                        game_map.delete_tile([X_OFFSET, Y_OFFSET], mouse_pos, SPACE, LAYER)
        
    # Update display ---------------------------------------------- #
    pygame.display.update()
    clock.tick(FPS)

# Quit ---------------------------------------------------------------------- #
pygame.quit()
quit()
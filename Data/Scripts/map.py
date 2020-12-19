import pygame, json
import Data.Scripts.image_handling as img_handling

class Map:
    def __init__(self, tile_size = 32):
        self.map_data = {}
        self.tile_size = tile_size
    
    def new_map(self):
        self.map_data = {"Tile_space": {}, "World_space": {}}
        
    def open(self, path):
        file = open(path, "r")
        self.map_data = json.loads(file.read())
        file.close()

    def save(self, save_path):
        file = open(save_path, "w")
        file.write(json.dumps(self.map_data))
        file.close()
    
    def get_loc(self, scroll, mouse_pos):
        tile_loc = [int((mouse_pos[0] - scroll[0]) / self.tile_size), int((mouse_pos[1] - scroll[1]) / self.tile_size)]
        return tile_loc

    def add_tile(self, scroll, mouse_pos, space, layer_no, new_tile_data):
        if self.map_data != {}:
            if space == "Tile_space":
                tile_loc = self.get_loc(scroll, mouse_pos)
                try:
                    self.map_data[space][f"Layer_{layer_no}"][f"{tile_loc[0]},{tile_loc[1]}"] = new_tile_data
                except KeyError as k_error:
                    self.map_data[space][f"Layer_{layer_no}"] = {}
                    self.map_data[space][f"Layer_{layer_no}"][f"{tile_loc[0]},{tile_loc[1]}"] = new_tile_data
            elif space == "World_space":
                try:
                    self.map_data[space][f"Layer_{layer_no}"][f"{mouse_pos[0] - scroll[0]},{mouse_pos[1] - scroll[1]}"] = new_tile_data
                except KeyError as k_error:
                    self.map_data[space][f"Layer_{layer_no}"] = {}
                    self.map_data[space][f"Layer_{layer_no}"][f"{mouse_pos[0] - scroll[0]},{mouse_pos[1] - scroll[1]}"] = new_tile_data
    
    def delete_tile(self, scroll, mouse_pos, space, layer_no):
        if self.map_data != {}:
            if space == "Tile_space":
                tile_loc = self.get_loc(scroll, mouse_pos)
                pop = False
                for pos in self.map_data["Tile_space"][f"Layer_{layer_no}"]:
                    if pos == f"{str(tile_loc[0])},{str(tile_loc[1])}":
                        pop = True
                        pop_pos = pos
                if pop:
                    self.map_data["Tile_space"][f"Layer_{layer_no}"].pop(pop_pos)
            elif space == "World_space":
                pop = False
                for tile_pos in self.map_data["World_space"][f"Layer_{layer_no}"]:
                    pos = [int(position) for position in tile_pos.split(",")]
                    if (pos[0] <= mouse_pos[0] - scroll[0] < pos[0] + self.tile_size) and (pos[1] <= mouse_pos[1] - scroll[1] < pos[1] + self.tile_size):
                        pop = True
                        pop_pos = tile_pos
                if pop:
                    self.map_data["World_space"][f"Layer_{layer_no}"].pop(pop_pos)

class Tileset:
    def __init__(self, img_path, colours, order):
        self.img_path = img_path
        self.tileset_img = pygame.image.load(self.img_path).convert()
        images = img_handling.split_tiles(self.tileset_img, colours)
        self.images = {}
        for i in range(len(images)):
            image = images[i]
            self.images[order[i]] = image

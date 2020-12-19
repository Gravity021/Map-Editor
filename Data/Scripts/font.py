import pygame
import Data.Scripts.image_handling as image_handling

class Font:
    def __init__(self, fontsheet, font_colour, space_width, offset=1):
        if fontsheet == "Data/Images/Fontsheets/large_font.png":
            self.font_order = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
            ".","-",",",":","+","'","!","?","0","1","2","3","4","5","6","7","8","9","_"]
        elif fontsheet == "Data/Images/Fontsheets/small_font.png":
            self.font_order = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
            ".","-",",",":","+","'","!","?","0","1","2","3","4","5","6","7","8","9","(",")","/","_","=","\\","[","]","*",'"',"<",">",";"]
        fontsheet_img = pygame.image.load(fontsheet).convert()
        fontsheet_img.set_colorkey((0, 0, 0))
        self.fontsheet = image_handling.change_colour(fontsheet_img, (255, 0, 0), (font_colour))
        
        current_char_width = 0
        self.font = {}
        character_count = 0
        for x in range(self.fontsheet.get_width()):
            c = self.fontsheet.get_at((x, 0))
            if c[0] == 127:
                char_img = image_handling.clip(self.fontsheet, [x - current_char_width, 0, current_char_width, self.fontsheet.get_height()])
                self.font[self.font_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1

        self.offset = offset
        self.space_width = space_width
    
    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != " ":
                surf.blit(self.scale(self.font[char]), [loc[0] + x_offset, loc[1]])
                x_offset += self.font[char].get_width() * 2 + self.offset * 2
            else:
                x_offset += self.space_width * 2 + self.offset * 2

    def get_width(self, text):
        x_offset = 0
        for char in text:
            if char != " ":
                x_offset += self.font[char].get_width() + self.offset
            else:
                x_offset += self.space_width + self.offset
        
        return x_offset * 2
    
    def scale(self, surf):
        return pygame.transform.scale(surf, (surf.get_width() * 2, surf.get_height() * 2))
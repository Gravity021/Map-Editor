import pygame

def clip(tilesheet, clip_rect):
    surf = tilesheet.copy()
    surf.set_clip(clip_rect)
    img = tilesheet.subsurface(surf.get_clip())
    img.set_colorkey((0,0,0))
    return img.copy()

def change_colour(img, old_col, new_col):
    img = img.copy()
    img.set_colorkey(old_col)
    surf = pygame.Surface(img.get_size())
    surf.fill(new_col)
    surf.blit(img, (0,0))
    return surf

def split_tiles(tilesheet, cols):
    tiles = []
    width = 0
    height = 0
    x = 1
    y = 0
    y2 = 1
    for i in range(tilesheet.get_height()):
        if tilesheet.get_at((0, y)) == cols["colour 1"]:
            while x < tilesheet.get_width() + 1:
                if tilesheet.get_at((x, y)) == cols["colour 2"]:
                    width = x - 1
                    x = 0
                    break
                x += 1
            
            while y2 < tilesheet.get_height() + 1:
                if tilesheet.get_at((0, y2 + y)) == cols["colour 2"]:
                    height = y2 - 1
                    y2 = 0
                    break
                y2 += 1
            
            tiles.append(clip(tilesheet, [1, y+1, width, height]))
        y += 1

    return tiles
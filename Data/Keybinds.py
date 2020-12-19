import pygame

KEYBINDS = {
    "Place tile": False, # Left mouse
    "Get hover": False, # Middle mouse
    "Delete tile": False, # Right mouse
    "Quit": pygame.K_ESCAPE, # Escape
    "CTRL": pygame.K_LCTRL, # CTRL
    "SHIFT": pygame.K_LSHIFT, # SHIFT
    "Move map down": pygame.K_UP, # Up
    "Move map up": pygame.K_DOWN, # Down
    "Move map left": pygame.K_LEFT, # Left
    "Move map right": pygame.K_RIGHT, # Right
    "Layer back": pygame.K_MINUS, 
    "Layer forward": pygame.K_EQUALS, # Plus
    "Toggle typing": pygame.K_INSERT, # Tnsert
    "Open": pygame.K_o, 
    "New": pygame.K_n, 
    "Save": pygame.K_s,
    "Toggle space": pygame.K_SLASH
}
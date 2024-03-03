import pygame
from donnees import *

# Ecris un texte à un endroit donné
def write(fenetre, text, abs, ord, color = 'white', size = 32, font='lato.ttf', box=False):
    sketch_font = pygame.font.Font('fonts/' + font, round(size))
    if color == 'white' :
        color_font = (255,255,255)
    elif color == 'red':
        color_font = (255, 0, 0)
    elif color == 'blue':
        color_font = (0, 0, 255)
    elif color == 'dark green':
        color_font = (0, 160, 35)
    elif color == 'green':
        color_font = (0, 220, 60)
    elif color == 'light green':
        color_font = (0, 255, 0)
    elif color == 'black':
        color_font = (0, 0, 0)
    elif color == 'light grey':
        color_font = (230, 230, 230)
    elif color == 'grey':
        color_font = (150, 150, 150)
    elif color == 'orange':
        color_font = (226, 121, 0)
    elif color == 'yellow':
        color_font = (255, 220, 45)
    elif color == 'bronze':
        color_font = (152, 72, 7)
    elif color == 'brown':
        color_font = (130, 84, 31)
    elif color == 'argent':
        color_font = (145, 223, 204)
    elif color == 'or':
        color_font = (255, 192, 0)
    elif color == 'diamant':
        color_font = (0, 112, 192)
    elif color == 'legende':
        color_font = (218, 92, 221)
    elif type(color) == list:
        color_font = (color[0], color[1], color[2])
    else:
        color_font = (255, 255, 255)
    score_surface = sketch_font.render(text, True, color_font)
    fenetre.blit(score_surface, (abs, ord))
    if box:
        return (abs, round(abs + size * len(text)/1.2), ord, ord + size)


def color_stats(stat):
    if stat < 10:
        color_stat = [140, 140, 140]
    elif stat < 20:
        color_stat = [180, 180, 180]
    elif stat < 30:
        color_stat = [220, 220, 220]
    elif stat < 40:
        color_stat = [150, 150, 0]
    elif stat < 50:
        color_stat = [190, 190, 0]
    elif stat < 60:
        color_stat = [230, 230, 0]
    elif stat < 70:
        color_stat = [0, 150, 0]
    elif stat < 80:
        color_stat = [0, 180, 0]
    elif stat < 90:
        color_stat = [0, 210, 0]
    else:
        color_stat = [30, 255, 30]
    return color_stat


def load_image(image):
    resized_image = pygame.image.load(image)
    return resized_image


def scale_image(image, size):
    new_image = pygame.transform.scale(image, size)
    return new_image


# Affiche une image dans la fenêtre avec opacité réglable
def blit_alpha(target, source, abs, ord, opacity):
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-abs, -ord))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, (abs, ord))


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)
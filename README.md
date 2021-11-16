import pygame


pygame.init()


window_resolution = ((710,630))
mario_resolution = ((108,156))

#fenetre

pygame.display.set_caption("Mario")
window_surface = pygame.display.set_mode(window_resolution)
window_surface = pygame.display.set_mode(mario_resolution)

background_image = pygame.image.load("mur.png")
mario_image = pygame.image.load("1.png")
#background_image.convert('RGBA')
mario_image = pygame.image.load("1.png")
#mario_image.blit(mario_image, [500,500])

window_surface.blit(background_image,[0,0])
window_surface.blit(mario_image,[0,0])

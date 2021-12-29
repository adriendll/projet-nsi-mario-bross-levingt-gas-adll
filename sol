import pygame
class Sol(pygame.sprite.Sprite):

    def __init__(self, image):

        super(Sol, self).__init__()
        self.rect = pygame.Rect(0, 700, 1000, 300)
        self.image = image

    def afficher(self, surface):

        surface.blit(self.image, self.rect)

        #pygame.draw.rect(surface, ("Green"), self.rect)

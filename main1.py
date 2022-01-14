import sys
import time
import pygame
from pygame.sprite import Group
from joueurmario import Joueurmario
from sol import Sol
from plateforme import Plateforme
from ninja import Ninja
from projectiles import Projectile, Slash, Flamme


class Jeu:
    def __init__(self):

        "Fonctions de base :"

        self.ecran = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption('Mario Jeu')
        self.jeu_encours = True

        "Caractéristiques de Mario :"

        self.joueur_x, self.joueur_y = 200, 200
        self.taille = [32, 64]
        self.joueurmario_vitesse_x = 0
        self.joueurmario = Joueurmario(self.joueur_x, self.joueur_x, self.taille)
        self.image_joueur = pygame.image.load("marioracaille.png")
        self.image_joueur_rect = pygame.Rect(0, 0, 111, 145)
        self.joueurmario.gravite = (0, 10)
        self.joueurmario.resistance = (0, 0)
        self.joueurmario.collision_sol = True

        "Caractéristiques du Ninja :"

        self.ninja_x, self.ninja_y = 800, 200
        self.ninja_taille = [39, 64]
        self.ninja_vitesse_x = 0
        self.ninja = Ninja(self.joueur_x, self.joueur_y, self.ninja_taille)
        self.image_ninja = pygame.image.load('kakashi.png')
        self.ninja.gravite = (0, 10)
        self.ninja.resistance = (0, 0)
        self.ninja.collision_sol = True

        "Caractéristiques de l'arrière plan, du sol et des plateformes :"

        self.image_arriere_plan = pygame.image.load("chateaubowser.png")
        self.arriere_plan_rect = [0, 0, 724, 397]
        self.image_mur = self.image_arriere_plan.subsurface(self.arriere_plan_rect)
        self.image_mur = pygame.transform.scale(self.image_mur, (1000, 700))
        self.rect = pygame.Rect(0, 0, 1000, 1000)

        self.image_sol_brique = pygame.image.load("solenbrique.jpg")
        self.image_sol_rect = [0, 0, 450, 300]
        self.image_sol = self.image_sol_brique.subsurface(self.image_sol_rect)
        self.image_sol = pygame.transform.scale(self.image_sol, (1000, 300))
        self.sol = Sol(self.image_sol)

        self.plateforme_groupe = Group()
        self.plateforme_liste_rect = [
            pygame.Rect(0, 550, 300, 50), pygame.Rect(700, 550, 300, 50),
            pygame.Rect(340, 400, 300, 50)
        ]
        self.image_plat_rect = [0, 0, 300, 50]
        self.image_plat = self.image_sol_brique.subsurface(self.image_plat_rect)
        self.image_plat = pygame.transform.scale(self.image_plat, (300, 50))

        "Fonctionnalités du temps dans jeu:"

        self.horloge = pygame.time.Clock()
        self.fps = 30
        self.slash = Group()
        self.projectile = Group()
        self.t1, self.t2 = 0, 0
        self.delta_temps = 0

        "Caractéristiques des projectiles (attaque de Mario) :"

        self.projectile_groupe = Group()
        self.image_boule_de_feu = pygame.image.load("fireball.png")
        self.image_boule_de_feu_rect = pygame.Rect(175, 70, 9, 9)
        self.image_boule_de_feu = self.image_boule_de_feu.subsurface(self.image_boule_de_feu_rect)

        "Attaques du Ninja) :"

        self.slash_groupe = Group()
        self.image_slash = pygame.image.load("kakashi.png")
        self.slash_image_rect = pygame.Rect(907, 3834, 77, 56)
        self.image_slash = self.image_ninja.subsurface(self.slash_image_rect)
        self.image_slash = pygame.transform.scale(self.image_slash, (30, 30))

        self.flamme_groupe = Group()
        self.image_flamme = pygame.image.load("kakashi.png")
        self.flamme_image_rect = pygame.Rect(631, 4335, 12, 13)
        self.image_flamme = self.image_ninja.subsurface(self.flamme_image_rect)
        self.image_flamme = pygame.transform.scale(self.image_flamme, (30, 30))

        "Boutton pause :"

        self.debut_timer = 90000
        self.bouton = pygame.image.load("button.png")
        self.bouton_rect = pygame.Rect(378, 30, 153, 153)
        self.image_bouton = self.bouton.subsurface(self.bouton_rect)
        self.image_bouton = pygame.transform.scale(self.image_bouton, (50, 50))

        self.replay_bouton = pygame.image.load("button.png")
        self.info_bouton = pygame.image.load("button.png")

        self.x_souris, self.y_souris = 0, 0
        self.etat_1 = False
        self.but_du_jeu = False

    """
    Boucle principale :
    """

    def boucle_principale(self):

        "Déclaration des dictionnaires d'images des personnages :"

        dictionnaire_vide_joueur = {}
        dictionnaire_images_joueur = self.joueurmario.convertir_rect_surface(self.image_joueur, dictionnaire_vide_joueur)
        dictionnaire_vide_ninja = {}
        dictionnaire_images_ninja = self.ninja.convertir_rect_surface(self.image_ninja, dictionnaire_vide_ninja)

        while self.jeu_encours:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    self.x_souris, self.y_souris = pygame.mouse.get_pos()

                    "Boutton pause"

                    if (self.x_souris < 525 and self.x_souris > 475 and self.y_souris < 190 and self.y_souris > 140):
                        self.etat_1 = True

                    "Boutton continuer"

                    if (self.x_souris < 900 and self.x_souris > 850 and self.y_souris < 240 and self.y_souris > 190) and self.etat_1:
                        self.etat_1 = False

                    "Boutton restart"

                    if (self.x_souris < 900 and self.x_souris > 850 and self.y_souris < 200 and self.y_souris > 150) and self.etat_1:
                        self.recommencer()
                        self.etat_1 = False

                    "Boutton info"

                    if (self.x_souris < 70 and self.x_souris > 20 and self.y_souris < 190 and self.y_souris > 140) and self.etat_1:
                        self.but_du_jeu = True


                "ACTIONS DE MARIO:"

                "Actions quand une touche est enfoncée :"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.joueurmario_vitesse_x = 10
                        self.joueurmario.direction = 1
                        self.joueurmario.etat = "bouger"

                    if event.key == pygame.K_LEFT:
                        self.joueurmario_vitesse_x = -10
                        self.joueurmario.direction = -1
                        self.joueurmario.etat = "bouger"

                    if event.key == pygame.K_SPACE:
                        self.joueurmario.a_sauter = True
                        self.joueurmario.nombre_de_saut += 1
                        self.joueurmario.etat = "saute"

                    if event.key == pygame.K_s:
                        self.t2 = time.time()
                        self.joueurmario.a_tire = True
                        self.joueurmario.etat = "attaque"

                    if event.key == pygame.K_p:
                        self.t1 = time.time()

                "Actions quand une touche est levée :"

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.joueurmario_vitesse_x = 0
                        self.joueurmario.etat = "debout"

                    if event.key == pygame.K_LEFT:
                        self.joueurmario_vitesse_x = 0
                        self.joueurmario.etat = "debout"

                    if event.key == pygame.K_s:
                        self.joueurmario.etat = "debout"

                "ACTIONS DU NINJA :"

                "Actions quand une touche est enfoncée :"

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_d:
                        self.ninja_vitesse_x = 10
                        self.ninja.direction = 1
                        self.ninja.etat = "bouger"

                    if event.key == pygame.K_q:
                        self.ninja_vitesse_x = -10
                        self.ninja.direction = -1
                        self.ninja.etat = "bouger"

                    if event.key == pygame.K_z:
                        self.ninja.a_sauter = True
                        self.ninja.nombre_de_saut += 1
                        self.ninja.etat = "saute"

                    if event.key == pygame.K_e:
                        self.ninja.a_attaque = True
                        self.ninja.etat = "attaque"

                    if event.key == pygame.K_r:
                        self.ninja.a_attaque_flamme = True
                        self.ninja.etat = "attaque de flamme"

                "Actions quand une touche est levée :"

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_d:
                        self.ninja_vitesse_x = 0
                        self.ninja.etat = "debout"

                    if event.key == pygame.K_q:
                        self.ninja_vitesse_x = 0
                        self.ninja.etat = "debout"

                    if event.key == pygame.K_e:
                        self.ninja.a_attaque = False
                        self.ninja.etat = "debout"

                    if event.key == pygame.K_r:
                        self.ninja.a_attaque_flamme = False
                        self.ninja.etat = "debout"

            "ATTAQUES DES PERSONNAGES /"

            "Attaque de Mario :"

            if self.joueurmario.a_tire:
                if len(self.projectile_groupe) < self.joueurmario.tir_autorise and self.delta_temps > 0.05:
                    projectile = Projectile(self.joueurmario.rect.x + 20, self.joueurmario.rect.y + 20, [12, 12],
                                            self.joueurmario.direction,
                                            self.image_boule_de_feu)
                    self.projectile_groupe.add(projectile)
                    self.joueurmario.a_tire = False

            for projectile in self.projectile_groupe:
                projectile.mouvement(50)
                if projectile.rect.right >= self.rect.right or projectile.rect.left <= self.rect.left:
                    self.projectile_groupe.remove(projectile)

                if self.ninja.rect.colliderect(projectile.rect):
                    self.projectile_groupe.remove(projectile)
                    self.ninja.degats_recus = 10
                    if self.delta_temps > 2:
                        self.ninja.degats_recus = 30
                    self.ninja.vie -= self.ninja.degats_recus
                    self.ninja.degats_recus = 0

            if self.joueurmario.vie <= 0:
                self.joueurmario.etat = 'mort'
            if self.ninja.vie <= 0:
                self.ninja.etat = 'mort'

            "ATTAQUE DU NINJA :"

            "Attaque de base :"

            if self.ninja.a_attaque:
                if len(self.slash_groupe) < self.ninja.tir_autorise :
                    slash = Slash (self.ninja.rect.x + 20, self.ninja.rect.y - 5, [30, 30],
                                   self.image_slash)
                    self.slash_groupe.add(slash)
                    self.ninja.a_attaque = False

            for slash in self.slash_groupe:
                slash.mouvement(50)
                if slash.rect.right >= self.rect.right or slash.rect.left <= self.rect.left:
                    self.slash_groupe.remove(slash)

                if self.joueurmario.rect.colliderect(slash.rect):
                    self.slash_groupe.remove(slash)
                    self.joueurmario.rect.x += 3
                    self.joueurmario.degats_recus = 10
                    self.joueurmario.vie -= self.joueurmario.degats_recus
                    self.joueurmario.degats_recus = 0

                if self.joueurmario.vie <= 0:
                    self.joueurmario.etat = 'mort'
                if self.ninja.vie <= 0:
                    self.ninja.etat = 'mort'

            "Attaque 'Flamme' :"

            if self.ninja.a_attaque_flamme :
                if len(self.flamme_groupe) < self.ninja.tir_autorise :
                    flamme = Flamme (self.ninja.rect.x + 20, self.ninja.rect.y - 5, [30, 30], self.image_flamme)
                    self.flamme_groupe.add(flamme)
                    self.ninja.a_attaque_flamme = False

            for flamme in self.flamme_groupe:
                flamme.mouvement(50)
                if flamme.rect.right >= self.rect.right or flamme.rect.left <= self.rect.left:
                    self.flamme_groupe.remove(flamme)

                if self.joueurmario.rect.colliderect(slash.rect):
                    self.slash_groupe.remove(slash)
                    self.joueurmario.rect.x += 3
                    self.joueurmario.degats_recus = 10
                    self.joueurmario.vie -= self.joueurmario.degats_recus
                    self.joueurmario.degats_recus = 0

                if self.joueurmario.vie <= 0:
                    self.joueurmario.etat = 'mort'
                if self.ninja.vie <= 0:
                    self.ninja.etat = 'mort'

            "Collision entre Mario et le sol :"

            if self.sol.rect.colliderect(self.joueurmario.rect):
                self.joueurmario.resistance = (0, -10)
                self.joueurmario.collision_sol = True
                self.joueurmario.nombre_de_saut = 0

            else:
                self.joueurmario.resistance = (0, 0)

            if self.joueurmario.a_sauter and self.joueurmario.collision_sol:
                if self.joueurmario.nombre_de_saut < 2:
                    self.joueurmario.sauter()
                    self.joueurmario.etat = "saute"

            "Collision entre Ninja et le sol :"

            if self.sol.rect.colliderect(self.ninja.rect):
                self.ninja.resistance = (0, -10)
                self.ninja.collision_sol = True
                self.ninja.nombre_de_saut = 0

            else:
                self.ninja.resistance = (0, 0)

            if self.ninja.a_sauter and self.ninja.collision_sol:
                if self.ninja.nombre_de_saut < 2:
                    self.ninja.sauter()

            "Collision entre les personnages et les plateformes :"

            for rectangle in self.plateforme_liste_rect:
                plateforme = Plateforme(rectangle, self.image_plat)
                self.plateforme_groupe.add(plateforme)

                if self.joueurmario.rect.midbottom[1] // 10 * 10 == plateforme.rect.top \
                        and self.joueurmario.rect.colliderect(rectangle):
                    self.joueurmario.resistance = (0, -10)
                    self.joueurmario.nombre_de_saut = 0

                if self.ninja.rect.midbottom[1] // 10 * 10 == plateforme.rect.top \
                        and self.ninja.rect.colliderect(rectangle):
                    self.ninja.resistance = (0, -10)
                    self.ninja.nombre_de_saut = 0

            "Timer :"

            secondes = (self.debut_timer - pygame.time.get_ticks()) // 1000

            if secondes == 0:
                break

            "Déclarations de toutes les fonctionnalités dans la boucle principale du jeu :"

            self.delta_temps = self.t2 - self.t1
            self.ninja.mouvement(self.ninja_vitesse_x)
            self.joueurmario.mouvement(self.joueurmario_vitesse_x)
            self.joueurmario_gravite_jeu()
            self.ninja_gravite_jeu()
            self.ecran.blit(self.image_mur, self.arriere_plan_rect)
            self.sol.afficher(self.ecran)
            self.joueurmario.rect.clamp_ip(self.rect)
            self.ninja.rect.clamp_ip(self.rect)
            self.joueurmario.afficher(self.ecran, dictionnaire_images_joueur)
            self.ninja.afficher(self.ecran, dictionnaire_images_ninja)
            self.horloge.tick(self.fps)
            self.ecran.blit(self.image_bouton, (475, 140, 50, 50))
            self.creer_message('grande', '{}'.format(secondes), [485, 195, 20, 20], (255, 255, 255))

            for plateforme in self.plateforme_groupe:
                plateforme.afficher(self.ecran)

            for projectile in self.projectile_groupe:
                projectile.afficher(self.ecran, self.delta_temps)

            for slash in self.slash_groupe:
                slash.afficher(self.ecran)

            for flamme in self.flamme_groupe:
                flamme.afficher(self.ecran)

            if self.etat_1:
                pygame.draw.rect(self.ecran, (255, 255, 255), (0, 0, 1000, 100), 2)
                pygame.draw.rect(self.ecran, (0, 0, 0), (0, 0, 1000, 280))
                self.ecran_menu()
                if self.but_du_jeu:
                    self.creer_message("petite", f"Le dernier survivant gagne !!! ", (100, 150, 80, 80), (255, 255, 255))

            pygame.display.flip()


    "Définition des fonctions gravité des personnages :"

    def joueurmario_gravite_jeu(self):

        self.joueurmario.rect.y += self.joueurmario.gravite[1] + self.joueurmario.resistance[1]

    def ninja_gravite_jeu(self):

        self.ninja.rect.y += self.ninja.gravite[1] + self.ninja.resistance[1]

    def creer_message(self, font, message, message_rectangle, couleur):

        if font == 'petite':
            font = pygame.font.SysFont('lato', 20, False)

        elif font == 'moyenne':
            font = pygame.font.SysFont('lato', 30, False)

        elif font == 'grande':
            font = pygame.font.SysFont('lato', 40, True)

        message = font.render(message, True, couleur)
        self.ecran.blit(message, message_rectangle)

    def ecran_menu(self):
        """
        Afficher les bouttons
        """
        image_rect = pygame.Rect(539, 441, 196, 196)
        image_restart = self.replay_bouton.subsurface(image_rect)
        image_restart = pygame.transform.scale(image_restart, (55, 55))

        image_continuer_rect = pygame.Rect(189, 30, 153, 153)
        image_continuer = self.bouton.subsurface(image_continuer_rect)
        image_continuer = pygame.transform.scale(image_continuer, (50, 50))

        image_info_rect = pygame.Rect(817, 445, 187, 187)
        image_info = self.bouton.subsurface(image_info_rect)
        image_info = pygame.transform.scale(image_info, (40, 40))

        self.ecran.blit(image_restart, (850, 140, 50, 50))
        self.ecran.blit(image_continuer, (850, 200, 50, 50))
        self.ecran.blit(image_info, (20, 140, 50, 50))

    def recommencer(self):

        self.joueurmario.vie = 100
        self.joueurmario.rect.x = 150
        self.joueurmario.rect.y = 200
        self.joueurmario.etat = "debout"

        self.ninja.vie = 100
        self.ninja.rect.x = 800
        self.ninja.rect.y = 200
        self.ninja.direction = -1
        self.ninja.etat = "debout"





if __name__ == '__main__':
    pygame.init()
    Jeu().boucle_principale()
    pygame.quit()

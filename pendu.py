import pygame
import math
import random

# Configuration de l'affichage
pygame.init()
LARGEUR, HAUTEUR = 1500, 700
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Pendu!") 
scor_file = "scores.txt"

# Variables des boutons
RAYON = 20
ECART = 15
lettres = []
debut_x = round((LARGEUR - (RAYON * 2 + ECART) * 13) / 2)
debut_y = 400
A = 65
for i in range(26):
    x = debut_x + ECART * 2 + ((RAYON * 2 + ECART) * (i % 13))
    y = debut_y + ((i // 13) * (ECART + RAYON * 2))
    lettres.append([x, y, chr(A + i), True])

# Polices
POLICE_LETTRE = pygame.font.SysFont('comicsans', 40)
POLICE_MOT = pygame.font.SysFont('comicsans', 60)
POLICE_TITRE = pygame.font.SysFont('comicsans', 70)

# Charger les images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# Variables du jeu
statut_pendu = 0
statut_pendu_max = 6  # Nombre maximum d'états du pendu
mots = []  # Liste pour stocker les mots du fichier
with open("mots.txt") as fichier_mots:
    mots = [mot.strip() for mot in fichier_mots.readlines()]
mot = random.choice(mots)
devinees = []

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Configurer la boucle de jeu
def dessiner():
    fenetre.fill(BLANC)

    # Dessiner le titre
    texte = POLICE_TITRE.render("PENDU ", 1, NOIR)
    fenetre.blit(texte, (LARGEUR/2 - texte.get_width()/2, 20))

    # Dessiner le mot
    mot_affiche = ""
    for lettre in mot:
        if lettre in devinees:
            mot_affiche += lettre + " "
        else:
            mot_affiche += "_ "
    texte = POLICE_MOT.render(mot_affiche, 1, NOIR)
    fenetre.blit(texte, (400, 200))

    # Dessiner les boutons
    for lettre in lettres:
        x, y, ltr, visible = lettre
        if visible:
            pygame.draw.circle(fenetre, NOIR, (x, y), RAYON, 3)
            texte = POLICE_LETTRE.render(ltr, 1, NOIR)
            fenetre.blit(texte, (x - texte.get_width()/2, y - texte.get_height()/2))

    fenetre.blit(images[statut_pendu], (150, 100))
    pygame.display.update()

def afficher_message(message):
    pygame.time.delay(1000)
    fenetre.fill(BLANC)
    texte = POLICE_MOT.render(message, 1, NOIR)
    fenetre.blit(texte, (LARGEUR/2 - texte.get_width()/2, HAUTEUR/2 - texte.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def jeu_principal():
    global statut_pendu
    FPS = 60
    horloge = pygame.time.Clock()
    en_cours = True

    while en_cours:
        horloge.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for lettre in lettres:
                    x, y, ltr, visible = lettre
                    if visible:
                        distance = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if distance < RAYON:
                            lettre[3] = False
                            devinees.append(ltr)
                            if ltr not in mot:
                                statut_pendu += 1
            elif event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    lettre = chr(event.key).upper()
                    for lettre_info in lettres:
                        x, y, ltr, visible = lettre_info
                        if visible and ltr == lettre:
                            lettre_info[3] = False
                            devinees.append(ltr)
                            if ltr not in mot:
                                statut_pendu += 1

        dessiner()

        gagne = all(lettre in devinees for lettre in mot)

        if gagne:
            afficher_message("Vous avez gagné !")
            break

        if statut_pendu == statut_pendu_max:
            afficher_message("Vous avez perdu ! Le mot était : {}".format(mot))
            break

if __name__ == "__main__":
    jeu_principal()

pygame.quit()















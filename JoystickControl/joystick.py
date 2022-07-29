import pygame


# Définir des couleurs.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# Ceci est une classe simple qui nous aidera à imprimer à l'écran.
# Cela n'a rien à voir avec les joysticks, juste la sortie du
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Définissez la largeur et la hauteur de l'écran (largeur, hauteur).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Boucle jusqu'à ce que l'utilisateur clique sur le bouton de fermeture.
done = False

# Utilisé pour gérer la vitesse de mise à jour de l'écran.
clock = pygame.time.Clock()

# Initialiser les joysticks.
pygame.joystick.init()

# Préparez-vous à imprimer.
textPrint = TextPrint()

# -------- Boucle du programme principal -----------
while not done:
    #
    # ÉTAPE DE TRAITEMENT DE L'ÉVÉNEMENT
    #
    # Actions possibles du joystick : JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # L'utilisateur a fait quelque chose.
        if event.type == pygame.QUIT: # Si l'utilisateur a cliqué sur fermer.
            done = True # Signalez que nous avons terminé afin que nous quittions cette boucle.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    #
    # ÉTAPE DESSIN
    #
    # Tout d'abord, effacez l'écran en blanc. Ne pas mettre d'autres commandes de dessin
    # au-dessus, ou ils seront effacés avec cette commande.
    screen.fill(WHITE)
    textPrint.reset()

    # Obtenez le nombre de joysticks.
    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # Pour chaque joystick :
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id() est une méthode SDL2
            jid = joystick.get_id()
        textPrint.tprint(screen, "Joystick {}".format(jid))
        textPrint.indent()

        # Obtenez le nom du système d'exploitation pour le contrôleur/joystick.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid() est une méthode SDL2
            pass
        else:
            textPrint.tprint(screen, "GUID: {}".format(guid))

        # Habituellement, les axes fonctionnent par paires, haut/bas pour un, et gauche/droite pour
        # L'autre.
        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            if i==1:
                print("Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.tprint(screen,
                             "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()

        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        # Position du chapeau. Tout ou rien pour la direction, pas un flotteur comme
        # get_axis(). La position est un tuple de valeurs int (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()

    #
    # TOUS LES CODES À DESSINER DOIVENT PASSER AU-DESSUS DE CE COMMENTAIRE
    #

    # Allez-y et mettez à jour l'écran avec ce que nous avons dessiné.
    pygame.display.flip()

    # Limite à 20 images par seconde.
    clock.tick(20)

# Fermez la fenêtre et quittez.
# Si vous oubliez cette ligne, le programme 'se bloquera'
# à la sortie si exécuté depuis IDLE.
pygame.quit()
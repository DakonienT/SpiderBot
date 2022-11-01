import pygame
import socket  #UDP Com
import pickle
import cv2
import logging
import numpy as np
import time
from PIL import Image, ImageDraw
CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
 

logging.basicConfig(format='%(asctime)s %(message)s')
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)
#Setup UDP com with server
serverAddressPort   = ("127.0.0.1", 20001)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
bufferSize          = 1024
logging.info("Emitting on UDP for Joystick on " + str(serverAddressPort[0]) + ":" + str(serverAddressPort[1]))
# Définir des couleurs.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
#socket for image
s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
ip="127.0.0.1"
port=6666
s.bind((ip,port))
logging.info("Listening UDP fof image on " + str(ip) + ":" + str(port))

logging.debug('Loading NN...')
net = cv2.dnn.readNet(r"C:\Users\simon\Desktop\VMShared\SpiderBot\JoystickControl\yolov3.weights",r"C:\Users\simon\Desktop\VMShared\SpiderBot\JoystickControl\yolov3.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
#net = cv2.dnn.readNetFromDarknet(r'C:\Users\simon\Desktop\VMShared\SpiderBot\JoystickControl\yolov3.cfg', r'C:\Users\simon\Desktop\VMShared\SpiderBot\JoystickControl\yolov3.weights')
#net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
#net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
logging.debug('NN Loaded !')
logging.debug('Loading COCO...')
class_names = []
with open(r"C:\Users\simon\Desktop\VMShared\SpiderBot\JoystickControl\coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]
#classes = open(r'C:\Users\simon\Desktop\VMShared\SpiderBot\JoystickControl\coco.names').read().strip().split('\n')
#np.random.seed(42)
#colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')
logging.debug('COCO Loaded !')

#ln = net.getLayerNames()
#print(net.getUnconnectedOutLayers())
#ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
class detection : 
    
    def YOLO(self, frame, target):
        boxes_return = []
        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end = time.time()
        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s : %f" % (class_names[classid], score)
            #label = class_names[classid[0]]
            #print(classid)
            #boxes_return.append(box)
            #if(class_names[classid] == "person"):
            #print(box)
            cv2.rectangle(frame, box, (255,134, 56), 2)
            x_box_TL = box[0]
            y_box_TL = box[1]
            x_box_BR = box[2]
            y_box_BR = box[3]
            xlist = np.arange(x_box_TL, x_box_BR)
            ylist = np.arange(y_box_TL, y_box_BR)
            #print(ylist)
            
            if(targetX in xlist and targetY in ylist):
                print("!!!!!!!!!!!!!!!!!!!!")
            #print(box)
            #if(target[0] in np.arange(box[0], ))
            
                cv2.putText(frame, label, (box[0], box[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        fps = "FPS: %.2f " % (1 / (end - start))
        #cv2.putText(frame, fps, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        return frame, fps, boxes_return

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
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def get_opencv_img_res(opencv_image):
    height, width = opencv_image.shape[:2]
    return width, height

def convert_opencv_img_to_pygame(opencv_image):
    """
Convert OpenCV images for Pygame.

    see https://blanktar.jp/blog/2016/01/pygame-draw-opencv-image.html
    """
    opencv_image = opencv_image[:,:,::-1]  #Since OpenCV is BGR and pygame is RGB, it is necessary to convert it.
    shape = opencv_image.shape[1::-1]  #OpenCV(height,width,Number of colors), Pygame(width, height)So this is also converted.
    pygame_image = pygame.image.frombuffer(opencv_image.tostring(), shape, 'RGB')

    return pygame_image

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def rounded_rectangle (src, top_left, bottom_right, radius=1, color=255, thickness=1, line_type=cv2.LINE_AA):

    #  corners:
    #  p1 - p2
    #  |     |
    #  p4 - p3

    p1 = top_left
    p2 = (bottom_right[1], top_left[1])
    p3 = (bottom_right[1], bottom_right[0])
    p4 = (top_left[0], bottom_right[0])

    height = abs(bottom_right[0] - top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height/2))

    if thickness < 0:

        #big rect
        top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

        top_left_rect_left = (p1[0], p1[1] + corner_radius)
        bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

        top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
        bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

        all_rects = [
        [top_left_main_rect, bottom_right_main_rect], 
        [top_left_rect_left, bottom_right_rect_left], 
        [top_left_rect_right, bottom_right_rect_right]]

        [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

    # draw straight lines
    cv2.line(src, (p1[0] + corner_radius, p1[1]), (p2[0] - corner_radius, p2[1]), color, abs(thickness), line_type)
    cv2.line(src, (p2[0], p2[1] + corner_radius), (p3[0], p3[1] - corner_radius), color, abs(thickness), line_type)
    cv2.line(src, (p3[0] - corner_radius, p4[1]), (p4[0] + corner_radius, p3[1]), color, abs(thickness), line_type)
    cv2.line(src, (p4[0], p4[1] - corner_radius), (p1[0], p1[1] + corner_radius), color, abs(thickness), line_type)

    # draw arcs
    cv2.ellipse(src, (p1[0] + corner_radius, p1[1] + corner_radius), (corner_radius, corner_radius), 180.0, 0, 90, color ,thickness, line_type)
    cv2.ellipse(src, (p2[0] - corner_radius, p2[1] + corner_radius), (corner_radius, corner_radius), 270.0, 0, 90, color , thickness, line_type)
    cv2.ellipse(src, (p3[0] - corner_radius, p3[1] - corner_radius), (corner_radius, corner_radius), 0.0, 0, 90,   color , thickness, line_type)
    cv2.ellipse(src, (p4[0] + corner_radius, p4[1] - corner_radius), (corner_radius, corner_radius), 90.0, 0, 90,  color , thickness, line_type)

    return src

def drawControl(avarr, gd, thr, yaw):
    pixel_array = np.full((120, 120, 3), (255,255,255), dtype=np.uint8)
    rounded = rounded_rectangle(pixel_array, (0,0), (120, 120), 0.3,color=(0,0,0), thickness = -1)
    cv2.line(rounded, (60, 0), (60, 120), (0, 255, 0), 1)
    cv2.line(rounded, (0, 60), (120, 60), (0, 255, 0), 1)
    map_avarr = translate(avarr, -1, 1, 0, 120)
    map_gd = translate(gd, -1, 1, 0, 120)
    map_thr = translate(thr, -1, 1, 70, 110)
    map_yaw = int(translate(yaw, -1, 1, 22, 98))
    logging.info("map_avarr : " + str(map_avarr))
    logging.info("map_gd : " + str(map_gd))
    cv2.line(rounded, (10, 110), (10, int(map_thr)), (255, 0, 0), 2)
    cv2.circle(rounded, (int(map_gd), int(map_avarr)), 6, (0,200,0),1)
    cv2.line(rounded, (20, 110), (100, 110), (0, 255, 0), 1)
    cv2.line(rounded, (map_yaw, 105), (map_yaw, 115), (0, 0, 255), 1)    
    return rounded

pointerColor = (0, 255, 0) # default color for pointer


    

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
targetX = 1
targetY = 0
det = detection()
button1state = 0 #For rising edge detection
lastButton1state = 0
while not done:
    #
    # ÉTAPE DE TRAITEMENT DE L'ÉVÉNEMENT
    #
    # Actions possibles du joystick : JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    x=s.recvfrom(1000000)
    clientip = x[1][0]
    data=x[0]
    #print(data)
    data=pickle.loads(data)
    #print(type(data))
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    
    for event in pygame.event.get(): # L'utilisateur a fait quelque chose.
        if event.type == pygame.QUIT: # Si l'utilisateur a cliqué sur fermer.
            done = True # Signalez que nous avons terminé afin que nous quittions cette boucle.
        #elif event.type == pygame.JOYBUTTONDOWN:
            #print("Joystick button pressed.")
        #elif event.type == pygame.JOYBUTTONUP:
            #print("Joystick button released.")

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

    # Pour chaque joystick :\python-opencv-cv2-line-method\
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
            axis_avarr = joystick.get_axis(1)
         
            axis_gd = joystick.get_axis(0)
            axis_yaw = joystick.get_axis(3)
            axis_thr = joystick.get_axis(2)

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
            #print(hat[0])
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()
        if(0 <= targetX <= data.shape[1] ):
            targetX = targetX + hat[0] * 5
        if(targetX <= 0):
            targetX = 0
        if(targetX >= data.shape[1]):
            targetX = data.shape[1]
        
        if(0 <= targetY <= data.shape[0] ):
            targetY =  targetY - hat[1] * 5
        if(targetY < 0):
            targetY = 0
        if(targetY >= data.shape[0]):
            targetY = data.shape[0]
        
        #Code for rising edge detection on BT 1
        #button1Read = joystick.get_button(0)
        button1state = joystick.get_button(0)
        if(button1state != lastButton1state):
            if(button1state == 1):
                logging.debug("button 1 pressed")
                #updatePointercolor()
                if (pointerColor == (0, 255, 0)):
                    pointerColor = (0, 0, 255)
                else:
                    pointerColor = (0, 255, 0)
            else:
                logging.debug("Button 1 released")
        lastButton1state = button1state


        targetPosition = (targetX, targetY)
        frame, fps, boxes = det.YOLO(data, targetPosition)
        textPrint.tprint(screen, fps)
        textPrint.tprint(screen, str(len(boxes)) + " objects detected")
        
        textPrint.tprint(screen, "Cursor position: "+ str(targetPosition))
        cv2.circle(frame, targetPosition, 12, pointerColor,2)
        textPrint.unindent()
        msgFromJoystick = "Joystick%"+str(axis_avarr)+"%"+str(axis_gd)+"%"+str(axis_thr)+"%"+str(hat[0])+"%"+str(hat[1])
        bytesToSend = str.encode(msgFromJoystick)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)


        img_desired_width_pg = 500-40
        resized = image_resize(frame, img_desired_width_pg)
        pygame_image = convert_opencv_img_to_pygame(resized)
        control_image = convert_opencv_img_to_pygame(drawControl(axis_avarr, axis_gd, axis_thr, axis_yaw))
        screen.blit(pygame_image, (20,700-resized.shape[1]+110))
        screen.blit (control_image, (300, (700-resized.shape[1]+110)/2 - 60))
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
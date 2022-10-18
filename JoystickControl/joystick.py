import pygame
import socket  #UDP Com
import pickle
import cv2
import logging
import numpy as np
import time

CONFIDENCE_THRESHOLD = 0.2
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


"""def YOLO(frame, dsize):
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, dsize, swapRB=True, crop=False)
    r = blob[0, 0, :, :]
    net.setInput(blob)
    outputs = net.forward(ln)
    boxes = []
    confidences = []
    classIDs = []
    h, w = frame.shape[:2]
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > 0.1:
                box = detection[:4] * np.array([w, h, w, h])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                box = [x, y, int(width), int(height)]
                boxes.append(box)
                confidences.append(float(confidence))
                classIDs.append(classID)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = (0,0,255)
            if (classes[classIDs[i]] == 'person'):
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame, boxes"""
def YOLO(frame):
    start = time.time()
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    end = time.time()
    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        label = "%s : %f" % (class_names[classid], score)
        #label = class_names[classid[0]]
        print(classid)
        cv2.rectangle(frame, box, color, 2)
        cv2.putText(frame, label, (box[0], box[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    fps = "FPS: %.2f " % (1 / (end - start))
    cv2.putText(frame, fps, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    return frame

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
            map_avarr = translate(axis_avarr, -1, 1, 0, 700)
            #print(map_avarr)
            axis_gd = joystick.get_axis(0)
            map_gd = translate(axis_gd, -1, 1, 0, 500)
            pygame.draw.circle(screen, (25,0,243), (map_gd, map_avarr), 10)
            axis_thr = joystick.get_axis(2)
            map_thr = translate(axis_thr, -1, 1, 25, 200)
            pygame.draw.line(screen, (0,255,0), (25, 25), (25, map_thr), width=5)

            #if i==1:
               #print("Axis {} value: {:>6.3f}".format(i, axis))
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

        frame = YOLO(data)
        targetPosition = (targetX, targetY)
        #pygame.draw.rect(screen, (0,0,255), (0,0, 100,100), width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1)
        cv2.circle(frame, targetPosition, 12, (0,234,0),2)
        textPrint.unindent()
        msgFromJoystick = "Joystick%"+str(axis_avarr)+"%"+str(axis_gd)+"%"+str(axis_thr)+"%"+str(hat[0])+"%"+str(hat[1])
        bytesToSend = str.encode(msgFromJoystick)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        #print(msgFromJoystick)
        #Run YOLO
        #dsize = (data.shape[0], data.shape[1])
        
        img_desired_width_pg = 500-40
        resized = image_resize(frame, img_desired_width_pg)
        pygame_image = convert_opencv_img_to_pygame(resized)
        screen.blit(pygame_image, (20,700-resized.shape[1]+90))
        """cv2.imshow('server', data) #to open image
        if cv2.waitKey(10) == 13:
            break"""

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
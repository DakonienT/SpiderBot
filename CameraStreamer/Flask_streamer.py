#Import necessary libraries
from xmlrpc.client import boolean
from flask import Flask, render_template, Response, request
import cv2
import logging
from datetime import datetime
import socket #to get IP
import psutil #to get res usage
import os
import numpy as np
import time

#Initialize the Flask app
app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

camera = cv2.VideoCapture(0)
logging.debug('Loading NN...')
net = cv2.dnn.readNetFromDarknet('yolov4-tiny.cfg', 'yolov4-tiny.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
logging.debug('NN Loaded !')
logging.debug('Loading COCO...')
classes = open('coco.names').read().strip().split('\n')
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')
logging.debug('COCO Loaded !')

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]



scale_percent = 120#Scale percent to reseize frames
pid = os.getpid() #Get PID of the program
logging.debug("PID : %s", str(pid))
def getRes():
    CPU = psutil.cpu_percent()
    VMem = dict(psutil.virtual_memory()._asdict())
    VMemPercent = psutil.virtual_memory().percent
    AvMem = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    PSPID = psutil.Process(pid)
    CPUForCurr = PSPID.cpu_percent
    stringRet ="PID : " + str(pid) + "\n"+ "CPU : " + str(CPU) + "\n" + "Virtual Memory : " + str(VMemPercent) + "\n" + "Available mMemory : " + str(AvMem) + "\n" + "Current CPU use for process : " + str(CPUForCurr) + "\n"
    
    return CPU, VMemPercent, AvMem, CPUForCurr


def YOLO(frame, dsize):
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
            if confidence > 0.5:
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
            color = [int(c) for c in colors[classIDs[i]]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame

def gen_frames():  
    global record
    record = False
    # used to record the time when we processed last frame
    prev_frame_time = 0
    
    # used to record the time at which we processed current frame
    new_frame_time = 0
    while True:
        success, frame = camera.read()  # read the camera frame

        #Resize the frame
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dsize = (width, height)
        frame = cv2.resize(frame, dsize)

        #YoLo
        frame = YOLO(frame, dsize)
        #Put date & time        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        frame = cv2.putText(frame, dt_string, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2,cv2.LINE_AA)

        #Calculate FPS
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)

        #Get process DATA
        cv2.putText(frame, "PID : " + str(pid), (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1,cv2.LINE_AA)
        cv2.putText(frame, "CPU : " + str(getRes()[0]) + "%", (10,95), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1,cv2.LINE_AA)
        cv2.putText(frame, "Virtual Memory : " + str(getRes()[1]) + "%", (10,110), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1,cv2.LINE_AA)
        cv2.putText(frame, "CPU For process : " + str(getRes()[2]) + "%", (10,125), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1,cv2.LINE_AA)
        cv2.putText(frame, "FPS : " + fps, (10,140), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1,cv2.LINE_AA)
        #print(getRes())
        #Record
        
        if(record):
            
            
            cv2.circle(frame, (80,80), 30, (0,255,0),-1)
        else:
            pass
        if not success:
            break
            logging.error("Error : can not get image ! ")
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        if request.form.get('Start recording') == 'Start recording':
            record = True
            logging.info("Start recording")
        elif request.form.get('Stop recording')== 'Stop recording':
            record = False
            logging.info("Stop recording...")
        else:
            pass
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    logging.info("Hostname : %s", hostname)
    logging.info("IP : %s", IPAddr)
    logging.info("Loading FLASK appliction...")
    app.run(debug=False,host=IPAddr)
    logging.info("Server ready !")
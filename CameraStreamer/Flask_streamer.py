#Import necessary libraries
from xmlrpc.client import boolean
from flask import Flask, render_template, Response, request
import cv2
import logging
from datetime import datetime
import socket

#Initialize the Flask app
app = Flask(__name__)
camera = cv2.VideoCapture(0)
scale_percent = 100

def gen_frames():  
    global record
    record = False
    while True:
        success, frame = camera.read()  # read the camera frame

        #Resize the frame
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dsize = (width, height)
        frame = cv2.resize(frame, dsize)

        #Put date & time        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        frame = cv2.putText(frame, dt_string, (30,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2,cv2.LINE_AA)

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
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)
    logging.info("Hostname : %s", hostname)
    logging.info("IP : %s", IPAddr)
    logging.info("Loading FLASK appliction...")
    app.run(debug=False,host=IPAddr)
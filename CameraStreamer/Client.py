import cv2
import socket 
import pickle
import os
import yaml
from yaml.loader import SafeLoader  
import logging
import numpy as np
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
serverip="127.0.0.1"
serverport=6666
cap = cv2.VideoCapture(0)
logging.basicConfig(format='%(asctime)s %(message)s')
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)
count = 0 #Frames counter
count_sent = 0
#camera_matrix = np.array([0,0,0],[0,0,0],[0,0,0])
#dist_coeff = np.array([0,0,0],[0,0,0],[0,0,0])

with open(r'C:\Users\simon\Desktop\VMShared\SpiderBot\calibration_matrix.yaml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    camera_matrix = np.array(data["camera_matrix"])
    dist_coeff = np.array(data["dist_coeff"])

    print( "Camera Matrix : " + str(camera_matrix))
    width = 640
    height = 480
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeff, (width, height), 1, (width, height))
    mapx,mapy = cv2.initUndistortRectifyMap(camera_matrix,dist_coeff,None,newcameramtx,(width,height),5)

    while True:    
        ret,photo = cap.read()
        h, w = photo.shape[:2]    
        print("(w, h) = (" + str(w) + ", " + str(h) +")")
        #cv2.imshow('streaming', photo)    
        #dst = cv2.remap(photo,mapx,mapy,cv2.INTER_LINEAR)
        dst = cv2.undistort(photo, camera_matrix, dist_coeff, None, newcameramtx)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        ret, buffer = cv2.imencode(".jpg", dst,[int(cv2.IMWRITE_JPEG_QUALITY),70])    
        x_as_bytes = pickle.dumps(buffer)    
        count +=1
        try:

            s.sendto(x_as_bytes,(serverip , serverport))
            count_sent += 1 #Increment counter
        except:
            pass
        logging.debug(str(count_sent) + "/" + str(count) + " Images sent to " + serverip + ":" + str(serverport))
        if cv2.waitKey(10) == 13:        
            
            break  
cv2.destroyAllWindows()
cap.release()
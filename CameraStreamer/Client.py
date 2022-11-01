import cv2, socket, pickle, os  
import logging
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
while True:    
    ret,photo = cap.read()    
    
    #cv2.imshow('streaming', photo)    
    
    ret, buffer = cv2.imencode(".jpg", photo,[int(cv2.IMWRITE_JPEG_QUALITY),70])    
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
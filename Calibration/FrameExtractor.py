import cv2

# Opens the Video file
cap= cv2.VideoCapture('Calibration.mp4')
i=0
print("Ok")
if(cap.isOpened() == False):
    print("Error while opening video")
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    print("Extracting  frame #"+str(i))
    cv2.imwrite('images\kang'+str(i)+'.jpg',frame)
    i+=1

cap.release()
cv2.destroyAllWindows()
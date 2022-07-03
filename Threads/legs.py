from time import sleep
from threading import Thread
import random

class leg:
    def __init__(self) -> None:
        self.rotation_servo_angle = 90 #The servo to go forward and backward
        self.elbow_servo_angle = 45 #The mid servo
        self.wrist_servo_angle = 45 # The last servo
        #Set channels for servos
        self.rotation_servo_channel = 1
        self.elbow_servo_channel = 2
        self.wrist_servo_channel =3

    def writeServos(self):
         #For now let's replace the real code by print
         print ("Writing rotation_servo_angle as " + str(self.rotation_servo_angle))
         print ("Writing elbow_servo_angle as " + str(self.elbow_servo_angle))
         print ("Writing wrist_servo_angle as " + str(self.wrist_servo_angle))

def legsUpdateThread(legs):
    while True:
        # block for a moment
        #sleep(1)
        # display a message
        print('This is from another thread')
        legs.writeServos()
        sleep(0.5)

leg1 = leg()

thread = Thread(target=legsUpdateThread, args=(leg1,), daemon=True)
# run the thread
thread.start()
# wait for the thread to finish
while True:
    sleep(0.5)
    print('Waiting for the thread...')
    #leg1.elbow_servo_angle = random.randint(0,180)
    #leg1.elbow_servo_channel = random.randint(0,180)
    
    print(random.randint(0,180))
    leg1.wrist_servo_channel = random.randint(0,180)
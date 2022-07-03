#!/usr/bin/python
import time
#import RPi.GPIO as GPIO
from PCA9685 import PCA9685

try:
    print ("This is an PCA9685 routine")
    pwm = PCA9685()
    pwm.setPWMFreq(50)
    #pwm.setServoPulse(1,500) 
    pwm.setRotationAngle(1, 0)
    
    while True:
        # setServoPulse(2,2500)
        for i in range(30,90,1): 
            pwm.setRotationAngle(6, i)   
            if(i<80):
                pwm.setRotationAngle(6, i)   
            time.sleep(0.5)

        for i in range(90,30,-1): 
            pwm.setRotationAngle(6, i)   
            if(i<80):
                pwm.setRotationAngle(6, i)            
            time.sleep(0.5)

except:
    pwm.exit_PCA9685()
    print ("\nProgram end")
    exit()
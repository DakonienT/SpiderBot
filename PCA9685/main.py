#!/usr/bin/python
import time
from PCA9685 import PCA9685

try:
    print ("This is an PCA9685 routine")
    pwm = PCA9685()
    pwm.setPWMFreq(50)
    #pwm.setServoPulse(1,500) 
    pwm.setRotationAngle(1, 0)
    pwm.setRotationAngle(0, 50)
    pwm.setRotationAngle(0, 90)
    time.sleep(1)
    while True:
        # setServoPulse(2,2500)
        for i in range(1,100,1): 
            pwm.setRotationAngle(0, i)   
            time.sleep(0.01)

        for i in range(100,1,-1): 
            pwm.setRotationAngle(0, i)   
            time.sleep(0.01)

except:
    pwm.exit_PCA9685()
    print ("Program end")
    pwm.disable(0)
    exit()
import time
from PCA9685 import PCA9685

SERVO1_LEG = 0
SERVO2_LEG = 1
SERVO3_LEG = 2

try:
    print ("This is an PCA9685 routine")
    pwm = PCA9685()
    pwm.setPWMFreq(50)
    #pwm.setServoPulse(1,500)
    # First, set Servo 2 to horizontal position  and 3 to vertical 
    while True: 
        pwm.setRotationAngle(SERVO2_LEG, 85)
        pwm.setRotationAngle(SERVO3_LEG, 0)
        time.sleep(0.5)
        #Second, Set servo 1 to 45deg forward
        pwm.setRotationAngle(SERVO1_LEG, 45)
        time.sleep(0.5)
        #then get leg down
        pwm.setRotationAngle(SERVO2_LEG, 45)
        pwm.setRotationAngle(SERVO3_LEG, 45)
        time.sleep(0.5)
        #And move leg back
        pwm.setRotationAngle(SERVO1_LEG, 100)
        time.sleep(0.5)
    """ while True:
        # setServoPulse(2,2500)
        for i in range(1,100,1): 
            pwm.setRotationAngle(SERVO2_LEG, i)   
            time.sleep(0.01)

        for i in range(100,1,-1): 
            pwm.setRotationAngle(SERVO2_LEG, i)   
            time.sleep(0.01) """

except:
    pwm.exit_PCA9685()
    print ("Program end")
    pwm.disable(SERVO2_LEG)
    pwm.disable(SERVO1_LEG)
    pwm.disable(SERVO3_LEG)
    exit()
pwm.disable(SERVO2_LEG)
pwm.disable(SERVO3_LEG)
pwm.disable(SERVO1_LEG)
exit()
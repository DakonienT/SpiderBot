#include "Leg.h"

Leg::Leg(int Servo1, int Servo2, int Servo3)
{


    ServoLeg1.attach(Servo1);
    ServoLeg2.attach(Servo2);
    ServoLeg3.attach(Servo3);
}
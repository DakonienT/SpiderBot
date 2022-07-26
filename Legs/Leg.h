#include <Servo.h>

class Leg
{
public:
    Servo ServoLeg1;
    Servo ServoLeg2;
    Servo ServoLeg3;
    void Leg(int Servo1, int Servo2, int Servo3);
    int positions[3] = {90, 90, 90};
}
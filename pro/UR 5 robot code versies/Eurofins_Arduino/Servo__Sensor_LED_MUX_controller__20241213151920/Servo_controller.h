#ifndef Servo_controller_H
#define Servo_controller_H

#include <Servo.h>

void initialize_servo(); // set Servo pin.
void servo_on(); // Turn servo to 90 degrees.
void servo_off(); // Turn servo to 0 degrees.

#endif
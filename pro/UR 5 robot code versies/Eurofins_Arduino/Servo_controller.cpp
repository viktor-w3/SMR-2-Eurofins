//Servo_controller.cpp
#include "Servo_controller.h"
//#include <Arduino.h> // For Testing Purposes

Servo myservo;

void initialize_servo(){
myservo.attach(5);  // attaches the servo on pin 5 to the Servo object
}

void servo_on() {
  myservo.write(35); // Tell servo to go to position 90 degrees
  //Serial.println("Servo 90"); // For Testing Purposes
}
void servo_off() {
  myservo.write(0); // Tell servo to go to position 0 degrees
  //Serial.println("Servo 0"); // For Testing Purposes
}
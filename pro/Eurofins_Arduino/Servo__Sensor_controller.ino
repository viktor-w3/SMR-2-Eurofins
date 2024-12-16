/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/
// mux common is 10
// mux A B C is 6 7 8
// servo is pin 5
// led is pin 9
// test setup: IR1 = on MUX 0 = abc 0 0 0, IR2 =  on MUX 1 = abc 1 0 0
#include <Servo.h>
#include <FastLED.h>

#define NUM_LEDS 2
#define DATA_PIN 9

CRGB leds[NUM_LEDS];

Servo myservo;  // create Servo object to control a servo
// twelve Servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int sensor1state = 0;
const int sensor1pin = 10;
const int muxA = 6;
const int muxB = 7;
const int muxC = 8;
const int muxCOM = 10;

void setup() {
  Serial.begin(9600);
  myservo.attach(5);  // attaches the servo on pin 5 to the Servo object
  pinMode(muxCOM, INPUT);
  FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
  
}

void loop() {
  sensor1state = digitalRead(muxCOM);
  Serial.print(digitalRead(muxCOM));
  
  if (sensor1state == LOW){
  servo_on(); //Turns servo to On position
  leds[0] = CRGB::Red;
  leds[1] = CRGB::Black;
  FastLED.show();
  FastLED.setBrightness( 50);
  delay(1000); //test for function control
  } 
  else 
  {
  servo_off(); //Turns servo to Off position
  leds[0,1] = CRGB::Blue;
  FastLED.show();
  FastLED.setBrightness( 10 );
  delay(1000);
  }
}

void servo_on(){
    myservo.write(90);              // tell servo to go to position 90 degrees
}

void servo_off(){
    myservo.write(0);              // tell servo to go to position 0 degrees
}
/*Current setup README
Servo:
Servo data pin is attached to pin 5. To change, go to Servo_controller.cpp. Line 7. Change 'x' myservo.attach(x);

LEDs:
The amount of LED strips and the maximum amount of LEDs per LEDstrip can be defined.
  To change the amount of LEDstrips, go to LED_controller.h. Line 6. Change 'x' #define NUM_STRIPS x.
  To change the maximum amount of LEDs per strip, go to LED_controller.h. Line 7. Change 'x' #define MAX_NUM_LEDS 10.

Ledstrip data pins are set to pin 9, 10 and 11. 
  To change, go to Led_controller.cpp. Line 5. Chanage 'x, y, z' int dataPins[NUM_STRIPS] = {x, y, z};

Ledstrip amount of LEDs are set to 10, 10 and 9 LEDs (10 for strip 0, 10 for strip 1 and 9 for strip 2). 
  To change, go to Led_controller.cpp. Line 6. Chanage 'x, y, z' int numLeds[NUM_STRIPS] = {x, y, z};

MUX:


*/
// mux common is 10
// mux A B C is 6 7 8
// servo is pin 5
// led is pin 9
// test setup: IR1 = on MUX 0 = abc 0 0 0, IR2 =  on MUX 1 = abc 1 0 0

#include "Servo_controller.h"
#include "Led_controller.h"

int pos = 0;    // variable to store the servo position
int sensor1state = 0;
const int sensor1pin = 10;
const int muxA = 6;
const int muxB = 7;
const int muxC = 8;
const int muxCOM = 10;

void setup() {
  Serial.begin(9600);
  initialize_leds(); //initialize all LED strips.
  pinMode(muxCOM, INPUT);
  pinMode(muxA, OUTPUT);
  pinMode(muxB, OUTPUT);
  pinMode(muxC, OUTPUT);
}

/*Example code for LEDs:
initialize_leds(); //initialize all LED strips.
set_all_leds(CRGB::Red); //Set all LEDs to red
set_strip_leds(1,CRGB::Blue); // Set all LEDs on strip 1 to Blue
set_led(0 ,5 ,CRGB::Green); // Set led 5 (6th led, 0-based) on strip 0 to Green
load_bar(CRGB::Yellow,5000, 1) // Display a yellow loading bar on LED strip 1for 5 seconds
set_all_leds(CRGB::Black); // Turn off all LEDs
*/

void loop() {
  initialize_servo();
  servo_on();
  Serial.println("Servo on");
  delay (500);
  servo_off();
  Serial.println("Servo off");
  delay(500);
}
/*
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n'); // Lees de ontvangen opdracht
    command.trim(); // Verwijder overbodige spaties of nieuwe regels

    if (command == "LED_ON") {
      digitalWrite(LED_BUILTIN, HIGH); // Zet de ingebouwde LED aan
      Serial.println("LED turned on");
    } else if (command == "LED_OFF") {
      digitalWrite(LED_BUILTIN, LOW); // Zet de ingebouwde LED uit
      Serial.println("LED turned off");
    } else if (command == "SERVOtest0") {
    myservo.write(90); // Zet de servo op de gewenste hoek
    Serial.println("SERVOtest0 received");
    } else if (command == "SERVOtest1") {
    myservo.write(0); // Zet de servo op de gewenste hoek
    Serial.println("SERVOtest1 received");
    }
    else {
      Serial.println("Unknown command");
    }
  }
}
/*
/*
  mux0(); // Check if mux channel 0 has a signal
  if (digitalRead(muxCOM) == LOW) { // If signal is present (arduino is reversed)
    servo_on(); // Turns servo to On position
    leds[0] = CRGB::Red;
    FastLED.show();
    delay(1000); // Test for function control
  } else { // If no signal, turn off LED 0
    servo_off(); // Turns servo to Off position
    leds[0] = CRGB::Black;
    FastLED.show();
    delay(1000);
  }

  mux1(); // Check if mux channel 1 has a signal
  if (digitalRead(muxCOM) == LOW) {
    servo_on(); // Turns servo to On position
    leds[1] = CRGB::Red;
    FastLED.show();
    delay(1000); // Test for function control
  } else {
    servo_off(); // Turns servo to Off position
    leds[1] = CRGB::Black;
    FastLED.show();
    delay(1000);
  }
}

void servo_on() {
  myservo.write(90); // Tell servo to go to position 90 degrees
}

void servo_off() {
  myservo.write(0); // Tell servo to go to position 0 degrees
}

void mux0() {
  // Sets pins for mux channel 0
  digitalWrite(muxA, LOW);
  digitalWrite(muxB, LOW);
  digitalWrite(muxC, LOW);

  // Delay for updating pins
  delay(5);

  // Print muxCH0 = muxchannel 0 value (for testing)
  Serial.print("MUXCH0 = ");
  Serial.println(digitalRead(muxCOM));
}

void mux1() {
  // Sets pins for mux channel 1
  digitalWrite(muxA, HIGH);
  digitalWrite(muxB, LOW);
  digitalWrite(muxC, LOW);

  // Delay for updating pins
  delay(5);

  // Print muxCH1 = muxchannel 1 value (for testing)
  Serial.print("MUXCH1 = ");
  Serial.println(digitalRead(muxCOM));
}
*/

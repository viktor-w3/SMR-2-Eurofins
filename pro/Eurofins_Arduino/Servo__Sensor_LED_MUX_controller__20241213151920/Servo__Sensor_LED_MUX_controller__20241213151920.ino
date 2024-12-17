/*Current setup README
Servo:
Servo data pin is attached to pin 5. To change, go to Servo_controller.cpp. Line 7. Change 'x' myservo.attach(x);

LEDs:
The amount of LED strips and the maximum amount of LEDs per LEDstrip can be defined.
  To change the amount of LEDstrips, go to LED_controller.h. Line 6. Change 'x' #define NUM_STRIPS x.
  To change the maximum amount of LEDs per strip, go to LED_controller.h. Line 7. Change 'x' #define MAX_NUM_LEDS 10.

Ledstrip data pins are set to pin 9, 10 and 11. 
  To change, go to Led_controller.cpp. Line 5. Change 'x, y, z' int dataPins[NUM_STRIPS] = {x, y, z};

Ledstrip amount of LEDs are set to 10, 10 and 9 LEDs (10 for strip 0, 10 for strip 1 and 9 for strip 2). 
  To change, go to Led_controller.cpp. Line 6. Change 'x, y, z' int numLeds[NUM_STRIPS] = {x, y, z};

MUX:
The multiplexer channel selection pins are all connected to i/o channels 6, 7 and 8.
  To change, go to Multiplexer_control.cpp. Line 5, 6 and 7. Change 'x ,y ,z' Multiplexer mux1(x, y, z, -);
Multiple multiplexers can be connected to the Arduino. At minimum, all multiplexers MUST have a seperate i/o pin for their common output.
  To change the common output pin, go to Multiplexer_control.cpp. Line 5, 6 and 7. Change 'x' Multiplexer mux1(-, -, -, x);
  To add a new multiplexer, go to Multiplexer_control.cpp. Line 5, 6 and 7. Copy: 'Multiplexer muxA(-, -, -, -);' and change 'A' to the multiplexer identification number (1, 2, 3 ... etc.)

*/

// mux1 common is 2
// mux2 common is 3
// mux3 common is 4
// mux A B C is 6 7 8

// servo is pin 5

// led data is pin 9

// test setup: IR1 = on MUX 0 = abc 0 0 0, IR2 =  on MUX 1 = abc 1 0 0

/*Example code for LEDs:
  initialize_leds(); //initialize all LED strips.
  set_all_leds(CRGB::Red); //Set all LEDs to red
  set_strip_leds(1,CRGB::Blue); // Set all LEDs on strip 1 to Blue
  set_led(0 ,5 ,CRGB::Green); // Set led 5 (6th led, 0-based) on strip 0 to Green
  load_bar(CRGB::Yellow,5000, 1) // Display a yellow loading bar on LED strip 1for 5 seconds
  set_all_leds(CRGB::Black); // Turn off all LEDs
*/

/*Example code for Multiplexers:
  readMultiplexer(mux1);              // Read Multiplexer 1
  readMuxChannel(mux1, 2);            // Read channel 2 of Multiplexer 2
*/

#include "Servo_controller.h"     // Include the servo controller header
#include "Led_controller.h"       // Include the LED controller header
#include "Multiplexer_control.h"  // Include the multiplexer control header

void setup() {
    Serial.begin(9600);           // Begin serial communication at 9600 baud
    initialize_leds();            // Initialize all LED strips
    initialize_servo();           // Set up servo pins and initial position
}

void loop() {
    // Check if a command is available via the serial interface
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n'); // Read the incoming command
        command.trim();                                // Remove leading/trailing whitespace
        processCommand(command);                      // Process the received command
    }
}

void processCommand(String command) {
    if (command == "initialize_servo") {
        // Reinitialize the servo
        initialize_servo();
        delay(100);              // Allow time for reinitialization
        Serial.println("done");  // Confirm the action is complete
    } else if (command == "servo_on") {
        // Move servo to the "on" position (90 degrees)
        servo_on();
        delay(500);              // Allow time for the servo to move
        Serial.println("done");  // Confirm the action is complete
    } else if (command == "servo_off") {
        // Move servo to the "off" position (0 degrees)
        servo_off();
        delay(500);              // Allow time for the servo to move
        Serial.println("done");  // Confirm the action is complete
    } else if (command == "initialize_leds") {
        // Reinitialize the LED strips
        initialize_leds();
        delay(100);              // Allow time for reinitialization
        Serial.println("done");  // Confirm the action is complete
    } else if (command.startsWith("set_all_leds")) {
        // Set all LEDs to the specified color
        String color = command.substring(13); // Extract the color name from the command
        if (color == "Red") {
            set_all_leds(CRGB::Red);          // Set all LEDs to red
        }
        delay(100);              // Allow time for the LEDs to update
        Serial.println("done");  // Confirm the action is complete
    } else if (command.startsWith("set_strip_leds")) {
        // Set all LEDs in a specific strip to the specified color
        int stripIndex = command.charAt(14) - '0'; // Get the strip index from the command
        String color = command.substring(16);     // Extract the color name from the command
        if (color == "Blue") {
            set_strip_leds(stripIndex, CRGB::Blue); // Set the strip LEDs to blue
        }
        delay(100);              // Allow time for the LEDs to update
        Serial.println("done");  // Confirm the action is complete
    } else if (command.startsWith("set_led")) {
        // Set a specific LED on a strip to the specified color
        int stripIndex = command.charAt(8) - '0';  // Get the strip index from the command
        int ledIndex = command.charAt(10) - '0';   // Get the LED index from the command
        String color = command.substring(12);     // Extract the color name from the command
        if (color == "Green") {
            set_led(stripIndex, ledIndex, CRGB::Green); // Set the LED to green
        }
        delay(100);              // Allow time for the LED to update
        Serial.println("done");  // Confirm the action is complete
    } else if (command.startsWith("load_bar")) {
        // Execute a loading bar animation on a strip
        String params = command.substring(9);             // Extract the parameters from the command
        int firstSpace = params.indexOf(' ');             // Find the first space
        int secondSpace = params.indexOf(' ', firstSpace + 1); // Find the second space
        String colorName = params.substring(0, firstSpace); // Extract the color name
        unsigned long duration = params.substring(firstSpace + 1, secondSpace).toInt(); // Extract duration
        int stripIndex = params.substring(secondSpace + 1).toInt(); // Extract strip index
        CRGB color = (colorName == "Yellow") ? CRGB::Yellow : CRGB::Black; // Map color name to CRGB value
        load_bar(color, duration, stripIndex); // Execute the loading bar animation
    } else {
        // Handle unknown commands
        Serial.println("Unknown command"); // Inform the user about the unrecognized command
    }
}


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
//main.ino
/* Include all function files */
#include "Servo_controller.h"     // Include the servo controller header
#include "Led_controller.h"       // Include the LED controller header
#include "Multiplexer_control.h"  // Include the multiplexer control header

/*Set default settings*/
void setup() {
    Serial.begin(9600);           // Begin serial communication at 9600 baud
    initialize_leds();            // Initialize all LED strips
    initialize_servo();           // Set up servo pins and initial position
}

/*Communicate with Python*/
void loop() {
    // Check if a command is available via the serial interface
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n'); // Read the incoming command
        command.trim();                                // Remove leading/trailing whitespace
        processCommand(command);                      // Process the received command
    }
    //readMuxChannel(mux2, 2);
    //readMultiplexer(mux1);
}

/*List of ALL command calls of Python for the Arduino*/
void processCommand(String command) {
    
    /*Servo Controlls*/
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
    /*Mux controls*/
    }else if (command == "read_mux0") {
        readMultiplexer(mux0); // Read all channels of mux1
        delay(100);
        Serial.println("done"); // Confirm the action is complete
    } else if (command == "read_mux1") {
        readMultiplexer(mux1); // Read all channels of mux2
        delay(100);
        Serial.println("done");
    } else if (command == "read_mux2") {
        readMultiplexer(mux2); // Read all channels of mux3
        delay(100);
        Serial.println("done");
    } else if (command.startsWith("read_mux_channel")) {
        // Example command format: "read_mux_channel 1 2" to read mux2 channel 2
        int spaceIndex = command.indexOf(' ');
        int muxIndex = command.substring(spaceIndex + 1, spaceIndex + 2).toInt(); // Mux number
        int channelIndex = command.substring(spaceIndex + 3).toInt(); // Channel number
        
        if (muxIndex == 0) {
            readMuxChannel(mux0, channelIndex);
            delay(100);
        } else if (muxIndex == 1) {
            readMuxChannel(mux1, channelIndex);
            delay(100);
        } else if (muxIndex == 2) {
            readMuxChannel(mux2, channelIndex);
            delay(100);
        }
        Serial.println("done");
        
    /*LED Controlls*/
    } else if (command == "initialize_leds") {
        // Initialize the LED strips
        initialize_leds();
        delay(100);              // Allow time for reinitialization
        Serial.println("done");  // Confirm the action is complete

    } else if (command.startsWith("set_all_leds")) {
      // Extract and log color
      String color = command.substring(13);
      Serial.println("Received color: " + color);  // Debugging
      CRGB ledColor = parseColor(color);
      set_all_leds(ledColor);
      Serial.println("done");

    } else if (command.startsWith("set_strip_leds")) {
        // Set all LEDs in a specific strip to the specified color
        int stripIndex = command.charAt(14) - '0';
        String color = command.substring(16);
        CRGB ledColor = parseColor(color);
        set_strip_leds(stripIndex, ledColor);
        delay(100);
        Serial.println("done");

    } else if (command.startsWith("set_led_range")) {
        // Stel een reeks LEDs in op een specifieke strip
        String params = command.substring(14);
        int firstSpace = params.indexOf(' ');
        int secondSpace = params.indexOf(' ', firstSpace + 1);
        int thirdSpace = params.indexOf(' ', secondSpace + 1);
        int stripIndex = params.substring(0, firstSpace).toInt();
        int startLed = params.substring(firstSpace + 1, secondSpace).toInt();
        int endLed = params.substring(secondSpace + 1, thirdSpace).toInt();
        String colorName = params.substring(thirdSpace + 1);
        CRGB color = parseColor(colorName);
        set_led_range(stripIndex, startLed, endLed, color);
        delay(100);              // Allow time for the LEDs to update
        Serial.println("done");  // Confirm the action is complete

    } else if (command.startsWith("load_bar_range")) {
        // Command format: "load_bar_range color duration stripIndex startIndex endIndex"
        String params = command.substring(15);
        int firstSpace = params.indexOf(' ');
        int secondSpace = params.indexOf(' ', firstSpace + 1);
        int thirdSpace = params.indexOf(' ', secondSpace + 1);
        int fourthSpace = params.indexOf(' ', thirdSpace + 1);

        String color = params.substring(0, firstSpace);
        unsigned long duration = params.substring(firstSpace + 1, secondSpace).toInt();
        int stripIndex = params.substring(secondSpace + 1, thirdSpace).toInt();
        int startIndex = params.substring(thirdSpace + 1, fourthSpace).toInt();
        int endIndex = params.substring(fourthSpace + 1).toInt();

        CRGB crgbColor = parseColor(color);
        load_bar_range(crgbColor, duration, stripIndex, startIndex, endIndex);
       
        delay(100);
        Serial.println("done");

    } else if (command.startsWith("blink")) {
        String params = command.substring(6);
        int firstSpace = params.indexOf(' ');
        String type = params.substring(0, firstSpace);
        params = params.substring(firstSpace + 1);

        if (type == "single") {
            int stripIndex = params.substring(0, params.indexOf(' ')).toInt();
            int ledIndex = params.substring(params.indexOf(' ') + 1, params.lastIndexOf(' ')).toInt();
            String colorName = params.substring(params.lastIndexOf(' ') + 1);
            int speed = params.substring(params.lastIndexOf(' ') + 1).toInt();

            CRGB color = parseColor(colorName);
            blink_single_led(stripIndex, ledIndex, color, speed);

        } else if (type == "all") {
            int stripIndex = params.substring(0, params.indexOf(' ')).toInt();
            String colorName = params.substring(params.indexOf(' ') + 1, params.lastIndexOf(' '));
            int speed = params.substring(params.lastIndexOf(' ') + 1).toInt();

            CRGB color = parseColor(colorName);
            blink_all_leds_on_strip(stripIndex, color, speed);

        } else if (type == "range") {
            int stripIndex = params.substring(0, params.indexOf(' ')).toInt();
            params = params.substring(params.indexOf(' ') + 1);
            int startLed = params.substring(0, params.indexOf(' ')).toInt();
            params = params.substring(params.indexOf(' ') + 1);
            int endLed = params.substring(0, params.indexOf(' ')).toInt();
            String colorName = params.substring(params.indexOf(' ') + 1, params.lastIndexOf(' '));
            int speed = params.substring(params.lastIndexOf(' ') + 1).toInt();

            CRGB color = parseColor(colorName);
            blink_led_range(stripIndex, startLed, endLed, color, speed);
        }
        delay(100);
        Serial.println("done");

    } else {
        Serial.println("Unknown command");
    }
}

CRGB parseColor(String colorName) {
    if (colorName == "Red") return CRGB::Red;
    if (colorName == "Green") return CRGB::Green;
    if (colorName == "Blue") return CRGB::Blue;
    if (colorName == "Yellow") return CRGB::Yellow;
    return CRGB::Black;  // Default to Black
}


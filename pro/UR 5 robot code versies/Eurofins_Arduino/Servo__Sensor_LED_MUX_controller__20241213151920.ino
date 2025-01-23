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
  set_led_range(1, 5, 10, Red); // Display Red LEDS on Ledstrip 1 on LED 5 to 10.
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
        //Serial.print("Received command: "); // Debugging print
        //Serial.println(command); // Show the received command
        command.trim();                                // Remove leading/trailing whitespace
        processCommand(command);                      // Process the received command
    }
}

/* Process commands */
void processCommand(String command) {
  command.trim();  // Trim leading/trailing whitespace

    if (command.startsWith("initialize_")) {
        if (command == "initialize_servo") {
            initialize_servo();
        } else if (command == "initialize_leds") {
            initialize_leds();
        }
        Serial.println("done");
    } else if (command.startsWith("servo_")) {
        handleServoCommand(command);
    } else if (command.startsWith("read_mux_channel")) {
        handleMuxCommand(command);
    } else if (command.startsWith("set_led_range")) {
        handleSetLedRange(command);
    } else if (command.startsWith("load_bar_range")) {
        handleLoadBarRange(command);
    } else if (command.startsWith("blink")) {
        handleBlinkCommand(command);
    } else if (command.startsWith("set_all_leds")) {
        handleSetAllLeds(command);
    } else {
        Serial.println("Unknown command");
    }
}

void handleSetAllLeds(String command) {
    // Extract the color from the command
    String colorName = getCommandParam(command, 1);
    CRGB color = parseColor(colorName);

    // Set all LEDs to the parsed color
    set_all_leds(color);

    delay(100);  // Optional delay for stability
    Serial.println("done");
}

/* Servo-related commands */
void handleServoCommand(String command) {
    if (command == "servo_on") {
        servo_on();
    } else if (command == "servo_off") {
        servo_off();
    }
    delay(500);
    Serial.println("done");
}

void handleMuxCommand(String command) {
    int muxIndex = getCommandParam(command, 1).toInt();
    int channelIndex = getCommandParam(command, 2).toInt();
    if (muxIndex == 0) {
        readMuxChannel("MUX0", mux0, channelIndex);
    } else if (muxIndex == 1) {
        readMuxChannel("MUX1", mux1, channelIndex);
    } else if (muxIndex == 2) {
        readMuxChannel("MUX2", mux2, channelIndex);
    }
    Serial.println("done");
}

/* Handle LED range setting */
void handleSetLedRange(String command) {
    int stripIndex = getCommandParam(command, 1).toInt();
    int startLed = getCommandParam(command, 2).toInt();
    int endLed = getCommandParam(command, 3).toInt();
    String colorName = getCommandParam(command, 4);
    CRGB color = parseColor(colorName);
    set_led_range(stripIndex, startLed, endLed, color);
    delay(100);
    Serial.println("done");
}

/* Handle load bar range */
void handleLoadBarRange(String command) {
    // Extract parameters from the command string
    String color = getCommandParam(command, 1);  // Color as string (e.g., "Red")
    unsigned long duration = getCommandParam(command, 2).toInt();  // Duration
    int stripIndex = getCommandParam(command, 3).toInt();  // Strip index
    int startIndex = getCommandParam(command, 4).toInt();  // Start LED index
    int endIndex = getCommandParam(command, 5).toInt();  // End LED index
    
    // Convert color name to CRGB object using parseColor
    CRGB crgbColor = parseColor(color);
    
    // Debugging: Print the parsed color for confirmation
    Serial.print("Received color: ");
    Serial.println(color);
    Serial.print("Parsed RGB color: ");
    Serial.print(crgbColor.r);
    Serial.print(", ");
    Serial.print(crgbColor.g);
    Serial.print(", ");
    Serial.println(crgbColor.b);

    // Call the load_bar_range function with the parsed parameters
    load_bar_range(crgbColor, duration, stripIndex, startIndex, endIndex);
    
    // Brief delay to ensure the command completes
    delay(100);
    
    // Confirm the completion of the command
    Serial.println("done");
}

/* Handle blink commands */
void handleBlinkCommand(String command) {
    String type = getCommandParam(command, 1);
    int stripIndex = getCommandParam(command, 2).toInt();
    if (type == "range") {
        int startLed = getCommandParam(command, 3).toInt();
        int endLed = getCommandParam(command, 4).toInt();
        String colorName = getCommandParam(command, 5);
        int speed = getCommandParam(command, 6).toInt();
        blink_led_range(stripIndex, startLed, endLed, parseColor(colorName), speed);
    }
    delay(100);
    Serial.println("done");
}

/* Parse the color name and return corresponding CRGB object */
CRGB parseColor(String colorName) {
    // Map the color name to corresponding CRGB value
    if (colorName == "Red") {
        return CRGB::Red;
    } else if (colorName == "Green") {
        return CRGB::Green;
    } else if (colorName == "Blue") {
        return CRGB::Blue;
    } else if (colorName == "Yellow") {
        return CRGB::Yellow;
    } else if (colorName == "White") {
        return CRGB::White;
    } else if (colorName == "Purple") {
        return CRGB::Purple;
    } else if (colorName == "Orange") {
        return CRGB::Orange;
    } else {
        // Default to black if color is not recognized
        return CRGB::Black;
    }
}

/* Helper function to extract parameters using commas */
String getCommandParam(String command, int paramIndex) {
    // Ensure the command is properly split into parameters
    int spaceIndex1 = command.indexOf(' ');
    int spaceIndex2;
    for (int i = 1; i < paramIndex; i++) {
        spaceIndex2 = command.indexOf(' ', spaceIndex1 + 1);
        spaceIndex1 = spaceIndex2;
    }
    spaceIndex2 = command.indexOf(' ', spaceIndex1 + 1);
    
    if (spaceIndex2 == -1) { // no more spaces, last parameter
        return command.substring(spaceIndex1 + 1);
    } else {
        return command.substring(spaceIndex1 + 1, spaceIndex2);
    }
}
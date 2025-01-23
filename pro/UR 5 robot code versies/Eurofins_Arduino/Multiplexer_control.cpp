//Multiplexer_Control.cpp
#include "Multiplexer_control.h"

// Define the Multiplexer instances with their respective pins
// All multiplexers share the same select pins (A, B, C) connected to Arduino pins 6, 7, and 8
Multiplexer mux0(6, 7, 8, 2); // Multiplexer 1: Output pin -> Arduino pin 2
Multiplexer mux1(6, 7, 8, 3); // Multiplexer 2: Output pin -> Arduino pin 3
Multiplexer mux2(6, 7, 8, 4); // Multiplexer 3: Output pin -> Arduino pin 4

// Constructor: initialize the multiplexer to the pins
Multiplexer::Multiplexer(int pinA, int pinB, int pinC, int outputPin)
    : _pinA(pinA), _pinB(pinB), _pinC(pinC), _outputPin(outputPin) {
    pinMode(_pinA, OUTPUT);
    pinMode(_pinB, OUTPUT);
    pinMode(_pinC, OUTPUT);
    pinMode(_outputPin, INPUT);
}

// Select the channel by setting the binary address to A, B, C.
void Multiplexer::selectChannel(int channel) {
    digitalWrite(_pinA, bitRead(channel, 0)); // LSB
    digitalWrite(_pinB, bitRead(channel, 1));
    digitalWrite(_pinC, bitRead(channel, 2)); // MSB
}

// Read the value of the selected channel
int Multiplexer::readChannel() {
    return digitalRead(_outputPin);
}

// Read all channels of the specified multiplexer and print values
void readMultiplexer(const char* muxName, Multiplexer& mux) {
    for (int channel = 0; channel < 8; channel++) {
        mux.selectChannel(channel);        // Select the current channel
        int value = mux.readChannel();     // Read the value of the current channel
        //Serial.print("Multiplexer ");
        //Serial.print(muxName);             // Print the multiplexer name
        //Serial.print(" - Channel ");
        //Serial.print(channel);             // Print the channel number
        //Serial.print(": ");
        Serial.println(value);             // Print the read value (1 or 0)
        delay(100);                        // Small delay for readability
    }
}


// Read a specific channel from the specified multiplexer and print its value
void readMuxChannel(const char* muxName, Multiplexer& mux, int channel) {
    mux.selectChannel(channel);           // Select the specific channel
    delay(50);                            // Delay to ensure proper selection (can be optimized)
    int value = mux.readChannel();        // Read the value of the specified channel
    //Serial.print("Multiplexer ");
    //Serial.print(muxName);                // Print the multiplexer name
    //Serial.print(" - Channel ");
    //Serial.print(channel);                // Print the channel number
    //Serial.print(": ");
    Serial.println(value);                // Print the value of the channel (1 or 0)
    delay(100);                           // Small delay for readability
}

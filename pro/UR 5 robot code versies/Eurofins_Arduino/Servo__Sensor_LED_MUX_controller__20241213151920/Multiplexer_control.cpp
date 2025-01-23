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

// Utility Function: Read All Channels of a Multiplexer and Print the Data
void readMultiplexer(Multiplexer& mux) {
    for (int channel = 0; channel < 8; channel++) {
        mux.selectChannel(channel); // Select the current channel
        int value = mux.readChannel(); // Read the value of the current channel
        Serial.print("Multiplexer Channel ");
        Serial.print(channel);
        Serial.print(": ");
        Serial.println(value); // Print the value of the current channel
        delay(100);
    }
}

// Utility Function: Read a Specific Channel of a Multiplexer and Print the Data
void readMuxChannel(Multiplexer& mux, int channel) {
    mux.selectChannel(channel); // Select the specified channel
    int value = mux.readChannel(); // Read the value of the specified channel
    Serial.print("Multiplexer Channel ");
    Serial.print(channel);
    Serial.print(": ");
    Serial.println(value); // Print the value of the selected channel
    delay(100);
}

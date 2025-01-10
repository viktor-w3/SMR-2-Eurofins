//Multiplexer_control.h
#ifndef Multiplexer_control_H
#define Multiplexer_control_H

#include <Arduino.h>

// Multiplexer Class Definition
class Multiplexer {
public:
    // Constructor: Initializes the multiplexer with specified pins
    // pinA, pinB, pinC are address line pins, outputPin is where the multiplexer output is connected
    Multiplexer(int pinA, int pinB, int pinC, int outputPin); 

    // Selects a specific channel (0-7)
    void selectChannel(int channel);

    // Reads the value from the selected channel (1 or 0)
    int readChannel();

private:
    int _pinA;
    int _pinB;
    int _pinC;
    int _outputPin;
};

// External Multiplexer Instances
extern Multiplexer mux0;
extern Multiplexer mux1;
extern Multiplexer mux2;

// Function to read all channels of a given multiplexer and print their values
void readMultiplexer(const char* muxName, Multiplexer& mux);

// Function to read a specific channel of a given multiplexer and print the value
void readMuxChannel(const char* muxName, Multiplexer& mux, int channel);

#endif

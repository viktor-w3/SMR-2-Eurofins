#ifndef Multiplexer_control_H
#define Multiplexer_control_H

#include <Arduino.h>

// Multiplexer Class Definition
class Multiplexer {
public:
    // Constructor: Initializes the multiplexer with specified pins
    Multiplexer(int pinA, int pinB, int pinC, int outputPin); //Initialize the pins of the multiplexer
    // Selects a specific channel (0-7)
    void selectChannel(int channel);
    // Reads the value from the selected channel
    int readChannel();

private:
    int _pinA;
    int _pinB;
    int _pinC;
    int _outputPin;
};

// External Multiplexer Instances
extern Multiplexer mux1;
extern Multiplexer mux2;
extern Multiplexer mux3;

// Function to read the complete Multiplexer and print data for all channels
void readMultiplexer(Multiplexer& mux);

// Function to read a specific channel of a Multiplexer and print its data
void readMuxChannel(Multiplexer& mux, int channel);

#endif

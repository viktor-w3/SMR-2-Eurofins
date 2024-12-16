#ifndef Led_controller_H
#define Led_controller_H

#include <FastLED.h>

#define NUM_STRIPS 3         // Number of LED strips (adjust this to match your setup)
#define MAX_NUM_LEDS 10  // Define the maximum number of LEDs in any strip

extern int numLeds[NUM_STRIPS]; // Array to store the number of LEDs for each strip
extern int dataPins[NUM_STRIPS]; // Array of data pins for each strip
extern CRGB leds[NUM_STRIPS][MAX_NUM_LEDS]; // Array to hold LED data for each strip

void initialize_leds();  // Initialize all LED strips
void set_all_leds(CRGB color);  // Set all LED strips to a color
void set_strip_leds(int stripIndex, CRGB color);  // Set individual strip LEDs to a color
void set_led(int stripIndex, int ledIndex, CRGB color);  // Set an individual LED on a specific strip
void load_bar(CRGB color, unsigned long duration, int stripIndex);  // Function to display a load bar
/*
Not required, FastLED.h already handles this.
void deinitialize_leds();  // Deinitialize and free memory // use after LEDs are done with everything.
*/
#endif

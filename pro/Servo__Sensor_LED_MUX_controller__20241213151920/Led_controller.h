//led_controller.h
#ifndef Led_controller_H
#define Led_controller_H

#include <FastLED.h>

// Configuration for LED strips
#define NUM_STRIPS  4              // Number of LED strips
#define MAX_NUM_LEDS 30            // Maximum number of LEDs per strip

// Pin assignments
#define DATA_PIN_1 9
#define DATA_PIN_2 10
#define DATA_PIN_3 11
#define DATA_PIN_4 12

// Global variables
extern int numLeds[NUM_STRIPS];                // Number of LEDs per strip
extern int dataPins[NUM_STRIPS];               // Data pins for each strip
extern CRGB leds[NUM_STRIPS][MAX_NUM_LEDS];    // LED data for each strip

// Function prototypes
void initialize_leds();                                  // Initialize all LED strips
void set_all_leds(CRGB color);                          // Set all LED strips to a single color
void blink_led_range(int stripIndex, int startLed, int endLed, CRGB color, int speed);  // Blink a range of LEDs
void load_bar_range(CRGB color, unsigned long duration, int stripIndex, int startIndex, int endIndex);  // Load bar animation
void set_led_range(int stripIndex, int startLed, int endLed, CRGB color);  // Set a range of LEDs to a color

#endif

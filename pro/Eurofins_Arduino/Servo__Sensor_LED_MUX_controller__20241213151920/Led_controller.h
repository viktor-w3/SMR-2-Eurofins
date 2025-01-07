//led_controller.h
#ifndef Led_controller_H
#define Led_controller_H

#include <FastLED.h>

#define NUM_STRIPS  3        // Number of LED strips (adjust this to match your setup)
#define MAX_NUM_LEDS 30  // Define the maximum number of LEDs in any strip

#define DATA_PIN_1 9
#define DATA_PIN_2 10
#define DATA_PIN_3 11

extern int numLeds[NUM_STRIPS]; // Array to store the number of LEDs for each strip
extern int dataPins[NUM_STRIPS]; // Array of data pins for each strip
extern CRGB leds[NUM_STRIPS][MAX_NUM_LEDS]; // Array to hold LED data for each strip

void initialize_leds();  // Initialize all LED strips
void set_all_leds(CRGB color);  // Set all LED strips to a color
void set_strip_leds(int stripIndex, CRGB color);  // Set individual strip LEDs to a color
void set_led(int stripIndex, int ledIndex, CRGB color);  // Set an individual LED color
void blink_all_leds_on_strip(int stripIndex, CRGB color, int speed);  // Blink all LEDs on a strip
void blink_single_led(int stripIndex, int ledIndex, CRGB color, int speed);  // Blink a single LED
void blink_led_range(int stripIndex, int startLed, int endLed, CRGB color, int speed);  // Blink a range of LEDs
void load_bar_range(CRGB color, unsigned long duration, int stripIndex, int startIndex, int endIndex);  // Load bar animation
void set_led_range(int stripIndex, int startLed, int endLed, CRGB color);
/*
Not required, FastLED.h already handles this.
void deinitialize_leds();  // Deinitialize and free memory // use after LEDs are done with everything.
*/
#endif

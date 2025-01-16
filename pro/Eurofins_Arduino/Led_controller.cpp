//Led_controller.cpp
#include "Led_controller.h"

CRGB leds[NUM_STRIPS][MAX_NUM_LEDS];  // Array to hold LED data for each strip

int dataPins[NUM_STRIPS] = {9, 10, 11};  // Adjust the data pins according to your setup
int numLeds[NUM_STRIPS] = {30, 30, 30};  // Example: 30 LEDs on each strip

/* Initialization (Default settings) */
void initialize_leds() {
    for (int i = 0; i < NUM_STRIPS; i++) {
        // Initialize each LED strip separately
        if (i == 0) {
            FastLED.addLeds<WS2812B, DATA_PIN_1, RGB>(leds[i], numLeds[i]);
        } else if (i == 1) {
            FastLED.addLeds<WS2812B, DATA_PIN_2, RGB>(leds[i], numLeds[i]);
        } else if (i == 2) {
            FastLED.addLeds<WS2812B, DATA_PIN_3, RGB>(leds[i], numLeds[i]);
        }
    }

    set_all_leds(CRGB::Black);  // Initialize LEDs as off
    FastLED.setBrightness(50);  // Set initial brightness
    FastLED.show();
    delay(500);
}

/* All LED control */
void set_all_leds(CRGB color) {
    for (int i = 0; i < NUM_STRIPS; i++) {
        for (int j = 0; j < numLeds[i]; j++) {
            leds[i][j] = color;
        }
    }
    FastLED.show();
}

/* LED group control */
void set_led_range(int stripIndex, int startLed, int endLed, CRGB color) {
    /*Serial.print("stripIndex: ");
    Serial.print(stripIndex);
    Serial.print(", startLed: ");
    Serial.print(startLed);
    Serial.print(", endLed: ");
    Serial.println(endLed); */

    if (stripIndex < 0 || stripIndex >= NUM_STRIPS) {
        Serial.println("Invalid strip index!");
        return;
    }
    if (startLed < 0 || endLed >= numLeds[stripIndex] || startLed > endLed) {
        Serial.println("Invalid LED range!");
        return;
    }

    for (int i = startLed; i <= endLed; i++) {
        leds[stripIndex][i] = color;
    }
    FastLED.show();
}

/* Load bar control */
void load_bar_range(CRGB color, unsigned long duration, int stripIndex, int startIndex, int endIndex) {
    if (stripIndex < 0 || stripIndex >= NUM_STRIPS) {
        Serial.println("Invalid strip index!");
        return;
    }

    int totalLeds = endIndex - startIndex + 1;
    unsigned long interval = duration / totalLeds;

    for (int i = startIndex; i <= endIndex && i < numLeds[stripIndex]; i++) {
        leds[stripIndex][i] = color;
        FastLED.show();
        delay(interval);
        // Print individual color components (Red, Green, Blue) instead of the entire CRGB object
        /*Serial.print("LED ");
        Serial.print(i);
        Serial.print(" updated with color: R=");
        Serial.print(color.r);  // Red component
        Serial.print(" G=");
        Serial.print(color.g);  // Green component
        Serial.print(" B=");
        Serial.println(color.b); // Blue component*/
    }

    // Turn off LEDs after the load bar completes
    for (int i = startIndex; i <= endIndex && i < numLeds[stripIndex]; i++) {
        leds[stripIndex][i] = CRGB::Black;
    }
    FastLED.show();
}

/* Blinking function for a range of LEDs */
void blink_led_range(int stripIndex, int startLed, int endLed, CRGB color, int speed) {
    if (stripIndex >= 0 && stripIndex < NUM_STRIPS && startLed >= 0 && endLed < numLeds[stripIndex]) {
        for (int i = startLed; i <= endLed; i++) {
            leds[stripIndex][i] = color;
        }
        FastLED.show();
        delay(speed);
        for (int i = startLed; i <= endLed; i++) {
            leds[stripIndex][i] = CRGB::Black;
        }
        FastLED.show();
        delay(speed);
    }
}



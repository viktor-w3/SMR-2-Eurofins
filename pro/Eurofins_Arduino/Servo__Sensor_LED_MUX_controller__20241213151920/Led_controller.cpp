#include "Led_controller.h"

CRGB leds[NUM_STRIPS][MAX_NUM_LEDS];  // Array to hold LED data for each strip, define MAX_NUM_LEDS based on the largest strip

int dataPins[NUM_STRIPS] = {9};  // Adjust the data pins according to your setup
int numLeds[NUM_STRIPS] = {30};  // Example: 10 LEDs on strip 1, 10 on strip 2, 9 on strip 3

void initialize_leds() {
  // Initialize each LED strip with its corresponding data pin
  for (int i = 0; i < NUM_STRIPS; i++) {
    // Initialize LEDs on each strip with numLeds[i] as the number of LEDs for that strip
    FastLED.addLeds<WS2812B, 9, RGB>(leds[i], numLeds[i]); // Use numLeds[i] instead of NUM_LEDS
  }
  set_all_leds(CRGB::Black);
  FastLED.setBrightness(50);
  FastLED.show();
}

/*
Not required, FastLED.h already handles this.
void deinitialize_leds() {
  for (int i = 0; i < NUM_STRIPS; i++) {
    // No need to delete leds[] here as FastLED manages memory automatically
  }
}
*/

void set_all_leds(CRGB color) {
  for (int i = 0; i < NUM_STRIPS; i++) {
    for (int j = 0; j < numLeds[i]; j++) {
      leds[i][j] = color;
    }
  }
  FastLED.show();
}

void set_strip_leds(int stripIndex, CRGB color) {
  if (stripIndex >= 0 && stripIndex < NUM_STRIPS) {
    for (int i = 0; i < numLeds[stripIndex]; i++) {
      leds[stripIndex][i] = color;
    }
    FastLED.show();
  } else {
    Serial.println("Invalid strip index!");
  }
}

void set_led(int stripIndex, int ledIndex, CRGB color) {
  if (stripIndex >= 0 && stripIndex < NUM_STRIPS && ledIndex >= 0 && ledIndex < numLeds[stripIndex]) {
    leds[stripIndex][ledIndex] = color;
    FastLED.show();
  } else {
    Serial.println("Invalid strip index or LED index!");
  }
}

void load_bar(CRGB color, unsigned long duration, int stripIndex) {
  if (stripIndex < 0 || stripIndex >= NUM_STRIPS) {
    Serial.println("Invalid strip index!");
    return;
  }

  int totalLeds = numLeds[stripIndex];       // Number of LEDs in the strip
  unsigned long interval = duration / totalLeds;  // Time interval for each LED to light up

  for (int i = 0; i < totalLeds; i++) {
    leds[stripIndex][i] = color;             // Set LED to the specified color
    FastLED.show();
    delay(interval);                        // Wait for the calculated interval
  }

  // Turn off LEDs after the load bar completes
  for (int i = 0; i < totalLeds; i++) {
    leds[stripIndex][i] = CRGB::Black;
  }
  FastLED.show();

  Serial.println("done"); // Notify completion
}

/*
  // Optional: Add a blinking effect after the loading bar is complete
  unsigned long blinkStartTime = millis();
  unsigned long blinkDuration = 500;
  unsigned long lastBlinkTime = millis();
  bool ledState = false;

  while (millis() - blinkStartTime < blinkDuration) {
    if (millis() - lastBlinkTime >= 200) {
      lastBlinkTime = millis();
      ledState = !ledState;
      CRGB currentColor = ledState ? color : CRGB::Black; // ? operator replaced if statement for the blinking.
      for (int i = 0; i < numLeds[stripIndex]; i++) {
        leds[stripIndex][i] = currentColor;
      }
      FastLED.show();
    }
  }
}
*/


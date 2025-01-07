//Led_controller.cpp
#include "Led_controller.h"

CRGB leds[NUM_STRIPS][MAX_NUM_LEDS];  // Array to hold LED data for each strip, define MAX_NUM_LEDS based on the largest strip

int dataPins[NUM_STRIPS] = {9 , 10, 11};  // Adjust the data pins according to your setup
int numLeds[NUM_STRIPS] = {30, 30, 30};  // Example: 10 LEDs on strip 1, 10 on strip 2, 9 on strip 3

/* Initialization (Delfault settings) */
void initialize_leds() {
    for (int i = 0; i < NUM_STRIPS; i++) {
        // Initialize each LED strip separately
        if (i == 0) {
            FastLED.addLeds<WS2812B, 9, RGB>(leds[i], numLeds[i]); // Strip 0
        } else if (i == 1) {
            FastLED.addLeds<WS2812B, 10, RGB>(leds[i], numLeds[i]); // Strip 1
        } else if (i == 2) {
            FastLED.addLeds<WS2812B, 11, RGB>(leds[i], numLeds[i]); // Strip 2
        }
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
/* All LED control */
void set_all_leds(CRGB color) {
  for (int i = 0; i < NUM_STRIPS; i++) {
    for (int j = 0; j < numLeds[i]; j++) {
      leds[i][j] = color;
    }
  }
  FastLED.show();
}

/* Strip control */
void set_strip_leds(int stripIndex, CRGB color) {
  if (stripIndex >= 0 && stripIndex < NUM_STRIPS) {
    for (int i = 0; i < numLeds[stripIndex]; i++) {
      leds[stripIndex][i] = color;
    }
    FastLED.show();
  } else {
    Serial.println("Invalid strip index!");
    Serial.println(stripIndex);  
  }
}

/*Single LED control */
void set_led(int stripIndex, int ledIndex, CRGB color) {
  if (stripIndex >= 0 && stripIndex < NUM_STRIPS && ledIndex >= 0 && ledIndex < numLeds[stripIndex]) {
    leds[stripIndex][ledIndex] = color;
    FastLED.show();
  } else {
    Serial.println("Invalid strip index or LED index!");
  }
}

/* LED group control */
void set_led_range(int stripIndex, int startLed, int endLed, CRGB color) {
    if (stripIndex < 0 || stripIndex >= NUM_STRIPS) {
        Serial.println("Invalid strip index!");
        Serial.println(stripIndex);  
        return;
    }
    if (startLed < 0 || endLed > numLeds[stripIndex] || startLed > endLed) {
        Serial.println("Invalid LED range!");
        Serial.print("Given start LED: ");
        Serial.println(startLed);
        Serial.print("Given end LED: ");
        Serial.println(endLed);
        return;
    }

    for (int i = startLed; i <= endLed; i++) {
        leds[stripIndex][i] = color;  // Stel de kleur in voor elk LED in het bereik
    }
    FastLED.show();  // Update de LEDs om de wijzigingen door te voeren
    Serial.println("done");  // Bevestig de opdracht
}

/* Loadbar control */
void load_bar_range(CRGB color, unsigned long duration, int stripIndex, int startIndex, int endIndex) {
  if (stripIndex < 0 || stripIndex >= NUM_STRIPS) {
    Serial.println("Invalid strip index!");
    Serial.println(stripIndex);
    return;
  }

  int totalLeds = endIndex - startIndex + 1;
  unsigned long interval = duration / totalLeds;

  for (int i = startIndex; i <= endIndex && i < numLeds[stripIndex]; i++) {
    leds[stripIndex][i] = color;
    FastLED.show();
    delay(interval);
  }

  // Turn off LEDs after the load bar completes
  for (int i = startIndex; i <= endIndex && i < numLeds[stripIndex]; i++) {
    leds[stripIndex][i] = CRGB::Black;
  }
  FastLED.show();
  Serial.println("done");
}

/* Blink functions */

// Blinking functions for single LEDs, all LEDs, and ranges
void blink_single_led(int stripIndex, int ledIndex, CRGB color, int speed) {
    if (stripIndex >= 0 && stripIndex < NUM_STRIPS && ledIndex >= 0 && ledIndex < numLeds[stripIndex]) {
        leds[stripIndex][ledIndex] = color;
        FastLED.show();
        delay(speed);
        leds[stripIndex][ledIndex] = CRGB::Black;
        FastLED.show();
        delay(speed);
    }
}

void blink_all_leds_on_strip(int stripIndex, CRGB color, int speed) {
    if (stripIndex >= 0 && stripIndex < NUM_STRIPS) {
        for (int i = 0; i < numLeds[stripIndex]; i++) {
            leds[stripIndex][i] = color;
        }
        FastLED.show();
        delay(speed);
        for (int i = 0; i < numLeds[stripIndex]; i++) {
            leds[stripIndex][i] = CRGB::Black;
        }
        FastLED.show();
        delay(speed);
    }
}

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
/*
void blink_multiple_strips(int stripIndices[], int numStrips, CRGB color, int speed) {
    for (int i = 0; i < 10; i++) {  // Blink 10 times (example)
        for (int s = 0; s < numStrips; s++) {
            int stripIndex = stripIndices[s];
            if (stripIndex < 0 || stripIndex >= NUM_STRIPS) continue;
            fill_solid(leds[stripIndex], numLeds[stripIndex], color);
        }
        FastLED.show();
        delay(speed);
        for (int s = 0; s < numStrips; s++) {
            int stripIndex = stripIndices[s];
            if (stripIndex < 0 || stripIndex >= NUM_STRIPS) continue;
            fill_solid(leds[stripIndex], numLeds[stripIndex], CRGB::Black);
        }
        FastLED.show();
        delay(speed);
    }
}
*/


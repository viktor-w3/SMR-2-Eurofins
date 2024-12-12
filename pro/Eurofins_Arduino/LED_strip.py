from ws2812 import WS2812

class LedColours:
	#Example where we set the colour of the first 4 leds by chaining the information in series.
	chain = WS2812(spi_bus=1, led_count=4)
	data = [
		(255, 0, 0),    # red LED 1
		(0, 255, 0),    # green LED 2
		(0, 0, 255),    # blue LED 3
		(85, 85, 85),   # white LED 4
	]
	chain.show(data)
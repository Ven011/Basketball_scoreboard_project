from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import audioio
import audiomp3
import board
import digitalio
import analogio
import displayio
import framebufferio
import neopixel
import rgbmatrix
import time

# setup RGBMatrix
displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
	bit_depth = 4,
	height = 32,
	width = 64,
	rgb_pins = [board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
	addr_pins = [board.A5, board.A4, board.A3, board.A2],
	clock_pin = board.D13,
	latch_pin = board.D0,
	output_enable_pin = board.D1
)
display = framebufferio.FramebufferDisplay(matrix)

# display groups
test_group = displayio.Group()

# setup font
font_ozone = bitmap_font.load_font("/fonts/ozone.bdf")

# setup graphics for the start_group
score_value = label.Label(font_ozone, text = "0", color = 0x00B300)
score_value.x = 3
score_value.y = 3

# add graphics to the display groups
test_group.append(score_value)

# show the test_group
display.show(test_group)

# setup distance sensor
sensor_1 = digitalio.digitalInOut(board.MOSI)
sensor_1.direction = digitalio.Direction.Input

sensor_2 = digitalio.digitalInOut(board.MISO)
sensor_2.direction = digitalio.Direction.Input

sensors_triggered = 0
score = 0

while True:
	if sensor_1.value:
		sensors_triggered += 1
	if sensor_2.value:
		sensors_triggered += 1
  
	if sensors_triggered == 2:
		sensors_triggered = 0
		score += 1

	score_value.text = str(score)
	time.sleep(0.10)

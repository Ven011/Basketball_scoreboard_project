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
distance_value = label.Label(font_ozone, text = "0", color = 0x00B300)
distance_value.x = 3
distance_value.y = 3

# add graphics to the display groups
test_group.append(distance_value)

# show the test_group
display.show(test_group)

# setup distance sensor
distance_sensor = analogio.AnalogIn(board.A1)
# distance_sensor.reference_voltage = 3.3 # AREF of feather M4 board

while True:
    voltage = distance_sensor.value*(5/1024)
    distance_value.text = str(int(13/voltage))
    time.sleep(0.25)

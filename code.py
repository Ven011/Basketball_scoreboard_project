from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import WHITE
import audioio
import audiomp3
import board
import digitalio
import displayio
import framebufferio
import neopixel
import rgbmatrix
import time
from random import randint

# RGBMatrix
displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
	width = 64,
	height = 32,
	bit_depth = 4,
	rgb_pins = [board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
	addr_pins = [board.A5, board.A4, board.A3, board.A2],
	clock_pin = board.D13,
	latch_pin = board.D0,
	output_enable_pin = board.D1
)
display = framebufferio.FramebufferDisplay(matrix)

# display groups
arcade_group = displayio.Group()

# font
font_ozone = bitmap_font.load_font("/fonts/ozone.bdf")
font_virtual_pet_sans = bitmap_font.load_font("/fonts/virtual_pet_sans.bdf")

# arcade_group graphics
ag_time = label.Label(font_ozone, text = "TIME", color = 0xB35A00)
ag_time.x = 1
ag_time.y = 4

ag_time_c = label.Label(font_virtual_pet_sans, text = "", color = 0x00B300)
ag_time_c.y = 16

ag_score = label.Label(font_ozone, text = "SCORE", color = 0x0000B3)
ag_score.x = 29
ag_score.y = 4

ag_score_c = label.Label(font_virtual_pet_sans, text = "", color = 0xFFFFFF)
ag_score_c.y = 16

ag_hiscore = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x00B3B3)
ag_hiscore.x = 7
ag_hiscore.y = 28

ag_hiscore_c = label.Label(font_virtual_pet_sans, text = "0", color = 0xB30000)
ag_hiscore_c.x = 52
ag_hiscore_c.y = 28

# add graphics to display groups
arcade_group.append(ag_time)
arcade_group.append(ag_time_c)
arcade_group.append(ag_score)
arcade_group.append(ag_score_c)
arcade_group.append(ag_hiscore)
arcade_group.append(ag_hiscore_c)

# audio files
speaker = audioio.AudioOut(board.A0)
audio_file = {
	"space_jam": "/audio/space_jam.mp3",
	"whistle": "/audio/whistle.mp3",
	"countdown": "/audio/countdown.mp3",
	"game_over": "/audio/game_over.mp3",
	"hiscore": "/audio/hiscore.mp3"
}
mp3stream = audiomp3.MP3Decoder(open(audio_file["space_jam"], "rb"))

# NeoPixels
led_pin = board.D25
num_leds = 54
leds = neopixel.NeoPixel(led_pin, num_leds, brightness = 0.20)
rainbow_sparkle = RainbowSparkle(leds, speed = 0.15, period = 3, num_sparkles = 27, precompute_rainbow = True)
solid = Solid(leds, color = WHITE)

# main loop, run the approriate screen function given the screen state
display.show(arcade_group)
score = 0
start_time = time.time()

mp3stream.file = open(audio_file["whistle"], "rb")

while True:
    if time.time() >= start_time + 10:
        speaker.play(mp3stream)
        display.show(arcade_group)
        start_time = time.time()
        score += 1
        
    ag_score_c.text = str(score)
    ag_score_c.color = 0xFFFFFF
    

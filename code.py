from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import audioio
import audiomp3
import board
import digitalio
import displayio
import framebufferio
import rgbmatrix
import time

# RGBMatrix setup
displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
	bit_depth = 4,
	height = 32,
	width = 64,
	rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
	addr_pins=[board.A5, board.A4, board.A3, board.A2],
	clock_pin = board.D13,
	latch_pin = board.D0,
	output_enable_pin = board.D1
)
display = framebufferio.FramebufferDisplay(matrix)

# display groups
start_group = displayio.Group()

# setup font & text for start_group
font_ozone = bitmap_font.load_font("/fonts/ozone.bdf")
font_virtual_pet_sans = bitmap_font.load_font("/fonts/virtual_pet_sans.bdf")

shootout_title = label.Label(font_ozone, text = "SHOOTOUT!", color = 0xFF8C00)
shootout_title.x = 3
shootout_title.y = 3

insert_title = label.Label(font_virtual_pet_sans, text = "INSERT", color = 0xFFFFFF)
insert_title.x = 1
insert_title.y = 17

coin_title = label.Label(font_virtual_pet_sans, text = "COIN", color = 0xFFFFFF)
coin_title.x = 40
coin_title.y = 17

hi_score_title = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x008B8B)
hi_score_title.x = 1
hi_score_title.y = 29

hi_score = label.Label(font_virtual_pet_sans, text = "000", color = 0x8B0000)
hi_score.x = 46
hi_score.y = 29
highest_score = 0

# add graphics to the display groups
start_group.append(shootout_title)
start_group.append(insert_title)
start_group.append(coin_title)
start_group.append(hi_score_title)
start_group.append(hi_score)

# show the start_group
display.show(start_group)

# setup audio files, stream, and speaker
speaker = audioio.AudioOut(board.A0)
audio_file = {
	"for_setup": "/audio/shootout.mp3",
	"shootout": "/audio/shootout.mp3",
	"insert_coin": "/audio/insert_coin.mp3"
}
mp3stream = audiomp3.MP3Decoder(open(audio_file["for_setup"], "rb"))

# play start_group audio
mp3stream.file = open(audio_file["shootout"], "rb")
speaker.play(mp3stream)

# setup button pin and state
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

button_state = False

# variables used in the loop
previous_time = time.time()
insert_title_is_visible = True
coin_title_is_visible = True

while True:
	# button debouncing
	if not button.value and not button_state:
		button_state = True

	# button is pressed
	if button_state:
		button_state = False
		mp3stream.file = open(audio_file["insert_coin"], "rb")
		speaker.play(mp3stream)
		# game would start from here...
        
	# blink "INSERT COIN" title
	if time.time() >= previous_time + 1:
		previous_time = time.time()
		if insert_title_is_visible and coin_title_is_visible:
			insert_title.color = 0x000000
			insert_title_is_visible = False
			coin_title.color = 0x000000
			coin_title_is_visible = False
		else:
			insert_title.color = 0xFFFFFF
			insert_title_is_visible = True
			coin_title.color = 0xFFFFFF
			coin_title_is_visible = True
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import audioio
import audiomp3
import board
import digitalio
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
start_group = displayio.Group()
game_group = displayio.Group()

# setup font
font_ozone = bitmap_font.load_font("/fonts/ozone.bdf")
font_virtual_pet_sans = bitmap_font.load_font("/fonts/virtual_pet_sans.bdf")

# setup graphics for the start_group
shootout_title = label.Label(font_ozone, text = "SHOOTOUT!", color = 0x45FF7F)
shootout_title.x = 3
shootout_title.y = 3

insert_title = label.Label(font_virtual_pet_sans, text = "INSERT", color = 0xFFFFFF)
insert_title.x = 1
insert_title.y = 17

coin_title = label.Label(font_virtual_pet_sans, text = "COIN", color = 0xFFFFFF)
coin_title.x = 40
coin_title.y = 17

hi_score_title = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0xFFDC45)
hi_score_title.x = 1
hi_score_title.y = 29

hi_score = label.Label(font_virtual_pet_sans, text = "000", color = 0xFF4568) 
hi_score.x = 46
hi_score.y = 29

# setup graphics for the game_group
time_title = label.Label(font_virtual_pet_sans, text = "TIME", color = 0xFF7F45)
time_title.x = 3
time_title.y = 6

score_title = label.Label(font_virtual_pet_sans, text = "SCORE", color = 0x45C5FF)
score_title.x = 32
score_title.y = 6

time_count = label.Label(font_ozone, text = "60", color = 0x45FF7F)
time_count.x = 8
time_count.y = 14

score_count = label.Label(font_ozone, text = "0", color = 0xFFFFFF)
score_count.x = 37
score_count.y = 14

game_hi_score_title = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0xFFDC45)
game_hi_score_title.x = 1
game_hi_score_title.y = 27

game_hi_score = label.Label(font_virtual_pet_sans, text = "000", color = 0xFF4568) 
game_hi_score.x = 46
game_hi_score.y = 27

# add graphics to the display groups
start_group.append(shootout_title)
start_group.append(insert_title)
start_group.append(coin_title)
start_group.append(hi_score_title)
start_group.append(hi_score)

game_group.append(time_title)
game_group.append(score_title)
game_group.append(time_count)
game_group.append(score_count)
game_group.append(game_hi_score_title)
game_group.append(game_hi_score)

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

# setup distance sensor

# setup neopixels

# variables used in the loop
scoreboard_state = "inStart" # scoreboard states: inStart, inGame, inGameEnd
previous_time = time.time()
insert_title_is_visible = True
coin_title_is_visible = True
game_start_time = 0

while True:
	# button debouncing
	if not button.value and not button_state:
		button_state = True

	# button is pressed while in start screen
	if button_state and scoreboard_state == "inStart":
		button_state = False
		mp3stream.file = open(audio_file["insert_coin"], "rb")
		speaker.play(mp3stream)

		# start the game
		scoreboard_state = "inGame"
		display.show(game_group)

		time.sleep(0.5) # wait half a second
		time_count.text = str(60)
		game_start_time = time.time()

		# reset title properties for a new game
		time_count.color = 0x45FF7F

		while scoreboard_state == "inGame":
			# update the time left in the round
			time_count.text = str(60 - int(time.time() - game_start_time)) # int() to get whole number

			# FOR TESTING: increment the score when the button is pressed
			if not button.value and not button_state:
				button_state = True

			if button_state:
				button_state = False
				score_count.text = str(int(score_count.text) + 2)

			# change the time value's color depending on time
			if int(time_count.text) <= 20 and int(time_count.text) >= 11:
				time_count.color = 0xFFDC45
			elif int(time_count.text) <= 10 and int(time_count.text) >= 0:
				time_count.color = 0xFF4568

			# update the high score value if the score is greater than the current high score
			if int(score_count.text) > int(game_hi_score.text): # int() is used in case value is a string
				game_hi_score.text = score_count.text

			# exit game if the time is up
			if int(time_count.text) == 0:
				scoreboard_state = "inStart"
				hi_score.text = game_hi_score.text
				display.show(start_group) # REMOVE AFTER TESTING

	# blink the INSERT COIN title when on the start screen
	if time.time() >= previous_time + 1 and scoreboard_state == "inStart":
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

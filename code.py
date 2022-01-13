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

# game functions
def get_set_hiscore(value = "_"):
	if value != "_":
 		hiscore_file = open("/temp/hiscore.txt", "w")
		hiscore_file.write(value)
		hiscore_file.close()
	else: # default value of zero for score indicated want to fetch hiscore
		hiscore_file = open("/temp/hiscore.txt", "r")
		score = hiscore_file.read()
		hiscore_file.close()
		return score

# setup font
font_ozone = bitmap_font.load_font("/fonts/ozone.bdf")
font_virtual_pet_sans = bitmap_font.load_font("/fonts/virtual_pet_sans.bdf")

# setup graphics for the start_group
shootout_title = label.Label(font_ozone, text = "SHOOTOUT!", color = 0x00B300)
shootout_title.x = 3
shootout_title.y = 3

insert_title = label.Label(font_virtual_pet_sans, text = "INSERT", color = 0xFFFFFF)
insert_title.x = 1
insert_title.y = 17

coin_title = label.Label(font_virtual_pet_sans, text = "COIN", color = 0xFFFFFF)
coin_title.x = 40
coin_title.y = 17

hiscore_title = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x00B3B3)
hiscore_title.x = 1
hiscore_title.y = 29

hiscore = label.Label(font_virtual_pet_sans, text = get_set_hiscore(), color = 0xB30000)
hiscore.x = 46
hiscore.y = 29

# setup graphics for the game_group
time_title = label.Label(font_virtual_pet_sans, text = "TIME", color = 0xB35A00)
time_title.x = 3
time_title.y = 4

time_count = label.Label(font_ozone, text = "60", color = 0x00B300)
time_count.x = 8
time_count.y = 13

score_title = label.Label(font_virtual_pet_sans, text = "SCORE", color = 0x0000B3)
score_title.x = 32
score_title.y = 4

score_count = label.Label(font_ozone, text = "0", color = 0xFFFFFF)
score_count.x = 37
score_count.y = 13

game_hiscore_title = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x00B3B3)
game_hiscore_title.x = 1
game_hiscore_title.y = 29

game_hiscore = label.Label(font_virtual_pet_sans, text = get_set_hiscore(), color = 0xB30000)
game_hiscore.x = 46
game_hiscore.y = 29

# add graphics to the display groups
start_group.append(shootout_title)
start_group.append(insert_title)
start_group.append(coin_title)
start_group.append(hiscore_title)
start_group.append(hiscore)

game_group.append(time_title)
game_group.append(time_count)
game_group.append(score_title)
game_group.append(score_count)
game_group.append(game_hiscore_title)
game_group.append(game_hiscore)

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
button = digitalio.DigitalInOut(board.SCL)
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

		# reset title properties
		time_count.text = "60"
		time_count.color = 0x00B300
		score_count.text = "0"

		display.show(game_group)
		time.sleep(0.5) # wait half a second
		game_start_time = time.time()

		# game variables
		highest_score = get_set_hiscore()

		while scoreboard_state == "inGame":
			# update the time left in the round
			time_count.text = str(60 - int(time.time() - game_start_time)) # int() to get whole number

			# FOR TESTING: increment the score when the button is pressed
			if not button.value and not button_state:
				button_state = True

			if button_state:
				button_state = False
				score_count.text = str(int(score_count.text) + 1)

			# change the time value's color depending on time
			if int(time_count.text) <= 20 and int(time_count.text) >= 11:
				time_count.color = 0xB3B300
			elif int(time_count.text) <= 10 and int(time_count.text) >= 0:
				time_count.color = 0xB30000

			# update the high score value if the score is greater than the current high score
			if int(score_count.text) > int(game_hiscore.text): # int() is used in case value is a string
				highest_score = score_count.text

			# exit game if the time is up
			if int(time_count.text) == 0:
				time.sleep(1)
				scoreboard_state = "inStart"
				hiscore.text = highest_score
				game_hiscore.text = highest_score
				get_set_hiscore(value = highest_score) # save highest score
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

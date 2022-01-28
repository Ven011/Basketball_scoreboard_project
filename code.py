from tracemalloc import start
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
new_hiscore_group = displayio.Group()
gameover_group = displayio.Group()

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

start_hiscore_title = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x00B3B3)
start_hiscore_title.x = 1
start_hiscore_title.y = 29

start_hiscore = label.Label(font_virtual_pet_sans, text = get_set_hiscore(), color = 0xB30000)
start_hiscore.x = 46
start_hiscore.y = 29

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
score_count.x = 43
score_count.y = 13

game_hiscore_title = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x00B3B3)
game_hiscore_title.x = 1
game_hiscore_title.y = 29

game_hiscore = label.Label(font_virtual_pet_sans, text = get_set_hiscore(), color = 0xB30000)
game_hiscore.x = 46
game_hiscore.y = 29

# Setup graphics for the new high score group
new_title = label.Label(font_ozone, text = "NEW", color = 0xFF0000)
new_title.x = 21
new_title.y = 5

new_hiscore_title = label.Label(font_virtual_pet_sans, text = "Hi-SCORE", color = 0xFFFF00)
new_hiscore_title.x = 10
new_hiscore_title.y = 16

new_hiscore_count = label.Label(font_virtual_pet_sans, text = "0", color = 0xFFFFFF)
new_hiscore_count.x = 24
new_hiscore_count.y = 29

# Setup graphics for the game over group
gameover_title = label.Label(font_ozone, text = "GAME OVER!", color = 0xFFC0CB)
gameover_title.x = 1
gameover_title.y = 4

gameover_score_title = label.Label(font_virtual_pet_sans, text = "SCORE", color = 0x0000FF)
gameover_score_title.x = 18
gameover_score_title.y = 15

gameover_score = label.Label(font_ozone, text = "0", color = 0xFFFFFF)
gameover_score.x = 24
gameover_score.y = 25

# add graphics to the display groups
start_group.append(shootout_title)
start_group.append(insert_title)
start_group.append(coin_title)
start_group.append(start_hiscore_title)
start_group.append(start_hiscore)

game_group.append(time_title)
game_group.append(time_count)
game_group.append(score_title)
game_group.append(score_count)
game_group.append(game_hiscore_title)
game_group.append(game_hiscore)

new_hiscore_group.append(new_title)
new_hiscore_group.append(new_hiscore_title)
new_hiscore_group.append(new_hiscore_count)

gameover_group.append(gameover_title)
gameover_group.append(gameover_score_title)
gameover_group.append(gameover_score)

# show the start_group
display.show(start_group)

# setup audio files, stream, and speaker
speaker = audioio.AudioOut(board.A0)
audio_file = {
	"for_setup": "/audio/shootout.mp3",
	"shootout": "/audio/shootout.mp3",
	"insert_coin": "/audio/insert_coin.mp3",
	"new_highscore": "/audio/hiscore.mp3",
	"game_over": "/audio/game_over.mp3"
}
mp3stream = audiomp3.MP3Decoder(open(audio_file["for_setup"], "rb"))

# play start_group audio
mp3stream.file = open(audio_file["shootout"], "rb")
speaker.play(mp3stream)

# setup button pin and state
button = digitalio.DigitalInOut(board.SCL)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

## setup distance sensor
# distance_sensor = analogio.AnalogIn(board.A1)

# setup break beam sensor
break_beam = digitalio.DigitalInOut(board.A1)
break_beam.direction = digitalio.Direction.INPUT
break_beam.pull = digitalio.Pull.UP

# setup neopixels
led_pin = board.D25
number_of_leds = 54
leds = neopixel.NeoPixel(led_pin, number_of_leds, brightness = 0.20)

# variables used in the loop
button_state = False

game_start_time = 0

blink_timer = time.time()
labels_are_visible = True # Used to blink labels

while True:
	# button debouncing
	if not button.value and not button_state:
		button_state = True

	# button is pressed while in start screen
	if button_state:
		# Setup and start the game
		button_state = False
		mp3stream.file = open(audio_file["insert_coin"], "rb")
		speaker.play(mp3stream)

		# reset title properties
		time_count.text = "60"
		time_count.color = 0x00B300
		score_count.text = "0"

		display.show(game_group)
		time.sleep(0.50) # wait half a second
		game_start_time = time.time()

		# game variables
		highest_score = get_set_hiscore()
		lights_color_intensity = 255 # used to fade in and out the RGB colors
		lights_clock = 0 # Keeps track of the time a color change in LEDs happened
		ball_scored = False
		beam_broken = False
		time_scored = time.time()

		while int(time_count.text) > -1:
			# update the time left in the round
			time_count.text = str(60 - int(time.time() - game_start_time)) # int() to get whole number

			# time_count text x pos if 1 digit time (if number has a 1 in it should move 1 more pixel)
			if int(time_count.text) <= 9:
				time_count.x = 12

			# get distance value
			# voltage = distance_sensor.value * (3.3 / 65535)
			# distance = int(13 / voltage)

			# Check if the beam has been broken
			beam_broken = True if break_beam.value == 0 else False
   
			if beam_broken and not ball_scored and time.time() >= time_scored + 1:
				score_count.text = str(int(score_count.text) + 1)
				time_scored = time.time()
				# Set score tracker variable to True
				ball_scored = True
			elif not beam_broken:
				if ball_scored:
					ball_scored = False

			# score_count text x pos if 3 digit score (if number has a 1 in it should move 1 more pixel)
			if int(score_count.text) >= 100:
				score_count.x = 37
			# score_count x pos if 2 digit score (if number has a 1 in it should move 1 more pixel)
			elif int(score_count.text) >= 10:
				score_count.x = 40

			# change the time value's color and RGB lights depending on time left in game
			if int(time_count.text) <= 60 and int(time_count.text) >= 21:
				time_count.color = 0x00B300 # Green
				if int(time_count.text) == 60:
					leds.fill((255, 0, 0))
					lights_clock = time.time()
				# Fade the LEDs in and out
				# lights_color_intensity = int(127.5 + 127.5 * math.cos(time.time() - lights_clock))

			elif int(time_count.text) <= 20 and int(time_count.text) >= 11:
				time_count.color = 0xB3B300 # Yellow
				if int(time_count.text) == 20:
					lights_clock = time.time()
					leds.fill((255, 0, 0))
				# Fade the LEDs in and out
				# lights_color_intensity = int(127.5 + 127.5 * math.cos(time.time() - lights_clock))

			elif int(time_count.text) <= 10 and int(time_count.text) >= 0:
				time_count.color = 0xB30000 # Red
				if int(time_count.text) == 10:
					lights_clock = time.time()
					leds.fill((255, 0, 0))
				# Fade the LEDs in and out
				# lights_color_intensity = int(127.5 + 127.5 * math.cos(time.time() - lights_clock))

			# update the high score value if the score is greater than the current high score
			if int(score_count.text) > int(game_hiscore.text): # int() is used in case value is a string
				highest_score = score_count.text

			# exit game if the time is up
			if int(time_count.text) == 0:
				time.sleep(1) # allow time value of 0 to be seen
				if highest_score > int(get_set_hiscore()): # if the player scored higher than the previous highscore
					# Update the start screen high score
					start_hiscore.text = highest_score
					# Update the game screen highscore value
					game_hiscore.text = highest_score
					# Save the high score
					get_set_hiscore(value = highest_score)
					# Show the new high score screen
					start_time = time.time()
     
					# Format the high score value on the display. Keep value centered
					if highest_score <= 9:
						new_hiscore_count.x = 29
					elif highest_score >= 10 and highest_score <= 99:
						new_hiscore_count.x = 26
					elif highest_score >= 100:
						new_hiscore_count.x = 23
     
					display.show(new_hiscore_group)
					
					# Play the new high score audio
					mp3stream.file = open(audio_file["new_highscore"], "rb")
					speaker.play(mp3stream)
     
					labels_are_visible = True
					blink_timer = time.time()

					while time.time() - start_time <= 5: # While in this screen for 5 seconds. 
						# Blink the labels
						if time.time() >= blink_timer + 1:
							blink_timer = time.time()
							if labels_are_visible:
								# Change their color to black
								new_title.color = 0x000000
								new_hiscore_title.color = 0x000000
								new_hiscore_count.color = 0x000000
								labels_are_visible = False
							else:
								# Change their color to their apppropriate colors
								new_title.color = 0xFF0000
								new_hiscore_title.color = 0xFFFF00
								new_hiscore_count.coloar = 0xFFFFFF
								labels_are_visible = True
        
					leds.fill((255, 255, 255)) # Set all pixels to white
					display.show(start_group)

				else: # The player finished the game, no new high score was set
					gameover_score.text = score_count.text		

     				# Play the game over audio
					mp3stream.file = open(audio_file["game_over"], "rb")
					speaker.play(mp3stream)
					
					labels_are_visible = True
					blink_timer = time.time()
					start_time = time.time()
     
					while time.time() - start_time <= 5: # While in this screen
						# Blink the gameover label
						if time.time() >= blink_timer + 1:
							blink_timer = time.time()
							if labels_are_visible:
								# Change their color to black
								gameover_title.color = 0x000000
								labels_are_visible = False
							else:
								# Change their color to their apppropriate colors
								gameover_title.color = 0xFFC0CB
								labels_are_visible = True

					leds.fill((255, 255, 255)) # Set all pixels to white
					display.show(start_group)

	# blink the INSERT COIN title when on the start screen
	if time.time() >= blink_timer + 1:
		blink_timer = time.time()
		if labels_are_visible:
			insert_title.color = 0x000000
			coin_title.color = 0x000000
			labels_are_visible = False
		else:
			insert_title.color = 0xFFFFFF
			coin_title.color = 0xFFFFFF
			labels_are_visible = True

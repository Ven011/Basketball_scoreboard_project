from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import WHITE, RED, YELLOW, GREEN, BLACK
import audioio
import audiomp3
import board
import digitalio
import displayio
import framebufferio
import neopixel
import rgbmatrix
import time

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
start_group = displayio.Group()
arcade_group = displayio.Group()
arcade_bt_group = displayio.Group()
game_over_group = displayio.Group()
new_hiscore_group = displayio.Group()
horse_group = displayio.Group()

# save the hiscore to file
def get_set_hiscore(value = "_"):
	if value != "_":
		hiscore_file = open("/temp/hiscore.txt", "w")
		hiscore_file.write(value)
		hiscore_file.close()
	else:
		hiscore_file = open("/temp/hiscore.txt", "r")
		score = hiscore_file.read()
		hiscore_file.close()
		return score

# font
font_ozone = bitmap_font.load_font("/fonts/ozone.bdf")
font_virtual_pet_sans = bitmap_font.load_font("/fonts/virtual_pet_sans.bdf")

# start_group graphics
sg_space = label.Label(font_ozone, text = "SPACE", color = 0x00B300)
sg_space.x = 2
sg_space.y = 4

sg_jam = label.Label(font_ozone, text = "JAM", color = 0x00B300)
sg_jam.x = 40
sg_jam.y = 4

sg_1p = label.Label(font_virtual_pet_sans, text = "1P", color = 0x00B3B3)
sg_1p.x = 6
sg_1p.y = 18

sg_arcade = label.Label(font_virtual_pet_sans, text = "ARCADE", color = 0xFFFFFF)
sg_arcade.x = 21
sg_arcade.y = 18

sg_2p = label.Label(font_virtual_pet_sans, text = "2P", color = 0xB300B3)
sg_2p.x = 6
sg_2p.y = 28

sg_h = label.Label(font_virtual_pet_sans, text = "H.", color = 0xFFFFFF)
sg_h.x = 21
sg_h.y = 28

sg_o = label.Label(font_virtual_pet_sans, text = "O.", color = 0xFFFFFF)
sg_o.x = 29
sg_o.y = 28

sg_r = label.Label(font_virtual_pet_sans, text = "R.", color = 0xFFFFFF)
sg_r.x = 37
sg_r.y = 28

sg_s = label.Label(font_virtual_pet_sans, text = "S.", color = 0xFFFFFF)
sg_s.x = 45
sg_s.y = 28

sg_e = label.Label(font_virtual_pet_sans, text = "E", color = 0xFFFFFF)
sg_e.x = 53
sg_e.y = 28

# arcade_group graphics
ag_time = label.Label(font_ozone, text = "TIME", color = 0xB35A00)
ag_time.x = 1
ag_time.y = 4

ag_time_c = label.Label(font_virtual_pet_sans, text = "", color = 0x00B300)
ag_time_c.x = 8
ag_time_c.y = 16

ag_score = label.Label(font_ozone, text = "SCORE", color = 0x0000B3)
ag_score.x = 29
ag_score.y = 4

ag_score_c = label.Label(font_virtual_pet_sans, text = "", color = 0xFFFFFF)
ag_score_c.x = 43
ag_score_c.y = 16

ag_hiscore = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x00B3B3)
ag_hiscore.x = 7
ag_hiscore.y = 28

ag_hiscore_c = label.Label(font_virtual_pet_sans, text = get_set_hiscore(), color = 0xB30000)
ag_hiscore_c.x = 52
ag_hiscore_c.y = 28

# arcade_bt_group
ag_bt_time = label.Label(font_ozone, text = "TIME", color = 0xB35A00)
ag_bt_time.x = 1
ag_bt_time.y = 4

ag_bt_time_c = label.Label(font_virtual_pet_sans, text = "", color = 0x00B300)
ag_bt_time_c.x = 8
ag_bt_time_c.y = 16

ag_bt_score = label.Label(font_ozone, text = "SCORE", color = 0x0000B3)
ag_bt_score.x = 29
ag_bt_score.y = 4

ag_bt_score_c = label.Label(font_virtual_pet_sans, text = "", color = 0xB3005A)
ag_bt_score_c.x = 43
ag_bt_score_c.y = 16

ag_bt_bonus = label.Label(font_virtual_pet_sans, text = "BONUS", color = 0x5A00B3)
ag_bt_bonus.x = 4
ag_bt_bonus.y = 28

ag_bt_bonus_t = label.Label(font_virtual_pet_sans, text = "TIME", color = 0x5A00B3)
ag_bt_bonus_t.x = 37
ag_bt_bonus_t.y = 28

# game_over_group graphics
gog_game = label.Label(font_ozone, text = "GAME", color = 0xB30000)
gog_game.x = 2
gog_game.y = 5

gog_over = label.Label(font_ozone, text = "OVER", color = 0xB30000)
gog_over.x = 35
gog_over.y = 5

gog_score = label.Label(font_virtual_pet_sans, text = "SCORE", color = 0x0000B3)
gog_score.x = 17
gog_score.y = 17

gog_score_c = label.Label(font_virtual_pet_sans, text = "", color = 0xFFFFFF)
gog_score_c.x = 29
gog_score_c.y = 27

# new_hiscore_group graphics
nhg_new = label.Label(font_ozone, text = "NEW", color = 0x00B300)
nhg_new.x = 21
nhg_new.y = 5

nhg_hiscore = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x00B3B3)
nhg_hiscore.x = 11
nhg_hiscore.y = 17

nhg_hiscore_c = label.Label(font_virtual_pet_sans, text = "", color = 0xFFFFFF)
nhg_hiscore_c.x = 29
nhg_hiscore_c.y = 27

# horse_group graphics
hg_time = label.Label(font_virtual_pet_sans, text = "TIME", color = 0xB35A00)
hg_time.x = 13
hg_time.y = 5

hg_time_c = label.Label(font_virtual_pet_sans, text = "10", color = 0x00B300)
hg_time_c.x = 40
hg_time_c.y = 5

hg_p1 = label.Label(font_virtual_pet_sans, text = "P1", color = 0x00B3B3)
hg_p1.x = 6
hg_p1.y = 17

hg_p1_h = label.Label(font_virtual_pet_sans, text = "H.", color = 0xFFFFFF)
hg_p1_h.x = 21
hg_p1_h.y = 17

hg_p1_o = label.Label(font_virtual_pet_sans, text = "O.", color = 0xFFFFFF)
hg_p1_o.x = 29
hg_p1_o.y = 17

hg_p1_r = label.Label(font_virtual_pet_sans, text = "R.", color = 0xFFFFFF)
hg_p1_r.x = 37
hg_p1_r.y = 17

hg_p1_s = label.Label(font_virtual_pet_sans, text = "S.", color = 0xFFFFFF)
hg_p1_s.x = 45
hg_p1_s.y = 17

hg_p1_e = label.Label(font_virtual_pet_sans, text = "E", color = 0xFFFFFF)
hg_p1_e.x = 53
hg_p1_e.y = 17

hg_p2 = label.Label(font_virtual_pet_sans, text = "P2", color = 0xB300B3)
hg_p2.x = 6
hg_p2.y = 28

hg_p2_h = label.Label(font_virtual_pet_sans, text = "H.", color = 0xFFFFFF)
hg_p2_h.x = 21
hg_p2_h.y = 28

hg_p2_o = label.Label(font_virtual_pet_sans, text = "O.", color = 0xFFFFFF)
hg_p2_o.x = 29
hg_p2_o.y = 28

hg_p2_r = label.Label(font_virtual_pet_sans, text = "R.", color = 0xFFFFFF)
hg_p2_r.x = 37
hg_p2_r.y = 28

hg_p2_s = label.Label(font_virtual_pet_sans, text = "S.", color = 0xFFFFFF)
hg_p2_s.x = 45
hg_p2_s.y = 28

hg_p2_e = label.Label(font_virtual_pet_sans, text = "E", color = 0xFFFFFF)
hg_p2_e.x = 53
hg_p2_e.y = 28

hg_p1_won = label.Label(font_ozone, text = "P1", color = 0x00B3B3)
hg_p1_won.x = 13
hg_p1_won.y = 4

hg_p1_w = label.Label(font_ozone, text = "WON", color = 0x00B3B3)
hg_p1_w.x = 28
hg_p1_w.y = 4

hg_p2_won = label.Label(font_ozone, text = "P2", color = 0xB300B3)
hg_p2_won.x = 12
hg_p2_won.y = 4

hg_p2_w = label.Label(font_ozone, text = "WON", color = 0xB300B3)
hg_p2_w.x = 29
hg_p2_w.y = 4

# add graphics to display groups
start_group.append(sg_space)
start_group.append(sg_jam)
start_group.append(sg_1p)
start_group.append(sg_arcade)
start_group.append(sg_2p)
start_group.append(sg_h)
start_group.append(sg_o)
start_group.append(sg_r)
start_group.append(sg_s)
start_group.append(sg_e)

arcade_group.append(ag_time)
arcade_group.append(ag_time_c)
arcade_group.append(ag_score)
arcade_group.append(ag_score_c)
arcade_group.append(ag_hiscore)
arcade_group.append(ag_hiscore_c)

arcade_bt_group.append(ag_bt_time)
arcade_bt_group.append(ag_bt_time_c)
arcade_bt_group.append(ag_bt_score)
arcade_bt_group.append(ag_bt_score_c)
arcade_bt_group.append(ag_bt_bonus)
arcade_bt_group.append(ag_bt_bonus_t)

game_over_group.append(gog_game)
game_over_group.append(gog_over)
game_over_group.append(gog_score)
game_over_group.append(gog_score_c)

new_hiscore_group.append(nhg_new)
new_hiscore_group.append(nhg_hiscore)
new_hiscore_group.append(nhg_hiscore_c)

horse_group.append(hg_time)
horse_group.append(hg_time_c)
horse_group.append(hg_p1)
horse_group.append(hg_p2)

# audio files
speaker = audioio.AudioOut(board.A0)

audio_file = {
	"space_jam": "/audio/space_jam.mp3",
	"whistle": "/audio/whistle.mp3",
	"countdown": "/audio/countdown.mp3",
	"game_over": "/audio/game_over.mp3",
	"hiscore": "/audio/hiscore.mp3"
}

space_jam_a = open(audio_file["space_jam"], "rb")
whistle_a = open(audio_file["whistle"], "rb")
countdown_a = open(audio_file["countdown"], "rb")
game_over_a = open(audio_file["game_over"], "rb")
hiscore_a = open(audio_file["hiscore"], "rb")

mp3stream = audiomp3.MP3Decoder(space_jam_a)

# button_1 pin and state
button_1 = digitalio.DigitalInOut(board.SCL)
button_1.direction = digitalio.Direction.INPUT
button_1.pull = digitalio.Pull.UP

# button_2 pin and state
button_2 = digitalio.DigitalInOut(board.SDA)
button_2.direction = digitalio.Direction.INPUT
button_2.pull = digitalio.Pull.UP

# break beam LED
break_beam = digitalio.DigitalInOut(board.A1)
break_beam.direction = digitalio.Direction.INPUT
break_beam.pull = digitalio.Pull.UP

# NeoPixels
led_pin = board.D25
num_leds = 54
leds = neopixel.NeoPixel(led_pin, num_leds, brightness = 0.20, auto_write = True)
rainbow = Rainbow(leds, speed = 0.1, period = 2, step = 1, precompute_rainbow = True)
solid_white = Solid(leds, color = WHITE)
solid_yellow = Solid(leds, color = YELLOW)
solid_red = Solid(leds, color = RED)
solid_green = Solid(leds, color = GREEN)
solid_black = Solid(leds, color = BLACK)
#blink = Blink(pixels, speed = 0.5, color = JADE)

# variables
screen_states = {
	1: "start_screen",
	2: "arcade_screen",
	3: "new_hiscore_screen",
	4: "game_over_screen"
}

button_states = {
	1: False,
	2: False
}

screen_state = "start_screen"
highest_score = "0"

def start_screen():
    global screen_state, highest_score

    # stop any previously playing audio
    if speaker.playing:
        speaker.stop()
        
    # set screen properties
    sg_1p.color = 0x00B3B3
    sg_arcade.color = 0xFFFFFF
    sg_2p.color = 0xB300B3
    sg_h.color = 0xFFFFFF
    sg_o.color = 0xFFFFFF
    sg_r.color = 0xFFFFFF
    sg_s.color = 0xFFFFFF
    sg_e.color = 0xFFFFFF

    # local variables
    labels_are_visible = False # if False show text, if True hide text
    reset_score_v = 0
    reset_score_t = 0
    blink_timer = 0
    blink_period = 0

    display.show(start_group)
    time.sleep(1)
    
    def checks():
        nonlocal labels_are_visible, blink_timer, blink_period
        # play the space_jam audio file
        if not speaker.playing:
            mp3stream.file = space_jam_a
            speaker.play(mp3stream)

        # blink the 1p arcade and 2p h.o.r.s.e text
        if time.time() >= blink_timer + blink_period:
            blink_timer = time.time()
            if labels_are_visible:
                labels_are_visible = False
                blink_period = 1
                sg_1p.color = 0x000000
                sg_arcade.color = 0x000000
                sg_2p.color = 0x000000
                sg_h.color = 0x000000
                sg_o.color = 0x000000
                sg_r.color = 0x000000
                sg_s.color = 0x000000
                sg_e.color = 0x000000
            else:
                labels_are_visible = True
                blink_period = 2
                sg_1p.color = 0x00B3B3
                sg_arcade.color = 0xFFFFFF
                sg_2p.color = 0xB300B3
                sg_h.color = 0xFFFFFF
                sg_o.color = 0xFFFFFF
                sg_r.color = 0xFFFFFF
                sg_s.color = 0xFFFFFF
                sg_e.color = 0xFFFFFF

    while screen_state == screen_states[1]:
        # LED animation
        rainbow.animate()
        
        # conduct checks to determine blinking and make sure sound if playing 
        checks()

        # reset the hiscore if the button is held for 5 seconds
        if not button_1.value and not button_states[1]:
            reset_score_v = time.time()
            button_states[1] = True
            while not button_1.value:
                # conduct checks
                checks()
                # Keep rainbow animation alive
                rainbow.animate()
                reset_score_t = time.time() - reset_score_v
                if reset_score_t == 5:
                    ag_hiscore_c.text = "0"
                    highest_score = "0"
                    get_set_hiscore(value = "0")
                    solid_white.animate() # indicate that the hiscore has been reset
                    button_states[1] = False # allow the button state to be changed to True after reset
                    reset_score_v = -1 # to be used to prevent entry to game after the 5 seconds
                    time.sleep(1)
                    break

        # change the state to arcade_screen when button 1 is pressed
        if button_states[1] and reset_score_v != -1:
            button_states[1] = False
            screen_state = screen_states[2] # breaks out of the loop

        # button_2 debounce and change the state to horse_screen
        if not button_2.value and not button_states[2]:
            button_states[2] = True

def arcade_screen():
    global screen_state, highest_score

    # stop any previously playing audio
    if speaker.playing:
        speaker.stop()

    # reset properties
    ag_time_c.text = "60"
    ag_time_c.color = 0x00B300      
    ag_score_c.text = "0"
    ag_score_c.color = 0xFFFFFF
    ag_hiscore.color = 0x00B3B3
    ag_hiscore_c.color = 0xB30000

    # local variables
    labels_are_visible = False
    blink_timer = time.time()
    blink_period = 0
    ball_scored = False
    beam_broken = False
    time_beam_restored = time.time()
    saved_hiscore = get_set_hiscore()
    ag_hiscore_c.text = saved_hiscore
    game_time = 60
    current_time = 0
    can_do_bonus = True if int(saved_hiscore) >= 20 else False # prevent the bonus time when the hiscore is 0 for the first game
    hiscore_beaten = False
    prev_time = 60

    # center the hiscore and hiscore text
    if int(saved_hiscore) <= 9:
        ag_hiscore.x = 7
        ag_hiscore_c.x = 52
    elif int(saved_hiscore) >= 10 and int(saved_hiscore) <= 99:
        ag_hiscore.x = 4
        ag_hiscore_c.x = 49
    elif int(saved_hiscore) >= 100:
        ag_hiscore.x = 1
        ag_hiscore_c.x = 46

    # center the time value text
    if int(ag_time_c.text) <= 9:
        ag_time_c.x = 11
    elif int(ag_time_c.text) >= 10 and int(ag_time_c.text) <= 60:
        ag_time_c.x = 8

    # center the score value text
    if int(ag_score_c.text) <= 9:
        ag_score_c.x = 43
    elif int(ag_score_c.text) >= 10 and int(ag_score_c.text) <= 99:
        ag_score_c.x = 40
    elif int(ag_score_c.text) >= 100:
        ag_score_c.x = 37

    display.show(arcade_group)
    time.sleep(1)

    # play the whistle audio file
    while not speaker.playing:
        mp3stream.file = whistle_a
        speaker.play(mp3stream)

    game_start_time = time.time()

    while screen_state == screen_states[2]:
        # update the time left in the round
        ag_time_c.text = str(game_time - int(time.time() - game_start_time))

        # difference between the saved high score and the game score
        score_diff = int(saved_hiscore) - int(ag_score_c.text)

        # center the time value text
        if int(ag_time_c.text) <= 9:
            ag_time_c.x = 11
        elif int(ag_time_c.text) >= 10 and int(ag_time_c.text) <= 60:
            ag_time_c.x = 8

        # check if the beam has been broken, a ball has been scored
        beam_broken = True if break_beam.value == 0 else False

        if beam_broken and not ball_scored:
            # increment the score if conditions are met
            if time.time() - time_beam_restored <= 0.1: # check the time between consecutive balls scored
                # if the time is less than 0.3, this should indicate an invalid score
                # time of 0.3 sec is assuming that two valid scores cannot be made within 0.3 seconds or less of each other
                pass
            else:
                ag_score_c.text = str(int(ag_score_c.text) + 1)
                # set score tracker variable to True
                ball_scored = True
        elif not beam_broken:
            if ball_scored:
                time_beam_restored = time.time() # after a ball is scored the beam is restored, get the time the beam was restored
                ball_scored = False

        # center the score value text
        if int(ag_score_c.text) <= 9:
            ag_score_c.x = 43
        elif int(ag_score_c.text) >= 10 and int(ag_score_c.text) <= 99:
            ag_score_c.x = 40
        elif int(ag_score_c.text) >= 100:
            ag_score_c.x = 37

        # bonus time
        if can_do_bonus:
            if score_diff <= 5 and score_diff >= 0: # game score is 5 points or less away from the hiscore
                # blink the hiscore title and hiscore count
                if time.time() >= blink_timer + blink_period:
                    blink_timer = time.time()
                    if labels_are_visible:
                        labels_are_visible = False
                        blink_period = 1
                        ag_hiscore.color = 0x000000
                        ag_hiscore_c.color = 0x000000
                    else:
                        labels_are_visible = True
                        blink_period = 1
                        ag_hiscore.color = 0x00B3B3
                        ag_hiscore_c.color = 0xB30000

            if score_diff < 0 and not hiscore_beaten and int(ag_time_c.text) < 31: # hiscore has been beaten and was not beaten before in this game
                hiscore_beaten = True

                # stop any previously playing audio
                if speaker.playing:
                    speaker.stop()

                # play the hiscore audio
                while not speaker.playing:
                    mp3stream.file = hiscore_a
                    speaker.play(mp3stream)

                # change score value color to pink
                ag_hiscore.color = 0x00B3B3 # in case the color was set to black before after blinking
                ag_hiscore_c.color = 0xB30000
                ag_score_c.color = 0xB3005A

                # add time if the score was beaten in set times
                if int(ag_time_c.text) >= 1 and int(ag_time_c.text) <= 10:
                    game_time += 30
                elif int(ag_time_c.text) >= 11 and int(ag_time_c.text) <= 20:
                    game_time += 20
                elif int(ag_time_c.text) >= 21 and int(ag_time_c.text) <= 30:
                    game_time += 10

                # go to the bonus time screen for 10 seconds
                ag_time_c.text, ag_score_c.text = arcade_bonus_screen(game_time, game_start_time, ag_score_c.text)
                display.show(arcade_group) # show arcade group after return

        # change the time value's color and RGB lights depending on time left in game
        if int(ag_time_c.text) <= 60 and int(ag_time_c.text) >= 21:
            ag_time_c.color = 0x00B300
            if not int(ag_time_c.text) % 2 and int(ag_time_c.text) != current_time: # the time left in the game is even
                current_time = int(ag_time_c.text)
                solid_green.animate()
            elif int(ag_time_c.text) != current_time:
                current_time = int(ag_time_c.text)
                solid_black.animate()

        elif int(ag_time_c.text) <= 20 and int(ag_time_c.text) >= 11:
            ag_time_c.color = 0xB3B300
            if int(ag_time_c.text) == 11:
                # stop any previously playing audio
                if speaker.playing:
                    speaker.stop()
                # play the countdown audio file
                mp3stream.file = countdown_a
                speaker.play(mp3stream)
            if not int(ag_time_c.text) % 2 and int(ag_time_c.text) != current_time: # the time left in the game is even
                current_time = int(ag_time_c.text)
                solid_yellow.animate()
            elif int(ag_time_c.text) != current_time:
                current_time = int(ag_time_c.text)
                solid_black.animate()

        elif int(ag_time_c.text) <= 10 and int(ag_time_c.text) >= 0:
            ag_time_c.color = 0xB30000
            if not int(ag_time_c.text) % 2 and int(ag_time_c.text) != current_time: # the time left in the game is even
                current_time = int(ag_time_c.text)
                solid_red.animate()
            elif int(ag_time_c.text) != current_time:
                current_time = int(ag_time_c.text)
                solid_black.animate()

        # update the hiscore value if the score is greater than the current hiscore value
        if int(ag_score_c.text) > int(saved_hiscore):
            highest_score = ag_score_c.text
            if not hiscore_beaten and int(ag_time_c.text) >= 31:
                hiscore_beaten = True
                ag_hiscore.color = 0x00B3B3 # in case the color was set to black before - after blinking
                ag_hiscore_c.color = 0xB30000
                # stop any previously playing audio
                if speaker.playing:
                    speaker.stop()
                # play the hiscore audio
                while not speaker.playing:
                    mp3stream.file = hiscore_a
                    speaker.play(mp3stream)

        # exit the game when the time is up
        if int(ag_time_c.text) <= 0:
            time.sleep(1) # allows the time value of 0 to be seen
            if int(highest_score) > int(saved_hiscore): # hiscore was beaten
                screen_state = screen_states[3]
                get_set_hiscore(value = ag_score_c.text) # save the hiscore
            else: # hiscore was not beaten
                screen_state = screen_states[4]

def arcade_bonus_screen(game_time, game_start_time, score):
    # set label properties
    ag_bt_score_c.text = score
    ag_bt_time_c.text = str(game_time - int(time.time() - game_start_time))
    ag_bt_score_c.color = 0xB3005A

    # show the bonus time group
    display.show(arcade_bt_group)

    # variables
    labels_are_visible = False
    blink_timer = time.time()
    blink_period = 1
    bt_start_time = time.time()
    bt_stay_time = 10
    current_time = 0
    ball_scored = False
    beam_broken = False
    time_beam_restored = time.time()
	
    # center the time value text
    if int(ag_bt_time_c.text) <= 9:
        ag_bt_time_c.x = 11
    elif int(ag_bt_time_c.text) >= 10 and int(ag_bt_time_c.text) <= 60:
        ag_bt_time_c.x = 8

    # center the score value text
    if int(ag_bt_score_c.text) <= 9:
        ag_bt_score_c.x = 43
    elif int(ag_bt_score_c.text) >= 10 and int(ag_bt_score_c.text) <= 99:
        ag_bt_score_c.x = 40
    elif int(ag_bt_score_c.text) >= 100:
        ag_bt_score_c.x = 37

    # stay in bonus time screen for time (seconds) specified in stay_time
    while time.time() < bt_start_time + bt_stay_time:
        rainbow.animate()
        # update the time
        ag_bt_time_c.text = str(game_time - int(time.time() - game_start_time))

        # check if the beam has been broken, a ball has been scored
        beam_broken = True if break_beam.value == 0 else False

        if beam_broken and not ball_scored:
            # increment the score if conditions are met
            if time.time() - time_beam_restored <= 0.1: # check the time between consecutive balls scored
                # if the time is less than 0.3, this should indicate an invalid score
                # time of 0.3 sec is assuming that two valid scores cannot be made within 0.3 seconds or less of each other
                pass
            else:
                ag_bt_score_c.text = str(int(ag_bt_score_c.text) + 1)
                # set score tracker variable to True
                ball_scored = True
        elif not beam_broken:
            if ball_scored:
                time_beam_restored = time.time() # after a ball is scored the beam is restored, get the time the beam was restored
                ball_scored = False

        # blink the bonus time text
        if time.time() >= blink_timer + blink_period:
            blink_timer = time.time()
            if labels_are_visible:
                labels_are_visible = False
                blink_period = 1
                ag_bt_bonus.color = 0x000000
                ag_bt_bonus_t.color = 0x000000
            else:
                labels_are_visible = True
                blink_period = 1
                ag_bt_bonus.color = 0x5A00B3
                ag_bt_bonus_t.color = 0x5A00B3

        # change the time value's color and RGB lights depending on time left in game
        if int(ag_bt_time_c.text) <= 60 and int(ag_bt_time_c.text) >= 21:
            ag_bt_time_c.color = 0x00B300
        if not int(ag_bt_time_c.text) % 2 and int(ag_bt_time_c.text) != current_time: # the time left in the game is even
            current_time = int(ag_bt_time_c.text)
            solid_green.animate()
        elif int(ag_bt_time_c.text) != current_time:
            current_time = int(ag_bt_time_c.text)
            solid_black.animate()

        elif int(ag_bt_time_c.text) <= 20 and int(ag_bt_time_c.text) >= 11:
            ag_bt_time_c.color = 0xB3B300
        if int(ag_bt_time_c.text) == 11:
            # stop any previously playing audio
            if speaker.playing:
                speaker.stop()
            # play the countdown audio file
            mp3stream.file = countdown_a
            speaker.play(mp3stream)
        if not int(ag_bt_time_c.text) % 2 and int(ag_bt_time_c.text) != current_time: # the time left in the game is even
            current_time = int(ag_bt_time_c.text)
            solid_yellow.animate()
        elif int(ag_bt_time_c.text) != current_time:
            current_time = int(ag_bt_time_c.text)
            solid_black.animate()

    return ag_bt_time_c.text, ag_bt_score_c.text

def game_over_screen():
	global screen_state

	# stop any previously playing audio
	if speaker.playing:
		speaker.stop()

	# play the game_over audio file
	while not speaker.playing:
		mp3stream.file = game_over_a
		speaker.play(mp3stream)

	# set text properties
	gog_score_c.text = ag_score_c.text

	# local variables
	labels_are_visible = False
	start_time = time.time()
	blink_timer = time.time()
	blink_period = 0

	# center the score value text
	if int(gog_score_c.text) <= 9:
		gog_score_c.x = 29
	elif int(gog_score_c.text) >= 10 and int(gog_score_c.text) <= 99:
		gog_score_c.x = 26
	elif int(gog_score_c.text) >= 100:
		gog_score_c.x = 23

	display.show(game_over_group)

	while time.time() - start_time <= 10:
		rainbow.animate()
		if time.time() >= blink_timer + blink_period:
			blink_timer = time.time()
			if labels_are_visible:
				labels_are_visible = False
				blink_period = 1
				gog_game.color = 0x000000
				gog_over.color = 0x000000
			else:
				labels_are_visible = True
				blink_period = 2
				gog_game.color = 0xB30000
				gog_over.color = 0xB30000

	screen_state = screen_states[1] # return to the start screen

def new_hiscore_screen():
	global screen_state, highest_score

	# stop any previously playing audio
	if speaker.playing:
		speaker.stop()

	# play the hiscore audio file
	while not speaker.playing:
		mp3stream.file = hiscore_a
		speaker.play(mp3stream)

	# set text properties
	nhg_hiscore_c.text = highest_score

	# local variables
	labels_are_visible = False
	start_time = time.time()
	blink_timer = time.time()
	blink_period = 0

	# center the hiscore value text
	if int(highest_score) <= 9:
		nhg_hiscore_c.x = 29
	elif int(highest_score) >= 10 and int(highest_score) <= 99:
		nhg_hiscore_c.x = 26
	elif int(highest_score) >= 100:
		nhg_hiscore_c.x = 23

	display.show(new_hiscore_group)

	while time.time() - start_time <= 10:  
		rainbow.animate()
		if time.time() >= blink_timer + blink_period:
			blink_timer = time.time()
			if labels_are_visible:
				labels_are_visible = False
				blink_period = 1
				nhg_new.color = 0x000000
			else:
				labels_are_visible = True
				blink_period = 2
				nhg_new.color = 0x00B300

	screen_state = screen_states[1] # go back to the start screen

def horse_screen():
	global screen_state

	button_states[2] = False # allow the button state to be changed to True after reset

	# reset properties
	hg_time_c.text = "10"
	hg_time_c.color = 0x00B300

	# center the time and time value text
	if int(hg_time_c.text) <= 9:
		hg_time.x = 16
		hg_time_c.x = 43
	elif int(hg_time_c.text) == 10:
		hg_time.x = 13
		hg_time_c.x = 40

	display.show(horse_group)
	time.sleep(1)

	screen_state = screen_states[1] # go back to the start screen

# variables
screens = {
	"start_screen": start_screen,
	"arcade_screen": arcade_screen,
	"new_hiscore_screen": new_hiscore_screen,
	"game_over_screen": game_over_screen,
	"horse_screen": horse_screen
}

# main loop, run the approriate screen function given the screen state
while True:
	screens[screen_state]()

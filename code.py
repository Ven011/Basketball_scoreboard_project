from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
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
new_hiscore_group = displayio.Group()
game_over_group = displayio.Group()
horse_group = displayio.Group()

# save hiscore to file
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

ag_time_c = label.Label(font_virtual_pet_sans, text = "60", color = 0x00B300)
ag_time_c.x = 8
ag_time_c.y = 16

ag_score = label.Label(font_ozone, text = "SCORE", color = 0x0000B3)
ag_score.x = 29
ag_score.y = 4

ag_score_c = label.Label(font_virtual_pet_sans, text = "0", color = 0xFFFFFF)
ag_score_c.x = 43
ag_score_c.y = 16

ag_hiscore = label.Label(font_virtual_pet_sans, text = "HISCORE", color = 0x00B3B3)
ag_hiscore.x = 7
ag_hiscore.y = 28

ag_hiscore_c = label.Label(font_virtual_pet_sans, text = get_set_hiscore(), color = 0xB30000)
ag_hiscore_c.x = 52
ag_hiscore_c.y = 28

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

new_hiscore_group.append(nhg_new)
new_hiscore_group.append(nhg_hiscore)
new_hiscore_group.append(nhg_hiscore_c)

game_over_group.append(gog_game)
game_over_group.append(gog_over)
game_over_group.append(gog_score)
game_over_group.append(gog_score_c)

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
leds = neopixel.NeoPixel(led_pin, num_leds, brightness = 0.20)
rainbow_sparkle = RainbowSparkle(leds, speed = 0.30, period = 5, num_sparkles = 27, precompute_rainbow = True)

# variables
screen_states = {
    1: "starting_screen",
    2: "arcade_game_screen",
    3: "new_highscore_screen",
    4: "gameover_screen"
}

button_states = {
    1: False,
    2: False
}

screen_state = "starting_screen"
highest_score = "0"

def starting_screen():
    global screen_state, highest_score
    # stop any previously playing audio
    if speaker.playing:
        speaker.stop()
    
    # play the space jam audio
    mp3stream.file = open(audio_file["space_jam"], "rb")
    speaker.play(mp3stream)
    
    # local variables
    reset_score_v = 0
    reset_score_t = 0
    labels_are_visible = False # if False, show them, if True, hide them
    blink_timer = 0
    blink_period = 0
    
    time.sleep(0.5)
    display.show(start_group)
    
    while screen_state == screen_states[1]:
        # led animation
        rainbow_sparkle.animate()
        
        # make sure the space jam audio is playing
        if not speaker.playing:
            mp3stream.file = open(audio_file["space_jam"], "rb")
            speaker.play(mp3stream)
            
        # blink the 1p arcade and 2p h.o.r.s.e text
        if time.time() >= blink_timer + blink_period:
            blink_timer = time.time()
            if labels_are_visible:
                blink_period = 1
                labels_are_visible = False
                sg_1p.color = 0x000000
                sg_arcade.color = 0x000000
                sg_2p.color = 0x000000
                sg_h.color = 0x000000
                sg_o.color = 0x000000
                sg_r.color = 0x000000
                sg_s.color = 0x000000
                sg_e.color = 0x000000
            else:
                blink_period = 2
                labels_are_visible = True
                sg_1p.color = 0x00B3B3
                sg_arcade.color = 0xFFFFFF
                sg_2p.color = 0xB300B3
                sg_h.color = 0xFFFFFF
                sg_o.color = 0xFFFFFF
                sg_r.color = 0xFFFFFF
                sg_s.color = 0xFFFFFF
                sg_e.color = 0xFFFFFF
        
        # reset high score is held for 5 seconds
        if not button_1.value and not button_states[1]:
            reset_score_v = time.time()
            button_states[1] = True
            while not button_1.value:
                reset_score_t = time.time() - reset_score_v
                if reset_score_t == 5:
                    # indicate that the score has been reset
                    leds.fill((0, 255, 0))
                    ag_hiscore_c.text = "0"
                    highest_score = "0"
                    get_set_hiscore(value = "0")
                    button_states[1] = False # allow button state to be changed to true after reset
                    reset_score_v = -1 # to be used to prevent entry to game after the 5 seconds
                    time.sleep(3)
                    break
                
        # button_2 debounce
        if not button_2.value and not button_states[2]:
            button_states[2] = True
            
        # change the state to arcade_game when button 1 is pressed once
        if button_states[1] and reset_score_v != -1:
            button_states[1] = False
            screen_state = screen_states[2] # breaks out of the loop
            
def arcade_game():
    global screen_state, highest_score
    # stop any previously playing audio
    if speaker.playing:
        speaker.stop()
    
    # play the whistle audio. make sure the whistle audio plays before proceeding
    while not speaker.playing:
        mp3stream.file = open(audio_file["whistle"], "rb")
        speaker.play(mp3stream)
    
    # local variables
    ball_scored = False
    beam_broken = False
    saved_hiscore = get_set_hiscore()
    ag_hiscore_c.text = saved_hiscore
    game_time = 60
    ## labels_are_visible = False
    time_beam_restored = time.time()
    curr_time = 0
    
    # reset properties
    ag_time_c.text = "60"
    ag_time_c.color = 0x00B300
    ag_score_c.text = "0"
    ag_score_c.color = 0xFFFFFF
    
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
        
    time.sleep(0.5)
    display.show(arcade_group)
    game_start_time = time.time()
    
    while screen_state == screen_states[2]:
        # update the time left in the round
        ag_time_c.text = str(game_time - int(time.time() - game_start_time))

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
            
        # check if the beam has been broken/ a ball has been scored
        beam_broken = True if break_beam.value == 0 else False

        if beam_broken and not ball_scored:
            # increment the score if conditions are met
            if time.time() - time_beam_restored <= 0.3: # check the time between consecutive balls scored
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
                
        # change the time value's color and RGB lights depending on time left in game
        if int(ag_time_c.text) <= 60 and int(ag_time_c.text) >= 21:
            if int(ag_time_c.text) == 60:
                ag_time_c.color = 0x00B300
            if not int(ag_time_c.text) % 2 and int(ag_time_c.text) != curr_time: # the time left in the game is even
                curr_time = int(ag_time_c.text)
                leds.fill((0, 255, 0))
            elif int(ag_time_c.text) != curr_time:
                curr_time = int(ag_time_c.text)
                leds.fill((0, 0, 0))

        elif int(ag_time_c.text) <= 20 and int(ag_time_c.text) >= 11:
            if int(ag_time_c.text) == 20:
                ag_time_c.color = 0xB3B300
            if int(ag_time_c.text) == 11:
                mp3stream.file = open(audio_file["countdown"], "rb")
                speaker.play(mp3stream)
            if not int(ag_time_c.text) % 2 and int(ag_time_c.text) != curr_time: # the time left in the game is even
                curr_time = int(ag_time_c.text)
                leds.fill((255, 255, 0))
            elif int(ag_time_c.text) != curr_time:
                curr_time = int(ag_time_c.text)
                leds.fill((0, 0, 0))

        elif int(ag_time_c.text) <= 10 and int(ag_time_c.text) >= 0:
            if int(ag_time_c.text) == 10:
                ag_time_c.color = 0xB30000
            if not int(ag_time_c.text) % 2 and int(ag_time_c.text) != curr_time: # the time left in the game is even
                curr_time = int(ag_time_c.text)
                leds.fill((255, 0, 0))
            elif int(ag_time_c.text) != curr_time:
                curr_time = int(ag_time_c.text)
                leds.fill((0, 0, 0))
                
        # update the hiscore value if the score is greater than the current hiscore value
        if int(ag_score_c.text) > int(saved_hiscore):
            highest_score = ag_score_c.text
            
        # exit the game when the time is up
        if int(ag_time_c.text) == 0:
            time.sleep(1) # allows the time value of 0 to be seen
            
            if int(highest_score) > int(saved_hiscore): # highscore was beaten
                screen_state = screen_states[3]
                # save the highest score
                get_set_hiscore(value = ag_score_c.text)
            elif int(highest_score) <= int(saved_hiscore): # highscore was not beaten
                screen_state = screen_states[4]
    
def new_highscore_screen():
    global screen_state, highest_score
    # stop any previously playing audio
    if speaker.playing:
        speaker.stop()
    
    # play the hiscore audio. make sure the audio plays before proceeding
    while not speaker.playing:
        mp3stream.file = open(audio_file["hiscore"], "rb")
        speaker.play(mp3stream)
    
    # set label properties
    nhg_hiscore_c.text = highest_score
    
    # local variables
    blink_timer = time.time()
    start_time = time.time()
    labels_are_visible = False
    blink_period = 0
    
    # center the hiscore value text
    if int(highest_score) <= 9:
        nhg_hiscore_c.x = 29
    elif int(highest_score) >= 10 and int(highest_score) <= 99:
        nhg_hiscore_c.x = 26
    elif int(highest_score) >= 100:
        nhg_hiscore_c.x = 23
        
    display.show(new_hiscore_group)
    
    # blink the new text
    while time.time() - start_time <= 10:
        if time.time() >= blink_timer + blink_period:
            blink_timer = time.time()
            if labels_are_visible:
                blink_period = 1
                labels_are_visible = False
                nhg_new.color = 0x000000
            else:
                blink_period = 2
                labels_are_visible = True
                nhg_new.color = 0x00B300
    
    screen_state = screen_states[1] # go back to start screen

def game_over_screen():
    global screen_state
    # stop any previously playing audio
    if speaker.playing:
        speaker.stop()
    
    # play the game_over audio. make sure the audio plays before proceeding
    while not speaker.playing:
        mp3stream.file = open(audio_file["game_over"], "rb")
        speaker.play(mp3stream)
    
    # set label properties
    gog_score_c.text = ag_score_c.text
    
    # local variables
    blink_timer = time.time()
    blink_period = 0
    start_time = time.time()
    labels_are_visible = False
    
    # center the score value text
    if int(gog_score_c.text) <= 9:
        gog_score_c.x = 29
    elif int(gog_score_c.text) >= 10 and int(gog_score_c.text) <= 99:
        gog_score_c.x = 26
    elif int(gog_score_c.text) >= 100:
        gog_score_c.x = 23
        
    display.show(game_over_group)

    while time.time() - start_time <= 10:
        if time.time() >= blink_timer + blink_period:
            blink_timer = time.time()
            if labels_are_visible:
                blink_period = 1
                labels_are_visible = False
                gog_game.color = 0x000000
                gog_over.color = 0x000000
            else:
                blink_period = 2
                labels_are_visible = True
                gog_game.color = 0xB30000
                gog_over.color = 0xB30000
                
    screen_state = screen_states[1] # return to the start screen

# more variables
screens = {
    "starting_screen": starting_screen,
    "arcade_game_screen": arcade_game,
    "new_highscore_screen": new_highscore_screen,
    "gameover_screen": game_over_screen
}

# Main loop. Run the approriate screen function given the screen state
while True:
    screens[screen_state]()
            
            
        

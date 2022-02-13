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
arcade_bt_group = display.Group()
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

# variables
screen_states = {
    1: "starting_screen",
    2: "arcade_game"
}

button_states = {
    1: False,
    2: False
}

screen_state = "starting_screen"

def starting_screen():
    global screen_state
    # play the space jam audio
    mp3stream.file = open(audio_file["space_jam"], "rb")
    speaker.play(mp3stream)
    
    # set LED color to white
    leds.fill((255, 255, 255))
    
    # local variables
    reset_score_v = 0
    reset_score_t = 0
    labels_are_visible = False # if False, show them, if True, hide them
    blink_timer = 0
    blink_period = 0
    
    time.sleep(0.5)
    display.show(start_group)
    
    while screen_state == screen_states[1]:
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
                    ## ag_hiscore_c.text = "0"
                    get_set_hiscore(value = "0")
                    button_states[1] = False # allow button state to be changed to true after reset
                    reset_score_v = -1 # to be used to prevent entry to game after the 5 seconds
                    time.sleep(3)
                    break
                
        # button_2 debounce
        if not button_2.value and not button_2_state:
            button_2_state = True
            
        # change the state to arcade_game when button 1 is pressed once
        if button_states[1] and reset_score_v != -1:
            screen_state = screen_states[2] # breaks out of the loop
            
def arcade_game():
    global screen_state
    leds.fill((0, 0, 255))
    for _ in range(5): # wait 5 seconds
        time.sleep(1)
        
    screen_state = screen_states[1] # return to the start group

# more variables
screens = {
    "starting_screen": starting_screen,
    "arcade_game": arcade_game
}

# Main loop. Run the approriate screen function given the screen state
while True:
    screens[screen_state]()
            
            
        
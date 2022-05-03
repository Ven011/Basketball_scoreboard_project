import displayio
import rgbmatrix
import board
import framebufferio
import audioio
import audiomp3
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from time import time, monotonic
import digitalio
import neopixel_spi as neopixel
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.solid import Solid
from pololu_tic_36v4 import TicI2C

# RGBMatrix setup
displayio.release_displays()

# hoop setup
tic = TicI2C()

matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=32,
    bit_depth=1,
    rgb_pins=[board.D2, board.D3, board.D4, board.D5, board.D6, board.D7],
    addr_pins=[board.A5, board.A1, board.A2, board.A3],
    clock_pin=board.A4,
    latch_pin=board.D10,
    output_enable_pin=board.D9
)
display = framebufferio.FramebufferDisplay(matrix)

# display groups
sg = displayio.Group()
cdg = displayio.Group()
ag = displayio.Group()
btg = displayio.Group()
gog = displayio.Group()
nhg = displayio.Group()

# save hiscore
def get_set_hiscore(value=-1):
    if value >= 0:
        hiscore_file = open("/temp/hiscore.txt", "w")
        hiscore_file.write(str(value))
        hiscore_file.close()
    else:
        hiscore_file = open("/temp/hiscore.txt", "r")
        score = hiscore_file.read()
        hiscore_file.close()
        return score

# font setup
ozone = bitmap_font.load_font("/fonts/ozone.pcf")
virtual_pet_sans = bitmap_font.load_font("/fonts/virtual_pet_sans.pcf")

# start graphics
sg_space = label.Label(ozone, text="SPACE", color=0x00B300, x=2, y=4)
sg_jam = label.Label(ozone, text="JAM", color=0x00B300, x=40, y=4)
sg_1p = label.Label(virtual_pet_sans, text="1P", color=0x00B3B3, x=6, y=18)
sg_arcade = label.Label(virtual_pet_sans, text="ARCADE", color=0xFFFFFF, x=21, y=18)
sg_2p = label.Label(virtual_pet_sans, text="2P", color=0xB300B3, x=6, y=28)
sg_h = label.Label(virtual_pet_sans, text="H.", color=0xFFFFFF, x=21, y=28)
sg_o = label.Label(virtual_pet_sans, text="O.", color=0xFFFFFF, x=29, y=28)
sg_r = label.Label(virtual_pet_sans, text="R.", color=0xFFFFFF, x=37, y=28)
sg_s = label.Label(virtual_pet_sans, text="S.", color=0xFFFFFF, x=45, y=28)
sg_e = label.Label(virtual_pet_sans, text="E", color=0xFFFFFF, x=53, y=28)

# countdown graphics
cdg_shoot = label.Label(virtual_pet_sans, text="SHOOT", color=0xFFFFFF, x=17, y=4)
cdg_time = label.Label(virtual_pet_sans, text="TIME", color=0xFFFF00, x=1, y=13)
cdg_time_c = label.Label(virtual_pet_sans, color=0xB30000, x=63, y=13, label_direction="RTL")
cdg_score = label.Label(virtual_pet_sans, text="SCORE", color=0xFFFF00, x=1, y=21)
cdg_score_c = label.Label(virtual_pet_sans, color=0x00B300, x=63, y=21, label_direction="RTL")
cdg_hiscore = label.Label(virtual_pet_sans, text="HISCORE", color=0x00B3B3, x=1, y=29)
cdg_hiscore_c = label.Label(virtual_pet_sans, text=get_set_hiscore(), color=0x00B3B3, x=63, y=29, label_direction="RTL")

# arcade graphics
ag_shoot = label.Label(virtual_pet_sans, text="SHOOT", color=0xFFFFFF, x=17, y=4)
ag_time = label.Label(virtual_pet_sans, text="TIME", color=0xFFFF00, x=1, y=13)
ag_time_c = label.Label(virtual_pet_sans, color=0xB30000, x=63, y=13, label_direction="RTL")
ag_score = label.Label(virtual_pet_sans, text="SCORE", color=0xFFFF00, x=1, y=21)
ag_score_c = label.Label(virtual_pet_sans, color=0x00B300, x=63, y=21, label_direction="RTL")
ag_hiscore = label.Label(virtual_pet_sans, text="HISCORE", color=0x00B3B3, x=1, y=29)
ag_hiscore_c = label.Label(virtual_pet_sans, text=get_set_hiscore(), color=0x00B3B3, x=63, y=29, label_direction="RTL")

# bonus time graphics
bt_shoot = label.Label(virtual_pet_sans, text="SHOOT", color=0xFFFFFF, x=17, y=4)
bt_time = label.Label(virtual_pet_sans, text="TIME", color=0xFFFF00, x=1, y=13)
bt_time_c = label.Label(virtual_pet_sans, color=0xB30000, x=63, y=13, label_direction="RTL")
bt_score = label.Label(virtual_pet_sans, text="SCORE", color=0xFFFF00, x=1, y=21)
bt_score_c = label.Label(virtual_pet_sans, color=0x00B300, x=63, y=21, label_direction="RTL")
bt_bonus = label.Label(virtual_pet_sans, text="BONUS", color=0x00FF00, x=4, y=29)
bt_bonus_t = label.Label(virtual_pet_sans, text="TIME", color=0x00FF00, x=37, y=29)

# game over graphics
gog_game = label.Label(ozone, text="GAME", color=0xB30000, x=2, y=5)
gog_over = label.Label(ozone, text="OVER", color=0xB30000, x=35, y=5)
gog_score = label.Label(virtual_pet_sans, text="SCORE", color=0x00B3B3, x=17, y=17)
gog_score_c = label.Label(virtual_pet_sans, color=0xFFFFFF)

# new hiscore graphics
nhg_new = label.Label(ozone, text="NEW", color=0x00B300, x=21, y=5)
nhg_hiscore = label.Label(virtual_pet_sans, text="HISCORE", color=0x00B3B3, x=11, y=17)
nhg_hiscore_c = label.Label(virtual_pet_sans, color=0xFFFFFF)

# add graphics to the display groups
sg.append(sg_space)
sg.append(sg_jam)
sg.append(sg_1p)
sg.append(sg_arcade)
sg.append(sg_2p)
sg.append(sg_h)
sg.append(sg_o)
sg.append(sg_r)
sg.append(sg_s)
sg.append(sg_e)

cdg.append(cdg_shoot)
cdg.append(cdg_time)
cdg.append(cdg_time_c)
cdg.append(cdg_score)
cdg.append(cdg_score_c)
cdg.append(cdg_hiscore)
cdg.append(cdg_hiscore_c)

ag.append(ag_shoot)
ag.append(ag_time)
ag.append(ag_time_c)
ag.append(ag_score)
ag.append(ag_score_c)
ag.append(ag_hiscore)
ag.append(ag_hiscore_c)

btg.append(bt_shoot)
btg.append(bt_time)
btg.append(bt_time_c)
btg.append(bt_score)
btg.append(bt_score_c)
btg.append(bt_bonus)
btg.append(bt_bonus_t)

gog.append(gog_game)
gog.append(gog_over)
gog.append(gog_score)
gog.append(gog_score_c)

nhg.append(nhg_new)
nhg.append(nhg_hiscore)
nhg.append(nhg_hiscore_c)

# audio setup
speaker = audioio.AudioOut(board.A0)
audio_file = {
    "space_jam": "/audio/space_jam.mp3",
    "whistle": "/audio/whistle.mp3",
    "countdown": "/audio/countdown.mp3",
    "game_over": "/audio/game_over.mp3",
    "hiscore": "/audio/hiscore.mp3"
}
mp3stream = audiomp3.MP3Decoder(open(audio_file["space_jam"], "rb"))
speaker.play(mp3stream)

# NeoPixel setup
pixels = neopixel.NeoPixel_SPI(board.SPI(), 53, brightness=0.2)
rainbow = Rainbow(pixels, speed=0.1, period=2, step=1)
colorcycle = ColorCycle(pixels, 2.0, colors=[0xFFFFFF, 0xB30000, 0x00B300, 0x0000B3])
solid_white = Solid(pixels, color=0xFFFFFF)
solid_green = Solid(pixels, color=0x00B300)
solid_yellow = Solid(pixels, color=0xB3B300)
solid_red = Solid(pixels, color=0xB30000)
solid_black = Solid(pixels, color=0x000000)

# arcade button setup
btn_arcade = digitalio.DigitalInOut(board.D8)
btn_arcade.direction = digitalio.Direction.INPUT
btn_arcade.pull = digitalio.Pull.UP

# reset button setup
btn_reset = digitalio.DigitalInOut(board.D11)
btn_reset.direction = digitalio.Direction.INPUT
btn_reset.pull = digitalio.Pull.UP

# top sensor setup
sen_top = digitalio.DigitalInOut(board.D0)
sen_top.direction = digitalio.Direction.INPUT
sen_top.pull = digitalio.Pull.UP

# bottom sensor setup
sen_btm = digitalio.DigitalInOut(board.D1)
sen_btm.direction = digitalio.Direction.INPUT
sen_btm.pull = digitalio.Pull.UP

# hoop movement setup
tic.control_hoop(max_speed = 300000000, starting_speed = 0, max_acceleration = 500000000, max_deceleration = 500000000) # the tic. ones are called from a TicI2C() class in an .mpy library

# variables
scrn_states = {
    1: "start_scrn",
    2: "countdown_scrn",
    3: "arcade_scrn",
    4: "game_over_scrn",
    5: "new_hiscore_scrn"
}

button_states = {
    1: False,
    2: False
}

label_sliding_vars = {
    "label": None,
    "shoot_x": 17,
    "prev_time": monotonic(),
    "wall": True
}

blink_labels = {
    "ag_hiscore": {
        "blink": False,
        "color": 0x00B3B3,
        "labels": {
            1: ag_hiscore,
            2: ag_hiscore_c
        } 
    },
    "bt_bonus": {
        "blink": False,
        "color": 0x00FF00,
        "labels": {
            1: bt_bonus,
            2: bt_bonus_t
        }
    },
    "gog": {
        "blink": False,
        "color": 0xB30000,
        "labels": {
            1: gog_game,
            2: gog_over
        }
    },
    "nhg_new": {
        "blink": False,
        "color": 0x00B300,
        "labels": {
            1: nhg_new
        }
    }
}
blink_vrs = {
    "blink_timer": time(),
    "labels_are_visible": True
}

scrn_state = "start_scrn"
highest_score = 0

def animate_label():
    global label_sliding_vars
    
    lsv = label_sliding_vars    
    # variables
    label_min_x = 1
    label_max_x = 28 # maximum x position the shoot value should slide to
    
    # move shoot label along the screen
    if (monotonic() - lsv["prev_time"]) >= 0.08: # check whether 0.08 seconds have passed
        if lsv["wall"]:
            lsv["shoot_x"] += 1
            if lsv["shoot_x"] == label_max_x:
                lsv["wall"] = not lsv["wall"]
                
        elif not lsv["wall"]:
            lsv["shoot_x"] -= 1
            if lsv["shoot_x"] == label_min_x:
                lsv["wall"] = not lsv["wall"]
        # update the previous time
        lsv["prev_time"] = monotonic()
        
    # update the label position
    lsv["label"].x = lsv["shoot_x"]

def handle_blink():
    global blink_labels, blink_vrs
    
    """
    This function blinks any labels that are called to blink.
    - The variables used to blink the labels are accessed from the global scope in order to allow this function to be called from anywhere
    """
    
    # blink the labels
    if time() >= blink_vrs["blink_timer"] + 1:
        blink_vrs["blink_timer"] = time()
        if blink_vrs["labels_are_visible"]:
            blink_vrs["labels_are_visible"] = False
            # set the color of all the labels that need to be blinked to black
            for k, v in blink_labels.items():
                if v["blink"]:
                    for key, value in blink_labels[k]["labels"].items():
                        value.color = 0x000000
                    
        else:
            blink_vrs["labels_are_visible"] = True
            # set the color of all the labels that need to be blinked to their default color
            for k, v in blink_labels.items():
                if v["blink"]:
                    for key, value in blink_labels[k]["labels"].items():
                        value.color = blink_labels[k]["color"]

def move_hoop(should_i_go, hoop_index, time_left):
    hoop_position = [-100000, 100000]
    bg_tasks = [animate_label]

    # move hoop
    if should_i_go and time_left > 1:
        tic.go_target(hoop_position[hoop_index], bg_task=bg_tasks)
        should_i_go = False
    
    # check if we have arrived at the position we were going
    if tic.get_current_position() == tic.centre + hoop_position[hoop_index]:
        should_i_go = True
        hoop_index = not hoop_index
    
    # stop hoop movement when the game is coming to an end
    if time_left <= 0:
        tic.halt_set_position()
    
    
    return should_i_go, hoop_index

def invert_string(string):
    inv_string = ""
    
    for index in range(len(string)):
        # concatenate the inverse string with elements of the string starting from the last string
        inv_string = inv_string + string[(index * -1) + len(string) - 1]
        
    return inv_string

def check_sensors(sen_triggered, sen_top_state, sen_btm_state, score):
    # prevent point if both sensors detect an object simultaneously
    # combined_sen_state = False if not sen_top.value and not sen_btm.value else True

    # # check if the top sensor is triggered
    # if not sen_top.value and not sen_top_state and combined_sen_state:
    #     sen_top_state = True
    #     sen_triggered += 1
    # if sen_top.value and sen_top_state and sen_triggered == 1:
    #     sen_triggered += 1

    # check if the bottom sensor is triggered
    if not sen_btm.value and not sen_btm_state: # and sen_triggered == 2:
        sen_btm_state = True
        sen_triggered += 1
    if sen_btm.value and sen_btm_state and sen_triggered == 1:
        sen_triggered += 1

    # add point if both sensors have been triggered consecutively
    if sen_triggered == 2:
        sen_top_state = False
        sen_btm_state = False
        sen_triggered = 0
        # check whether the top sensor detects the ball
        if not sen_top.value:  # it does
            pass
        else:  # it does not
            score += 8

    return sen_triggered, sen_top_state, sen_btm_state, score

def handle_audio(time_left):
    if time_left >= 21 and time_left <= 60:
        solid_green.animate()
        if time_left == 60:
            if not speaker.playing:
                mp3stream.file = open(audio_file["whistle"], "rb")
                speaker.play(mp3stream)
    if time_left >= 11 and time_left <= 20:
        solid_yellow.animate()
    if time_left >= 0 and time_left <= 10:
        solid_red.animate()
        if time_left == 10:
            if not speaker.playing:
                mp3stream.file = open(audio_file["countdown"], "rb")
                speaker.play(mp3stream)

def start_scrn():
    global scrn_state, highest_score

    # variables
    labels_are_visible = False
    blink_timer = 0
    blink_period = 0
    reset_score = False

    display.show(sg)

    while scrn_state == scrn_states[1]:
        colorcycle.animate()

        if time() >= blink_timer + blink_period:
            blink_timer = time()
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
        
        if not speaker.playing:
            mp3stream.file = open(audio_file["space_jam"], "rb")
            speaker.play(mp3stream)
        
        # check if the reset button is low
        if not btn_reset.value and not button_states[2] and not reset_score:
            button_states[2] = True

        # reset the hiscore if the reset button is pressed
        if button_states[2]:
            button_states[2] = False
            reset_score = True
            solid_black.animate()
                
        # check if the arcade btn is low
        if not btn_arcade.value and not button_states[1]:
            button_states[1] = True

        # switch to the arcade scrn
        if button_states[1]:
            button_states[1] = False
            if speaker.playing:
                speaker.stop()
                
            # reset the hiscore if we need to 
            if reset_score:
                ag_hiscore_c.text = "0"
                get_set_hiscore(value=0)
            
            scrn_state = scrn_states[2]

def countdown_scrn():
    global scrn_state

    solid_green.animate()

    # set properties
    cdg_time_c.text = invert_string("3")
    cdg_score_c.text = invert_string("0")
    label_sliding_vars["label"] = cdg_shoot

    # variables
    countdown_time = 3
    saved_hiscore = int(get_set_hiscore())
    cdg_hiscore_c.text = invert_string(str(saved_hiscore))
    
    time_left = 3

    display.show(cdg)
    
    s_time = time()
    while time() - s_time < 1:
        animate_label()
        cdg_shoot.x = label_sliding_vars["shoot_x"]
    
    countdown_timer = time()

    while scrn_state == scrn_states[2]:
        # update the time left in the countdown
        time_left = (countdown_time - int(time() - countdown_timer))
        cdg_time_c.text = invert_string(str(time_left))
        
        # move shoot label
        animate_label()
        cdg_shoot.x = label_sliding_vars["shoot_x"]

        # switch to the arcade scrn
        if time_left == 1:
            s_time = time()
            while time() - s_time < 1: # pause for 1 second
                animate_label()
                cdg_shoot.x = label_sliding_vars["shoot_x"]
            scrn_state = scrn_states[3]

def arcade_scrn():
    global scrn_state, highest_score, label_sliding_vars

    # set properties
    ag_time_c.text = invert_string("60")
    ag_score_c.text = invert_string("0")
    ag_hiscore.color = 0x00B3B3
    ag_hiscore_c.color = 0x00B3B3
    label_sliding_vars["label"] = ag_shoot
    ag_shoot.x = label_sliding_vars["shoot_x"]

    # variables
    game_time = 60
    saved_hiscore = int(get_set_hiscore())
    ag_hiscore_c.text = invert_string(str(saved_hiscore))
    can_do_bonus = True if saved_hiscore >= 20 else False # prevent the bonus time when the hiscore is 0 for the first game
    hiscore_beaten = False
    sen_triggered = 0
    sen_top_state = False
    sen_btm_state = False

    time_left = 60
    game_score = 0
    
    hoop_index = 0 # used for hoop movement
    should_i_go = True

    display.show(ag)
    game_timer = time()

    while scrn_state == scrn_states[3]:
        # update the time left in the game
        time_left = (game_time - int(time() - game_timer))
        ag_time_c.text = invert_string(str(time_left))
        
        sen_triggered, sen_top_state, sen_btm_state, game_score = check_sensors(sen_triggered, sen_top_state, sen_btm_state, game_score)
        
        ag_score_c.text = invert_string(str(game_score))

        # difference between the saved high score and the game score
        score_diff = saved_hiscore - game_score

        # bonus time
        if can_do_bonus:
            if score_diff <= 5 and score_diff >= 0:
                # blink the ag_hiscore labels
                blink_labels["ag_hiscore"]["blink"] = True
            else:
                # don't blink the ag_hiscore labels
                blink_labels["ag_hiscore"]["blink"] = False

            # hiscore has been beaten and was not beaten before in this game
            if score_diff < 0 and not hiscore_beaten and time_left <= 30:
                hiscore_beaten = True

                ag_hiscore.color = 0x000000
                ag_hiscore_c.color = 0x000000

                mp3stream.file = open(audio_file["hiscore"], "rb")
                speaker.play(mp3stream)

                # add time when the score is beaten
                if time_left >= 1 and time_left <= 10:
                    game_time += 30
                elif time_left >= 11 and time_left <= 20:
                    game_time += 20
                elif time_left >= 21 and time_left <= 30:
                    game_time += 10

                # go to the bonus time scrn for 10 seconds
                game_score, time_left = arcade_bonus_scrn(game_time, game_timer, game_score)

                # update labels
                ag_score_c.text = invert_string(str(game_score))
                ag_time_c.text = invert_string(str(time_left))
                ag_shoot.x = label_sliding_vars["shoot_x"]
                label_sliding_vars["label"] = ag_shoot
                
                ag_hiscore.color = 0x00B3B3
                ag_hiscore_c.color = 0x00B3B3

                display.show(ag)

        # play specific audio given time
        handle_audio(time_left)
        
        # slide the shoot label back and forth
        animate_label()
        ag_shoot.x = label_sliding_vars["shoot_x"]
    
        # move the hoop
        should_i_go, hoop_index = move_hoop(should_i_go, hoop_index, time_left)            

        # check if the previously set hiscore has been beaten
        if game_score > saved_hiscore:
            highest_score = game_score
            if not hiscore_beaten and time_left >= 1:
                hiscore_beaten = True
                ag_hiscore.color = 0x00B3B3
                ag_hiscore_c.color = 0x00B3B3
                mp3stream.file = open(audio_file["hiscore"], "rb")
                speaker.play(mp3stream)

        # exit the game when the time is up
        if time_left <= 0:
            s_time = time()
            while time() - s_time < 1:
                # slide the shoot label back and forth
                animate_label()
                ag_shoot.x = label_sliding_vars["shoot_x"]
            if highest_score > saved_hiscore: # hiscore was beaten
                scrn_state = scrn_states[5]
                get_set_hiscore(value=game_score) # save the hiscore
            else: # hiscore was not beaten
                scrn_state = scrn_states[4]

def arcade_bonus_scrn(game_time, game_timer, score):
    global label_sliding_vars
    
    # set properties
    bt_bonus.color = 0x000000
    bt_bonus_t.color = 0x000000
    bt_score_c.text = invert_string(str(score))
    label_sliding_vars["label"] = bt_shoot
    bt_shoot.x = label_sliding_vars["shoot_x"]
    
    start_time = (game_time - int(time() - game_timer)) + 1
    exception = 0.5
    # don't start bonus time until the remainder of the past second has fully passed
    while (game_time - int(time() - game_timer)) == start_time - 1:
        # make an exception if the remainder of the past seconds is greater than the exception time
        if start_time - (game_time - (time() - game_timer)) > exception:
            break
        else:
            pass

    # variables
    bt_start_time = time()
    bt_stay_time = 10
    sen_triggered = 0
    sen_top_state = False
    sen_btm_state = False
    
    time_left = (game_time - int(time() - game_timer))
    bt_time_c.text = invert_string(str(time_left)) # needs to come after the loop above
    
    game_score = score

    display.show(btg)

    # stop any previous audio
    if speaker.playing:
        speaker.stop()
    # play hiscore audio file    
    mp3stream.file = open(audio_file["hiscore"], "rb")
    speaker.play(mp3stream)
    
    # give command to blink labels
    blink_labels["bt_bonus"]["blink"] = True

    # stay in the bonus time scrn for the time specified in stay_time
    while time() < bt_start_time + bt_stay_time:
        rainbow.animate()
        
        # slide the shoot label back and forth
        animate_label()
        bt_shoot.x = label_sliding_vars["shoot_x"]

        # update the time
        time_left = (game_time - int(time() - game_timer))
        bt_time_c.text = invert_string(str(time_left))
        
        # handle scoring
        sen_triggered, sen_top_state, sen_btm_state, game_score = check_sensors(sen_triggered, sen_top_state, sen_btm_state, game_score)
        bt_score_c.text = invert_string(str(game_score))

        # blink the bt_bonus and bt_bonus_t labels
        handle_blink()

    # give command to stop blinking bt_bonus labels
    blink_labels["bt_bonus"]["blink"] = False
    
    return game_score, time_left

def game_over_scrn():
    global scrn_state

    # set properties
    gog_score_c.text = invert_string(ag_score_c.text)

    # variables
    start_time = time()
    bg_tasks = [rainbow.animate, handle_blink] # functions to be called while the hoop centers

    # center the score value label
    if int(gog_score_c.text) <= 9:
        gog_score_c.x = 29
        gog_score_c.y = 27
    elif int(gog_score_c.text) >= 10 and int(gog_score_c.text) <= 99:
        gog_score_c.x = 26
        gog_score_c.y = 27
    elif int(gog_score_c.text) >= 100:
        gog_score_c.x = 23
        gog_score_c.y = 27

    display.show(gog)
    
    # play the game over audio
    if speaker.playing:
        speaker.stop()
    mp3stream.file = open(audio_file["game_over"], "rb")
    speaker.play(mp3stream)
    
    # allow gog labels to blink
    blink_labels["gog"]["blink"] = True
    blink_vrs["labels_are_visible"] = False # makes sure the labels are visible at the start of blinking
    
    # center the hoop
    tic.go_home_centre(bg_task=bg_tasks)

    while time() - start_time <= 10:
        # animate LEDs
        rainbow.animate()
        
        # blink labels
        handle_blink()

    # stop gog labels blink
    blink_labels["gog"]["blink"] = False

    scrn_state = scrn_states[1]

def new_hiscore_scrn():
    global scrn_state, highest_score

    # set properties
    nhg_hiscore_c.text = str(highest_score)

    # variables
    start_time = time()
    bg_tasks = [rainbow.animate, handle_blink] # functions to be called while the hoop centers

    # center the hiscore value label
    if highest_score <= 9:
        nhg_hiscore_c.x = 29
        nhg_hiscore_c.y = 27
    elif highest_score >= 10 and highest_score <= 99:
        nhg_hiscore_c.x = 26
        nhg_hiscore_c.y = 27
    elif highest_score >= 100:
        nhg_hiscore_c.x = 23
        nhg_hiscore_c.y = 27

    display.show(nhg)
    
    # play the hiscore audio
    if speaker.playing:
        speaker.stop()
    mp3stream.file = open(audio_file["hiscore"], "rb")
    speaker.play(mp3stream)
    
    # allow gog labels to blink
    blink_labels["nhg_new"]["blink"] = True
    blink_vrs["labels_are_visible"] = False # makes sure the labels are visible at the start of blinking
    
    # center the hoop
    tic.go_home_centre(bg_task=bg_tasks)

    while time() - start_time <= 10:
        # animate LEDs
        rainbow.animate()
        
        # blink labels
        handle_blink()
        
    # stop nhg_new labels blink
    blink_labels["nhg_new"]["blink"] = False

    scrn_state = scrn_states[1]

# variables
scrns = {
    "start_scrn": start_scrn,
    "countdown_scrn": countdown_scrn,
    "arcade_scrn": arcade_scrn,
    "game_over_scrn": game_over_scrn,
    "new_hiscore_scrn": new_hiscore_scrn
}

# main loop, run the approriate screen function given the screen state
while True:
    scrns[scrn_state]()

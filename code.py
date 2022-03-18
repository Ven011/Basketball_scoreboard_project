import displayio
import rgbmatrix
import board
import framebufferio
import audioio
import audiomp3
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label as label
from time import sleep, time, monotonic
import digitalio
import neopixel
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.solid import Solid

# RGBMatrix setup
displayio.release_displays()

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
hg = displayio.Group()

# save hiscore
def get_set_hiscore(value="_"):
    if value != "_":
        hiscore_file = open("/temp/hiscore.txt", "w")
        hiscore_file.write(value)
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
cdg_time = label.Label(virtual_pet_sans, text="TIME", color=0x0000FF, x=3, y=5)
cdg_time_c = label.Label(virtual_pet_sans, color=0xFF0000, x=12, y=15)
cdg_score = label.Label(virtual_pet_sans, text="SCORE", color=0x0000FF, x=32, y=5)
cdg_score_c = label.Label(virtual_pet_sans, color=0xFFFFFF, x=44, y=15)
cdg_hiscore = label.Label(virtual_pet_sans, text="HISCORE", color=0x00FFFF)
cdg_hiscore_c = label.Label(virtual_pet_sans, text=get_set_hiscore(), color=0x00FFFF)

# arcade graphics
ag_time = label.Label(virtual_pet_sans, text="TIME", color=0x0000FF, x=3, y=5)
ag_time_c = label.Label(virtual_pet_sans, color=0xFF0000)
ag_score = label.Label(virtual_pet_sans, text="SCORE", color=0x0000FF, x=32, y=5)
ag_score_c = label.Label(virtual_pet_sans, color=0xFFFFFF)
ag_hiscore = label.Label(virtual_pet_sans, text="HISCORE", color=0x00FFFF)
ag_hiscore_c = label.Label(virtual_pet_sans, text=get_set_hiscore(), color=0x00FFFF)

# bonus time graphics
bt_time = label.Label(virtual_pet_sans, text="TIME", color=0x0000FF, x=3, y=5)
bt_time_c = label.Label(virtual_pet_sans, color=0xFF0000)
bt_score = label.Label(virtual_pet_sans, text="SCORE", color=0x0000FF, x=32, y=5)
bt_score_c = label.Label(virtual_pet_sans, color=0xFFFFFF)
bt_bonus = label.Label(virtual_pet_sans, text="BONUS", color=0x00FF00, x=4, y=28)
bt_bonus_t = label.Label(virtual_pet_sans, text="TIME", color=0x00FF00, x=37, y=28)

# game over graphics
gog_game = label.Label(ozone, text="GAME", color=0xB30000, x=2, y=5)
gog_over = label.Label(ozone, text="OVER", color=0xB30000, x=35, y=5)
gog_score = label.Label(virtual_pet_sans, text="SCORE", color=0x00B3B3, x=17, y=17)
gog_score_c = label.Label(virtual_pet_sans, color=0xFFFFFF)

# new hiscore graphics
nhg_new = label.Label(ozone, text="NEW", color=0x00B300, x=21, y=5)
nhg_hiscore = label.Label(virtual_pet_sans, text="HISCORE", color=0x00B3B3, x=11, y=17)
nhg_hiscore_c = label.Label(virtual_pet_sans, color=0xFFFFFF)

# h.o.r.s.e graphics
hg_time = label.Label(virtual_pet_sans, text="TIME", color=0xB35A00)
hg_time_c = label.Label(virtual_pet_sans, color=0x00B300)
hg_p1 = label.Label(virtual_pet_sans, text="P1", color=0x00B3B3, x=6, y=17)
hg_p1_h = label.Label(virtual_pet_sans, text="H.", color=0xFFFFFF, x=21, y=17)
hg_p1_o = label.Label(virtual_pet_sans, text="O.", color=0xFFFFFF, x=29, y=17)
hg_p1_r = label.Label(virtual_pet_sans, text="R.", color=0xFFFFFF, x=37, y=17)
hg_p1_s = label.Label(virtual_pet_sans, text="S.", color=0xFFFFFF, x=45, y=17)
hg_p1_e = label.Label(virtual_pet_sans, text="E", color=0xFFFFFF, x=53, y=17)
hg_p2 = label.Label(virtual_pet_sans, text="P2", color=0xB300B3, x=6, y=28)
hg_p2_h = label.Label(virtual_pet_sans, text="H.", color=0xFFFFFF, x=21, y=28)
hg_p2_o = label.Label(virtual_pet_sans, text="O.", color=0xFFFFFF, x=29, y=28)
hg_p2_r = label.Label(virtual_pet_sans, text="R.", color=0xFFFFFF, x=37, y=28)
hg_p2_s = label.Label(virtual_pet_sans, text="S.", color=0xFFFFFF, x=45, y=28)
hg_p2_e = label.Label(virtual_pet_sans, text="E", color=0xFFFFFF, x=53, y=28)
hg_p1_won = label.Label(ozone, text="P1", color=0x00B3B3, x=13, y=4)
hg_p1_w = label.Label(ozone, text="WON", color=0x00B3B3, x=28, y=4)
hg_p2_won = label.Label(ozone, text="P2", color=0xB300B3, x=12, y=4)
hg_p2_w = label.Label(ozone, text="WON", color=0xB300B3, x=29, y=4)

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

cdg.append(cdg_time)
cdg.append(cdg_time_c)
cdg.append(cdg_score)
cdg.append(cdg_score_c)
cdg.append(cdg_hiscore)
cdg.append(cdg_hiscore_c)

ag.append(ag_time)
ag.append(ag_time_c)
ag.append(ag_score)
ag.append(ag_score_c)
ag.append(ag_hiscore)
ag.append(ag_hiscore_c)

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

hg.append(hg_time)
hg.append(hg_time_c)
hg.append(hg_p1)
hg.append(hg_p2)

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

# NeoPixel setup
pixels = neopixel.NeoPixel(board.D8, 54, brightness=0.2)
rainbow = Rainbow(pixels, speed=0.1, period=2, step=1)
colorcycle = ColorCycle(pixels, 0.5, colors=[0xFFFFFF, 0xB30000, 0x00B300, 0x0000B3])
solid_white = Solid(pixels, color=0xFFFFFF)
solid_green = Solid(pixels, color=0x00B300)
solid_yellow = Solid(pixels, color=0xB3B300)
solid_red = Solid(pixels, color=0xB30000)

# arcade button setup
btn_arcade = digitalio.DigitalInOut(board.SCK)
btn_arcade.direction = digitalio.Direction.INPUT
btn_arcade.pull = digitalio.Pull.UP

# h.o.r.s.e button setup
btn_horse = digitalio.DigitalInOut(board.MISO)
btn_horse.direction = digitalio.Direction.INPUT
btn_horse.pull = digitalio.Pull.UP

# top sensor setup
sen_top = digitalio.DigitalInOut(board.D0)
sen_top.direction = digitalio.Direction.INPUT
sen_top.pull = digitalio.Pull.UP

# bottom sensor setup
sen_btm = digitalio.DigitalInOut(board.D1)
sen_btm.direction = digitalio.Direction.INPUT
sen_btm.pull = digitalio.Pull.UP

# variables
scrn_states = {
    1: "start_scrn",
    2: "countdown_scrn",
    3: "arcade_scrn",
    4: "game_over_scrn",
    5: "new_hiscore_scrn",
    6: "horse_scrn"
}

button_states = {
    1: False,
    2: False
}

scrn_state = "start_scrn"
highest_score = "0"

# center labels
def center_labels(time_c_label, score_c_label):
    # center the time value label
    if int(time_c_label.text) >= 10 and int(time_c_label.text) <= 60:
        time_c_label.x = 9
        time_c_label.y = 15
        display.refresh()
    elif int(time_c_label.text) >= 0:
        time_c_label.x = 12
        time_c_label.y = 15
        display.refresh()

    # center the score value label
    if int(score_c_label.text) >= 100:
        score_c_label.x = 38
        score_c_label.y = 15
        display.refresh()
    elif int(score_c_label.text) >= 10 and int(score_c_label.text) <= 99:
        score_c_label.x = 41
        score_c_label.y = 15
        display.refresh()
    elif int(score_c_label.text) >= 0:
        score_c_label.x = 44
        score_c_label.y = 15
        display.refresh()

# control pixels in the arcade and bonus time modes
def control_pixels(time_c_label, mode):
    if int(time_c_label.text) <= 60 and int(time_c_label.text) >= 21:
        solid_green.animate()
    elif int(time_c_label.text) <= 20 and int(time_c_label.text) >= 11:
        solid_yellow.animate()
        if int(time_c_label.text) == 11:
            mp3stream.file = open(audio_file["countdown"], "rb")
            speaker.play(mp3stream)
    if mode == "arcade_scrn":
        if int(time_c_label.text) <= 10 and int(time_c_label.text) >= 0:
            solid_red.animate()

def start_scrn():
    global scrn_state, highest_score

    # variables
    labels_are_visible = False
    blink_timer = 0
    blink_period = 0
    reset_score_v = 0
    reset_score_t = 0

    display.show(sg)

    def checks():
        nonlocal labels_are_visible, blink_timer, blink_period

        if not speaker.playing:
            mp3stream.file = open(audio_file["space_jam"], "rb")
            speaker.play(mp3stream)

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

    while scrn_state == scrn_states[1]:
        colorcycle.animate()

        checks()

        # reset the hiscore if the arcade button is held for 5 seconds
        if not btn_arcade.value and not button_states[1]:
            reset_score_v = time()
            button_states[1] = True
            while not btn_arcade.value:
                checks()
                colorcycle.animate()
                reset_score_t = time() - reset_score_v
                if reset_score_t == 5:
                    ag_hiscore_c.text = "0"
                    highest_score = "0"
                    get_set_hiscore(value="0")
                    solid_white.animate()
                    # allow the button state to be changed to True after reset
                    button_states[1] = False
                    # used to prevent entry to game after the 5 seconds
                    reset_score_v = -1
                    sleep(1)
                    break

        # switch to the arcade scrn
        if button_states[1] and reset_score_v != -1:
            button_states[1] = False
            if speaker.playing:
                speaker.stop()
            scrn_state = scrn_states[2]

        # switch to the h.o.r.s.e scrn
        if not btn_horse.value and not button_states[2]:
            button_states[2] = True
            if speaker.playing:
                speaker.stop()
            scrn_state = scrn_states[6]

def countdown_scrn():
    global scrn_state

    # set properties
    cdg_time_c.text = "3"
    cdg_score_c.text = "0"

    # variables
    countdown_time = 3
    saved_hiscore = get_set_hiscore()
    cdg_hiscore_c.text = saved_hiscore
    prev_time = countdown_time

    # center the hiscore labels
    if int(saved_hiscore) >= 100:
        cdg_hiscore.x = 1
        cdg_hiscore.y = 28
        cdg_hiscore_c.x = 46
        cdg_hiscore_c.y = 28
    elif int(saved_hiscore) >= 10 and int(saved_hiscore) <= 99:
        cdg_hiscore.x = 4
        cdg_hiscore.y = 28
        cdg_hiscore_c.x = 49
        cdg_hiscore_c.y = 28
    elif int(saved_hiscore) >= 0:
        cdg_hiscore.x = 7
        cdg_hiscore.y = 28
        cdg_hiscore_c.x = 52
        cdg_hiscore_c.y = 28

    solid_green.animate()

    display.show(cdg)
    sleep(1)
    countdown_timer = time()
    
    # set the initial text of the countdown time counter
    cdg_time_c.text = str(3)

    while scrn_state == scrn_states[2]:
        # update the time left in the countdown
        if (countdown_time - int(time() - countdown_timer)) == prev_time - 1:
            cdg_time_c.text = str(prev_time - 1)
            prev_time = prev_time - 1

        # switch to the arcade scrn
        if int(cdg_time_c.text) == 1:
            sleep(1)
            scrn_state = scrn_states[3]
            mp3stream.file = open(audio_file["whistle"], "rb")
            speaker.play(mp3stream)

def arcade_scrn():
    global scrn_state, highest_score

    # set properties
    ag_time_c.text = "60"
    ag_score_c.text = "0"
    ag_hiscore.color = 0x00FFFF
    ag_hiscore_c.color = 0x00FFFF

    # variables
    labels_are_visible = False
    blink_timer = time()
    hiscoretext_delay = 0
    blink_period = 0
    game_time = 60
    saved_hiscore = get_set_hiscore()
    ag_hiscore_c.text = saved_hiscore
    can_do_bonus = True if int(saved_hiscore) >= 20 else False # prevent the bonus time when the hiscore is 0 for the first game
    hiscore_beaten = False
    sen_triggered = 0
    sen_top_state = False
    sen_btm_state = False
    combined_sen_state = True
    prev_time = game_time

    # center the time and score value
    center_labels(ag_time_c, ag_score_c)

    # center the hiscore labels
    if int(saved_hiscore) >= 100:
        ag_hiscore.x = 1
        ag_hiscore.y = 28
        ag_hiscore_c.x = 46
        ag_hiscore_c.y = 28
    elif int(saved_hiscore) >= 10 and int(saved_hiscore) <= 99:
        ag_hiscore.x = 4
        ag_hiscore.y = 28
        ag_hiscore_c.x = 49
        ag_hiscore_c.y = 28
    elif int(saved_hiscore) >= 0:
        ag_hiscore.x = 7
        ag_hiscore.y = 28
        ag_hiscore_c.x = 52
        ag_hiscore_c.y = 28

    display.show(ag)
    game_timer = time()

    while scrn_state == scrn_states[3]:
        # delay showing hiscore text after bonus time
        if time() - hiscoretext_delay is not time() and time() - hiscoretext_delay > 1:
            ag_hiscore.color = 0x00FFFF
            ag_hiscore_c.color = 0x00FFFF
        
        # update the time left in the game
        if (game_time - int(time() - game_timer)) == prev_time - 1:
            ag_time_c.text = str(prev_time - 1)
            prev_time = prev_time - 1

        # prevent point if both sensors detect an object simultaneously
        combined_sen_state = False if not sen_top.value and not sen_btm.value else True

        # check if the top sensor is triggered
        if not sen_top.value and not sen_top_state:
            sen_top_state = True
            sen_triggered += 1
        # if sen_top.value and sen_top_state:
        #     sen_triggered += 1

        # check if the bottom sensor is triggered
        if not sen_btm.value and not sen_btm_state:
            sen_btm_state = True
            sen_triggered += 1
        if sen_btm.value and sen_btm_state and sen_triggered == 2:
            sen_triggered += 1

        # add point if both sensors have been triggered consecutively
        if sen_triggered == 3:
            sen_top_state = False
            sen_btm_state = False
            sen_triggered = 0
            # check whether the top sensor detects the ball
            if not sen_top.value:  # it does
                pass
            else:  # it does not
                ag_score_c.text = str(int(ag_score_c.text) + 4)

        # center the time and score value
        center_labels(ag_time_c, ag_score_c)

        # difference between the saved high score and the game score
        score_diff = int(saved_hiscore) - int(ag_score_c.text)

        # bonus time
        if can_do_bonus:
            if score_diff <= 5 and score_diff >= 0:
                if time() >= blink_timer + blink_period:
                    blink_timer = time()
                    if labels_are_visible:
                        labels_are_visible = False
                        blink_period = 1
                        ag_hiscore.color = 0x000000
                        ag_hiscore_c.color = 0x000000
                    else:
                        labels_are_visible = True
                        blink_period = 1
                        ag_hiscore.color = 0x00FFFF
                        ag_hiscore_c.color = 0x00FFFF

            # hiscore has been beaten and was not beaten before in this game
            if score_diff < 0 and not hiscore_beaten and int(ag_time_c.text) <= 30:
                hiscore_beaten = True

                ag_hiscore.color = 0x000000
                ag_hiscore_c.color = 0x000000

                mp3stream.file = open(audio_file["hiscore"], "rb")
                speaker.play(mp3stream)

                # add time when the score is beaten
                if int(ag_time_c.text) >= 1 and int(ag_time_c.text) <= 10:
                    game_time += 30
                elif int(ag_time_c.text) >= 11 and int(ag_time_c.text) <= 20:
                    game_time += 20
                elif int(ag_time_c.text) >= 21 and int(ag_time_c.text) <= 30:
                    game_time += 10

                # go to the bonus time scrn for 10 seconds
                ag_score_c.text, ag_time_c.text, ag_time_c.x, ag_time_c.y = arcade_bonus_scrn(game_time, game_timer, ag_score_c.text)
                
                prev_time = int(ag_score_c.text) # update the previous time to make sure that the time keeps updating in game
                
                hiscoretext_delay = time() 

                display.show(ag)

        control_pixels(ag_time_c, "arcade_scrn")

        # check if the previously set hiscore has been beaten
        if int(ag_score_c.text) > int(saved_hiscore):
            highest_score = ag_score_c.text
            if not hiscore_beaten and int(ag_time_c.text) >= 31:
                hiscore_beaten = True
                ag_hiscore.color = 0x00FFFF
                ag_hiscore_c.color = 0x00FFFF
                mp3stream.file = open(audio_file["hiscore"], "rb")
                speaker.play(mp3stream)

        # exit the game when the time is up
        if int(ag_time_c.text) <= 0:
            sleep(1)
            if int(highest_score) > int(saved_hiscore): # hiscore was beaten
                scrn_state = scrn_states[5]
                get_set_hiscore(value=ag_score_c.text) # save the hiscore
                mp3stream.file = open(audio_file["hiscore"], "rb")
                speaker.play(mp3stream)
            else: # hiscore was not beaten
                scrn_state = scrn_states[4]
                mp3stream.file = open(audio_file["game_over"], "rb")
                speaker.play(mp3stream)

def arcade_bonus_scrn(game_time, game_timer, score):
    # set properties
    bt_bonus.color = 0x000000
    bt_bonus_t.color = 0x000000
    bt_score_c.text = score
    
    start_time = (game_time - int(time() - game_timer)) + 1
    exception = 0.5
    # don't start bonus time until the remainder of the past second has fully passed
    while (game_time - int(time() - game_timer)) == start_time - 1:
        # make an exception if the remainder of the past seconds is greater than the exception time
        if start_time - (game_time - (time() - game_timer)) > exception:
            break
        pass
    
    bt_time_c.text = str(game_time - int(time() - game_timer)) # needs to come after the loop above

    # variables
    labels_are_visible = False
    blink_timer = time()
    blink_period = 1
    bt_start_time = time()
    bt_stay_time = 10
    sen_triggered = 0
    sen_top_state = False
    sen_btm_state = False
    combined_sen_state = True
    prev_time = int(bt_time_c.text)

    # center the time and score value
    center_labels(ag_time_c, ag_score_c)

    display.show(btg)

    # stay in the bonus time scrn for the time specified in stay_time
    while time() < bt_start_time + bt_stay_time:
        rainbow.animate()

        # update the time
        if (game_time - int(time() - game_timer)) == prev_time - 1:
            bt_time_c.text = str(prev_time - 1)
            prev_time = prev_time - 1

        # prevent point if both sensors detect an object simultaneously
        combined_sen_state = False if not sen_top.value and not sen_btm.value else True

        # check if the top sensor is triggered
        if not sen_top.value and not sen_top_state and combined_sen_state:
            sen_top_state = True
            sen_triggered += 1
        if sen_top.value and sen_top_state and sen_triggered == 1:
            sen_triggered += 1

        # check if the bottom sensor is triggered
        if not sen_btm.value and not sen_btm_state and sen_triggered == 2:
            sen_btm_state = True
            sen_triggered += 1
        if sen_btm.value and sen_btm_state and sen_triggered == 3:
            sen_triggered += 1

        # add point if both sensors have been triggered consecutively
        if sen_triggered == 4:
            sen_top_state = False
            sen_btm_state = False
            sen_triggered = 0
            # # check whether the top sensor detects the ball
            if not sen_top.value:  # it does
                pass
            else:  # it does not
                bt_score_c.text = str(int(bt_score_c.text) + 4)

        # center the time and score value
        center_labels(bt_time_c, bt_score_c)

        if time() >= blink_timer + blink_period:
            blink_timer = time()
            if labels_are_visible:
                labels_are_visible = False
                blink_period = 1
                bt_bonus.color = 0x000000
                bt_bonus_t.color = 0x000000
            else:
                labels_are_visible = True
                blink_period = 1
                bt_bonus.color = 0x00FF00
                bt_bonus_t.color = 0x00FF00

        control_pixels(bt_time_c, "arcade_bonus_scrn")

    return bt_score_c.text, bt_time_c.text, bt_time_c.x, bt_time_c.y

def game_over_scrn():
    global scrn_state

    # set properties
    gog_score_c.text = ag_score_c.text

    # variables
    labels_are_visible = False
    blink_timer = time()
    blink_period = 0
    start_time = time()

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

    while time() - start_time <= 10:
        rainbow.animate()

        if time() >= blink_timer + blink_period:
            blink_timer = time()
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

    scrn_state = scrn_states[1]

def new_hiscore_scrn():
    global scrn_state, highest_score

    # set properties
    nhg_hiscore_c.text = highest_score

    # variables
    labels_are_visible = False
    blink_timer = time()
    blink_period = 0
    start_time = time()

    # center the hiscore value label
    if int(highest_score) <= 9:
        nhg_hiscore_c.x = 29
        nhg_hiscore_c.y = 27
    elif int(highest_score) >= 10 and int(highest_score) <= 99:
        nhg_hiscore_c.x = 26
        nhg_hiscore_c.y = 27
    elif int(highest_score) >= 100:
        nhg_hiscore_c.x = 23
        nhg_hiscore_c.y = 27

    display.show(nhg)

    while time() - start_time <= 10:
        rainbow.animate()

        if time() >= blink_timer + blink_period:
            blink_timer = time()
            if labels_are_visible:
                labels_are_visible = False
                blink_period = 1
                nhg_new.color = 0x000000
            else:
                labels_are_visible = True
                blink_period = 2
                nhg_new.color = 0x00B300

    scrn_state = scrn_states[1]

def horse_scrn():
    global scrn_state

    button_states[2] = False

    # set properties
    hg_time_c.text = "10"

    # center the time and time value text
    if int(hg_time_c.text) <= 9:
        hg_time.x = 16
        hg_time.y = 5
        hg_time_c.x = 43
        hg_time_c.y = 5
    elif int(hg_time_c.text) == 10:
        hg_time.x = 13
        hg_time.y = 5
        hg_time_c.x = 40
        hg_time_c.y = 5

    display.show(hg)
    sleep(1)

# variables
scrns = {
    "start_scrn": start_scrn,
    "countdown_scrn": countdown_scrn,
    "arcade_scrn": arcade_scrn,
    "game_over_scrn": game_over_scrn,
    "new_hiscore_scrn": new_hiscore_scrn,
    "horse_scrn": horse_scrn
}

# main loop, run the approriate screen function given the screen state
while True:
    scrns[scrn_state]()

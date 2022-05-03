'''
Copyright © Tomislav Vuksic 2022, All Rights Reserved.
This system, including hardware and software, is Copyrighted© and trademarked® by Tomislav Vuksic.
Any unauthorised / commercial use of the system or any part of it is strictly prohibited.
'''
import bitbangio
import board
from adafruit_bus_device.i2c_device import I2CDevice
from time import time

class TicI2C(object):
    def __init__(self, address=14, centre=110000):
        """
        - tic.address() is optional and defaults to 14
        - tic.centre() is optional and defaults to 110000, centre is also used to calculate all relative movements
        - tic.current_position() is an absolute value and defaults to 0. To update the current position call the tic.get_current_position() function or the homing function tic_go_home()
        - tic.time_sleep() is used for setting a pause in the tic.control_hoop() function
        """

        self.address = address
        self.centre = centre
        self.current_position = 0
        self.time_sleep = 0.0
        
    def active_sleep(self, duration, bg_task=None):
        """
        - This function is meant to mimic the sleep function, but will not stop other tasks from running like sleep does.
        """
        s_time = time()
        while time() - s_time < duration:
            if bg_task == None:
                pass
            else:
                bg_task()

    def write_command(self, command):
        """
        write command via I2C to the Tic while locking the bus, the array includes a specific command with its data variables
        """

        bytes_to_write = bytearray(command)

        with bitbangio.I2C(board.SCL, board.SDA, timeout=1500) as i2c:
            device = I2CDevice(i2c, self.address)
            with device:
                device.write(bytes_to_write)

    def get_variables(self, offset, length):
        """
        - reads a variable from a specific offset from the Tic for defined length
        - returns a list of data
        """

        with bitbangio.I2C(board.SCL, board.SDA, timeout=1500) as i2c:
            device = I2CDevice(i2c, self.address)
            read = bytearray(length)
            with device:
                device.write_then_readinto(bytearray([0xA1, offset]), read)

        return list(read)

    def control_hoop(self, max_speed=500000000, starting_speed=0, max_acceleration=500000000, max_deceleration=500000000):
        """
        this function declares the velocity parameters and if the parameters are not declared the values used are the default Tic settings:
        - max_speed
        - starting_speed
        - max_acceleration
        - max_deceleration
        """

        # set the max speed
        if max_speed <= 500000000:
            command = [0xE6,
                max_speed >> 0 & 0xFF,
                max_speed >> 8 & 0xFF,
                max_speed >> 16 & 0xFF,
                max_speed >> 24 & 0xFF,
            ]
            self.write_command(command)
            if self.time_sleep > 0.0:
                self.active_sleep(self.time_sleep)

        # set the starting speed
        if starting_speed <= 500000000:
            command = [0xE5,
                starting_speed >> 0 & 0xFF,
                starting_speed >> 8 & 0xFF,
                starting_speed >> 16 & 0xFF,
                starting_speed >> 24 & 0xFF,
            ]
            self.write_command(command)
            if self.time_sleep > 0.0:
                self.active_sleep(self.time_sleep)

        # set the max acceleration
        if max_acceleration <= 2147483647:
            command = [0xEA,
                max_acceleration >> 0 & 0xFF,
                max_acceleration >> 8 & 0xFF,
                max_acceleration >> 16 & 0xFF,
                max_acceleration >> 24 & 0xFF,
            ]
            self.write_command(command)
            if self.time_sleep > 0.0:
                self.active_sleep(self.time_sleep)

        # set the max deceleration
        if max_deceleration <= 2147483647:
            command = [0xE9,
                max_deceleration >> 0 & 0xFF,
                max_deceleration >> 8 & 0xFF,
                max_deceleration >> 16 & 0xFF,
                max_deceleration >> 24 & 0xFF,
            ]
            self.write_command(command)
            if self.time_sleep > 0.0:
                self.active_sleep(self.time_sleep)

    def get_current_position(self):
        """
        tic.get_current_position() reads and returns the current position from the Tic
        """

        b = self.get_variables(0x22, 4)
        position = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)

        if position >= (1 << 31):
            position -= (1 << 32)

        # save the current position
        self.current_position = position

        return position

    def set_target_position(self, target):
        """
        - tell the Tic to move to a specific target
        - tic.set_target_position(0) is the real 0 position
        """

        command = [0xE0,
        target >> 0 & 0xFF,
        target >> 8 & 0xFF,
        target >> 16 & 0xFF,
        target >> 24 & 0xFF]

        self.write_command(command)
        self.current_position = target

    def go_target(self, position, target_sleep=0.0, bg_task=None):
        """
        this function moves to a specified position relative to the centre:
        - tic.go_target(0) is always the centre position
        - target_sleep is an optional parameter and was defaulted to 0.002 (code won't continue until sleep is complete)
        - positive values will move away from the stepper
        - negative values will move toward the stepper
        """

        # set the new position if it does not exceed the max extents
        if abs(position) <= self.centre:
            self.set_target_position(self.centre + position)

            # wait until the position is reached
            if target_sleep > 0.0:
                while self.get_current_position() != self.centre + position:
                    if target_sleep > 0.0:
                        self.active_sleep(self.time_sleep, bg_task=bg_task)

    def go_home(self, reverse=True):
        """
        - tic.go_home() will reverse to the limit switch
        - if the parameter reverse is set to False it will move forward to the limit switch
        """

        direction = 0
        if not reverse:
            direction = 1

        command = [0x97,
            direction >> 0 & 0x7F,
        ]
        self.write_command(command)
        if self.time_sleep > 0.0:
            self.active_sleep(self.time_sleep)
        self.current_position = 0

    def go_home_centre(self, reverse=True, wait_time=5, max_speed=500000000, starting_speed=0, max_acceleration=500000000, max_deceleration=500000000, bg_task = None):
        """
        this function executes the tic.go_home() function, then waits for the wait_time, and moves to centre using the velocity parameters
        - the parameter wait_time is by default 5 seconds
        - the reverse parameter gets passed to the tic.go_home() function and is by default True
        - the velocity parameters are the same as the tic.control_hoop() function and are passed to it

        if using the function tic.go_home_centre() it will go home in reverse, wait for 5 seconds and go to the centre with a max_speed of 500M,
        starting_speed of 0, max_acceleration of 500M and max_deceleration of 500M, as it will use all the default values

        if using the function tic.go_home_centre(wait_time=2, max_speed=100000000) it will go home in reverse, wait for 2 seconds
        and go to the centre with a max_speed of 100M, starting_speed of 0, max_acceleration of 500M and max_deceleration of 500M
        """

        self.go_home(reverse=reverse)
        if wait_time > 0.0:
            self.active_sleep(wait_time, bg_task)

        self.control_hoop(max_speed=max_speed, starting_speed=starting_speed, max_acceleration=max_acceleration, max_deceleration=max_deceleration)
        self.go_target(0)

    def halt_set_position(self):
        """
        tic.halt_set_position() halts the motor and sets the current position roughly
        """

        position = self.get_current_position()

        command = [0xEC,
            position >> 0 & 0xFF,
            position >> 8 & 0xFF,
            position >> 16 & 0xFF,
            position >> 24 & 0xFF,
        ]
        self.write_command(command)
        if self.time_sleep > 0.0:
            self.active_sleep(self.time_sleep)

    def exit_safe_start(self):
        """
        tell the Tic to execute the tic.exit_safe_start() function
        """

        command = [0x83]

        self.write_command(command)

    def macro_velocity(self, pos_dict):
        """
        this function accepts a dictionary as a macro for predefined values to be passed to the tic.control_hoop() function, once a parameter is changed the new value will become permanent until changed again

        this example will expect all parameters to be present in the dictionary including the position:
        m_CONTROLHOOP = {"max_speed":300000000, "starting_speed":0, "max_acceleration":300000000, "max_deceleration":300000000}
        tic.macro_velocity(m_CONTROLHOOP)

        this example will only change one parameter while keeping the others unchanged:
        m_CONTROLHOOP["max_speed"] = 400000000
        tic.macro_velocity(m_CONTROLHOOP)

        this example will change two parameters while keeping the others unchanged:
        m_CONTROLHOOP["max_speed"] = 400000000
        m_CONTROLHOOP["max_acceleration"] = 300000000
        tic.macro_velocity(m_CONTROLHOOP)
        """

        self.control_hoop(pos_dict["max_speed"], pos_dict["starting_speed"], pos_dict["max_acceleration"], pos_dict["max_deceleration"])

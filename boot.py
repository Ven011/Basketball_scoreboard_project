import board
import digitalio
import storage

# Feather M4 Express
# switch = digitalio.DigitalInOut(board.D4)
# switch.direction = digitalio.Direction.INPUT
# switch.pull = digitalio.Pull.UP

# Metro M4 Express
switch = digitalio.DigitalInOut(board.D2)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the switch pin is connected to ground CircuitPython can write to the drive
storage.remount("/", switch.value)

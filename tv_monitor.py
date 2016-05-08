import cec_power
import remote_command
from time import sleep

old_state = cec_power.power_status(0)

while True:
    new_state = cec_power.power_status(0)
    if new_state - old_state == 1:
        remote_command.remote_com("TV_AUDIO")
    old_state = cec_power.power_status(0)
    sleep(1)

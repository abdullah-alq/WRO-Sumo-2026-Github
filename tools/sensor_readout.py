# sensor_readout.py - live sensor values on the brain screen and console.
# Same ports and LED settings as sumo.py, so the numbers match the match code.
from vex import *

brain = Brain()

line_front_left = Optical(Ports.PORT9)
line_front_right = Optical(Ports.PORT4)
line_back = Optical(Ports.PORT5)
distance_left = Distance(Ports.PORT8)
distance_right = Distance(Ports.PORT3)

for s in (line_front_left, line_front_right, line_back):
    s.set_light_power(100, PERCENT)
    s.set_light(LedStateType.ON)
wait(300, MSEC)


def dist(sensor):
    # -1 means nothing detected
    return sensor.object_distance(MM) if sensor.is_object_detected() else -1


while True:
    optical = (("FL", line_front_left), ("FR", line_front_right), ("BK", line_back))

    brain.screen.clear_screen()
    row = 1
    for name, s in optical:
        brain.screen.set_cursor(row, 1)
        brain.screen.print("%s b%3d h%3d" % (name, s.brightness(), s.hue()))
        row += 1
    brain.screen.set_cursor(4, 1)
    brain.screen.print("DL%5d DR%5d" % (dist(distance_left), dist(distance_right)))

    print("FL b%d h%d | FR b%d h%d | BK b%d h%d | DL %d DR %d" % (
        line_front_left.brightness(), line_front_left.hue(),
        line_front_right.brightness(), line_front_right.hue(),
        line_back.brightness(), line_back.hue(),
        dist(distance_left), dist(distance_right)))

    wait(200, MSEC)

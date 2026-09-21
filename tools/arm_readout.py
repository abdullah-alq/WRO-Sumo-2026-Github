# arm_readout.py - read arm positions by moving the arm by hand.
# Start with the arm FULLY UP (that is zero, same as sumo.py), press Run,
# then move the arm by hand and read the numbers.
from vex import *

brain = Brain()
arm_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
ARM_RATIO = 36 / 12

arm_motor.set_position(0, DEGREES)
arm_motor.stop(COAST)       # free to move by hand

while True:
    motor_deg = arm_motor.position(DEGREES)
    arm_deg = motor_deg / ARM_RATIO

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("motor %d" % motor_deg)
    brain.screen.set_cursor(2, 1)
    brain.screen.print("arm   %d" % arm_deg)

    print("motor %d deg | arm %d deg" % (motor_deg, arm_deg))
    wait(200, MSEC)

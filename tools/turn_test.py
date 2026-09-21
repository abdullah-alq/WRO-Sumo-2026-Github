# turn_test.py - measure the real escape turn and break pivot angles.
# Uses the Brain's built-in inertial sensor, so no protractor needed.
# Put the robot on the mat, press Run, keep it still while it calibrates.
# Each turn is run right then left, with the same power ramp as sumo.py.
from vex import *

brain = Brain()
imu = Inertial()

right_drive = MotorGroup(Motor(Ports.PORT1, GearSetting.RATIO_18_1, False),
                         Motor(Ports.PORT2, GearSetting.RATIO_18_1, False))
left_drive = MotorGroup(Motor(Ports.PORT6, GearSetting.RATIO_18_1, True),
                        Motor(Ports.PORT7, GearSetting.RATIO_18_1, True))

# (name, power, ms) - same values as sumo.py
TESTS = [("escape", 80, 190), ("break", 90, 200)]
REPEATS = 2
LOOP_MS = 5
RAMP = 6                    # percent per tick, same as sumo.py


def spin(left, right):
    left_drive.spin(FORWARD, left, PERCENT)
    right_drive.spin(FORWARD, right, PERCENT)


def pivot(power, ms, turn_right):
    current = 0.0
    for _ in range(ms // LOOP_MS):
        current = min(current + RAMP, power)
        if turn_right:
            spin(current, -current)
        else:
            spin(-current, current)
        wait(LOOP_MS, MSEC)
    left_drive.stop(BRAKE)
    right_drive.stop(BRAKE)


imu.calibrate()
while imu.is_calibrating():
    wait(50, MSEC)

print("=== turn test ===")
for name, power, ms in TESTS:
    for run in range(REPEATS):
        for turn_right in (True, False):
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("%s %s" % (name, "R" if turn_right else "L"))
            wait(2000, MSEC)            # time to settle between runs

            imu.reset_rotation()
            pivot(power, ms, turn_right)
            wait(500, MSEC)             # let it stop fully
            angle = abs(imu.rotation(DEGREES))

            brain.screen.set_cursor(2, 1)
            brain.screen.print("%d deg" % angle)
            print("%s | %s | power %d | %d ms | %d deg"
                  % (name, "right" if turn_right else "left", power, ms, angle))

brain.screen.clear_screen()
brain.screen.print("done")

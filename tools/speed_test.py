# speed_test.py - measure real top speed and distance.
# Put the robot at one edge of the ring facing across, press Run.
# It waits 3 s, drives straight for 1.5 s (same ramp as sumo.py), stops.
# Measure the real distance with a tape and compare it to the printout.
# If the tape says less than the encoders, the wheels slipped.
from vex import *

brain = Brain()

right_drive = MotorGroup(Motor(Ports.PORT1, GearSetting.RATIO_18_1, False),
                         Motor(Ports.PORT2, GearSetting.RATIO_18_1, False))
left_drive = MotorGroup(Motor(Ports.PORT6, GearSetting.RATIO_18_1, True),
                        Motor(Ports.PORT7, GearSetting.RATIO_18_1, True))

DRIVE_RATIO = 36 / 12
WHEEL_CM = 6.5 * 3.1416     # circumference
RUN_MS = 1500
LOOP_MS = 5
RAMP = 6


def wheel_cm_per_s(motor_rpm):
    return motor_rpm / DRIVE_RATIO * WHEEL_CM / 60


wait(3000, MSEC)
left_drive.set_position(0, DEGREES)
right_drive.set_position(0, DEGREES)

current = 0.0
speeds = []
for tick in range(RUN_MS // LOOP_MS):
    current = min(current + RAMP, 100)
    left_drive.spin(FORWARD, current, PERCENT)
    right_drive.spin(FORWARD, current, PERCENT)
    if current >= 100:
        rpm = (left_drive.velocity(RPM) + right_drive.velocity(RPM)) / 2
        speeds.append(wheel_cm_per_s(rpm))
    wait(LOOP_MS, MSEC)

left_drive.stop(BRAKE)
right_drive.stop(BRAKE)
wait(300, MSEC)

motor_deg = (left_drive.position(DEGREES) + right_drive.position(DEGREES)) / 2
distance = motor_deg / DRIVE_RATIO / 360 * WHEEL_CM
top = sum(speeds) / len(speeds) if speeds else 0

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)
brain.screen.print("dist %.1f cm" % distance)
brain.screen.set_cursor(2, 1)
brain.screen.print("speed %.1f cm/s" % top)
print("encoder distance %.1f cm | average full power speed %.1f cm/s" % (distance, top))
print("tape measured distance: ______ cm")

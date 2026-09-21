#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration
# ============================================================
# WRO SUMO - TRI WHEEL RWD
# VEXcode V5 Python
# ============================================================

from vex import *

brain = Brain()


# ============================================================
# MODE TOGGLES
#
# Change these two lines and nothing else to switch the robot's
# whole behaviour. Useful on competition day if the judges rule
# against the mechanism at inspection.
#
#   ARM_ENABLED  = False  ->  the arm never moves during a match.
#                             It stays fully up at 0. Pure pusher,
#                             and the robot stays inside 20 x 20 cm
#                             for the whole match (rule 9.1).
#
#   LIFT_ENABLED = False  ->  the arm drops to the floor and stays
#                             there as a passive wedge. No lifting
#                             motion at all.
#
#   both True             ->  full behaviour: wedge in, then lift.
# ============================================================

ARM_ENABLED = True
LIFT_ENABLED = True

# Prints one line per state change to the VEXcode console: what the
# robot saw and why it did or did not lift. Costs nothing to leave on
# while testing, turn it off for the competition.
DEBUG = True


# ============================================================
# PORT MAP
# ============================================================

PORT_RIGHT_MOTOR_1 = Ports.PORT1
PORT_RIGHT_MOTOR_2 = Ports.PORT2
PORT_LEFT_MOTOR_1  = Ports.PORT6
PORT_LEFT_MOTOR_2  = Ports.PORT7

PORT_DISTANCE_RIGHT = Ports.PORT3
PORT_DISTANCE_LEFT  = Ports.PORT8

PORT_LINE_FRONT_RIGHT = Ports.PORT4
PORT_LINE_FRONT_LEFT  = Ports.PORT9
PORT_LINE_BACK        = Ports.PORT5

PORT_ARM = Ports.PORT10


# ============================================================
# EXTERNAL GEARING
#
# Drive: 12 tooth driving 36 tooth  -> 3:1 torque, 1/3 wheel speed
# Arm:   12 tooth driving 36 tooth  -> 3:1 torque, 1/3 arm speed
#
# The cartridge inside the motor is separate from this.
# These ratios are the metal gears on the robot.
# ============================================================

# Drive is two 12T sprockets (one per motor) on a chain to a 36T on the
# wheel axle. Nothing in the code needs this number, everything drives
# in percent power, but it belongs in the engineering notebook.
DRIVE_GEAR_IN = 12
DRIVE_GEAR_OUT = 36
DRIVE_RATIO = DRIVE_GEAR_OUT / DRIVE_GEAR_IN     # 3.0, recorded not used

# 200 rpm motor / 3 = 66.7 rpm at the wheel. 6.5 cm wheel = 20.4 cm
# per turn, so theoretical top speed is about 22.7 cm/s. Real speed
# under load is lower and still needs measuring.

ARM_GEAR_IN = 12
ARM_GEAR_OUT = 36
ARM_RATIO = ARM_GEAR_OUT / ARM_GEAR_IN           # 3.0


# ============================================================
# MOTOR DIRECTION
#
# Flip these if a side spins the wrong way.
# Test with a simple forward command before running the match code.
# ============================================================

RIGHT_REVERSED = False
LEFT_REVERSED  = True
ARM_REVERSED   = False


# ============================================================
# HARDWARE
# ============================================================

right_motor_1 = Motor(PORT_RIGHT_MOTOR_1, GearSetting.RATIO_18_1, RIGHT_REVERSED)
right_motor_2 = Motor(PORT_RIGHT_MOTOR_2, GearSetting.RATIO_18_1, RIGHT_REVERSED)

left_motor_1 = Motor(PORT_LEFT_MOTOR_1, GearSetting.RATIO_18_1, LEFT_REVERSED)
left_motor_2 = Motor(PORT_LEFT_MOTOR_2, GearSetting.RATIO_18_1, LEFT_REVERSED)

right_drive = MotorGroup(right_motor_1, right_motor_2)
left_drive  = MotorGroup(left_motor_1, left_motor_2)

# EXP 5.5W motors have no changeable cartridge. They run at a nominal
# 200 rpm and vexos reports them as an 18:1 green cartridge, so every
# motor here uses RATIO_18_1, including the arm.
arm_motor = Motor(PORT_ARM, GearSetting.RATIO_18_1, ARM_REVERSED)

distance_right = Distance(PORT_DISTANCE_RIGHT)
distance_left  = Distance(PORT_DISTANCE_LEFT)

line_front_right = Optical(PORT_LINE_FRONT_RIGHT)
line_front_left  = Optical(PORT_LINE_FRONT_LEFT)
line_back        = Optical(PORT_LINE_BACK)


# ============================================================
# DRIVE SETTINGS
# ============================================================

ATTACK_SPEED = 100          # full attack, never backs off

# Steering is proportional now instead of three fixed buckets.
# correction = (distance difference in mm) * STEER_GAIN
# It gets subtracted from the inner wheel, and the inner wheel is
# allowed to go negative so the robot pivots instead of arcing wide.

STEER_GAIN = 0.55
MAX_CORRECTION = 170        # inner wheel can reach -70, a real pivot
CENTER_TOLERANCE_MM = 35    # closer than this, just charge straight

# Only one sensor sees the opponent. With two forward facing sensors
# that just means they are offset by roughly half the sensor spacing,
# NOT that they are far off to the side. The old fixed -40 pivot made
# a small robot sitting slightly off centre look like a hard turn, and
# as it flickered between sensors the robot jerked left and right.
#
# Now the inner wheel is a fraction of forward power: a gentle arc when
# they are close, a firmer one when they are far.
SINGLE_NEAR_MM = 300
SINGLE_NEAR_FACTOR = 0.75   # close in, barely steer
SINGLE_FAR_FACTOR = 0.35    # far away, steer harder

SEARCH_SPEED = 70           # search spin

# Which way to spin when we lose them. Spinning away from where they
# just were can cost most of a full rotation on a ring this small.
SEARCH_TOWARD_LAST_SEEN = True


# ============================================================
# DISTANCE SETTINGS (mm)
# ============================================================

DETECT_DISTANCE_MM = 900    # opponent seen up to 90 cm
FORK_DOWN_DISTANCE_MM = 120 # at 12 cm, drop to the floor to slide under
# The lift triggers on EITHER of two things, whichever happens first:
#
#   distance  - get_distance() reports 0 when the sensor is inside its
#               20 mm minimum, which means something is pressed against
#               us. Simple and hard to fool.
#   motor stall - both sides falling short of their command.
#
# Either alone has failed in testing, so both are wired up and the
# first one to fire wins.
LIFT_DISTANCE_MM = 70       # this close counts as contact

# A sensor that drops out for a tick or two keeps its last reading for
# this long. Stops a one tick dropout on one side from flipping the
# steering to the other side.
SENSOR_HOLD_MS = 40


# ============================================================
# ARM POSITIONS
#
# ZERO IS THE ARM FULLY UP, which is where it physically sits
# when you press RUN. No calibration routine, the arm is already
# in a known place.
#
# Down is negative. The targets are stored in MOTOR degrees, because
# that is what the motor encoder actually counts and what was read
# with arm_readout.py and tested on the robot. The gear ratio only
# converts them to real arm angles for reference.
#
# If the arm gear is ever physically swapped, these motor numbers
# no longer land in the same place. Re-measure with arm_readout.py.
# ============================================================

ARM_TOP = 0                 # fully up, PRE MATCH ONLY
ARM_GROUND = -510           # wedge on the floor, was -488, lowered ~7 arm degrees
ARM_LIFT = -430             # opponent lifted

ARM_GROUND_DEG = ARM_GROUND / ARM_RATIO     # about -170 arm degrees
ARM_LIFT_DEG = ARM_LIFT / ARM_RATIO         # about -143 arm degrees

# There is no separate "ready" height any more. The wedge drops to the
# floor once when the countdown ends and lives there for the whole
# round, searching included, so a robot that rushes us always meets a
# wedge that is already in position. The only movement is the ~27 degree
# lift, and it returns to the floor immediately after.
#
# ARM_TOP (0) is the pre-match position ONLY. Nothing in the match loop
# ever commands it. Raising the arm ~143 degrees while in contact would
# be a flip, which rule 5.1 prohibits.


# ============================================================
# ARM SPEEDS
# ============================================================

ARM_DROP_SPEED = 100        # startup drop, no reason to be gentle
ARM_DOWN_SPEED = 100        # drop fast, it has to beat the robot there
ARM_LIFT_SPEED = 55         # was 22, too slow to finish a lift mid charge


# ============================================================
# WHITE LINE SETTINGS
#
# Same rule for all three sensors:
#   < 60%  = ignore
#   >= 60% = possible white border
#
# Needs 3 readings in a row before reacting.
# ============================================================

WHITE_THRESHOLD = 60

# The ring has RED start markings (2 x 20 cm rectangles) on the black
# surface. Red reflects far more than matte black, so brightness alone
# would read them as the border and send the robot fleeing from its own
# start position. Hue separates them: white has no dominant hue, red
# sits at the ends of the scale.
RED_HUE_LOW = 330           # above this is red
RED_HUE_HIGH = 22           # below this is red
# Measured with sensor_readout.py (LED at 100%):
#   black  b14-25            -> ignored by brightness alone
#   white  b100, hue 26-40   -> must count as border
#   red    b72-100, hue 11-20 -> must be ignored
# The old cutoff of 30 made white at hue 26 and 28 (rear and front
# right sensors) look red, so those two sensors could not see the
# border at all. 22 sits between red (max ~20) and white (min 26).
# The gap is small, so if in doubt this errs toward seeing white:
# a false escape on a red mark costs a moment, a missed border
# costs the round. Re-check with sensor_readout.py at the venue.
# At ~23 cm/s the 5 cm band takes about 220 ms to cross, and 3 readings
# at a 5 ms loop costs 15 ms. Plenty of margin, so take the extra
# confirmation and buy noise immunity with it.
LINE_CONFIRM_COUNT = 3


# ============================================================
# ESCAPE TIMING (loop ticks, 1 tick = 5 ms)
# ============================================================

# 5 ms instead of 10. The border band is only 5 cm wide, so every
# millisecond between seeing white and reversing is distance travelled.
# Rule 8.18: after the start button is pressed, the robot must not move
# for at least 5 seconds. Rule 8.26 (item 3) makes moving early a warning, and
# a repeat loses the round. Nothing moves in that window, arm included.
START_DELAY_MS = 5300       # 5 s plus margin

# ---- OPENING ----
#
# We are heavy, torque rich and slow (~23 cm/s theoretical). A light fast opponent
# beats us to the middle no matter what we do, so racing them is a game
# we lose. Instead: advance slowly with the wedge already on the floor
# and let them arrive at speed. Their momentum goes into climbing our
# wedge, which is exactly where we want it, and after the first hit the
# match becomes a torque contest we are built to win.
#
# Rules 8.19 and 8.26.5 only punish a robot that never moves for a
# minute, so a slow advance is safe.
OPENING_MS = 350            # how long to stay braced
OPENING_SPEED = 22          # barely creeping, maximum grip, wedge down

# If the opponent reaches us before the arm finishes coming down,
# the fork is at some useless mid height where it can catch on them
# or let them under us. In that case abandon the lift for the whole
# round: put the arm back up out of the way and just push.
CONTACT_DISTANCE_MM = 110   # close enough that the arm is out of time
# The wedge rests on the floor, so the motor often stalls short of the
# commanded angle. Measured in the air it reaches -488 motor degrees, but loaded it
# may stop well before that, and a tight tolerance was latching push
# mode every round and disabling the lift entirely.
ARM_DOWN_TOLERANCE = 120    # motor degrees, how close counts as "down"

# ============================================================
# SHOVING MATCH DETECTION
#
# The motors report their real velocity. Comparing that to what we
# commanded tells us what is physically happening:
#
#   commanded full ahead, wheels barely turning  -> deadlock
#   commanded full ahead, wheels turning backward -> losing
#
# Deadlock is survivable, rule 8.21 restarts a locked match. Being
# driven backward is not, so that one gets an escape.
# ============================================================

# Contact is a mechanical event, not an optical one. At zero range the
# distance sensors are useless, but the drive motors are not: command
# full power, watch the wheels slow, that is contact.
CONTACT_CONFIRM_MS = 40     # brief, contact is abrupt
WEDGE_ENTRY_MS = 220        # keep driving after contact so the wedge slides under

# TRACTION, NOT TORQUE, IS THE LIMIT.
#
# Through the 12:36 the motors can push harder than the tyres can grip.
# At 2.4 kg the wheels can only put roughly 15 to 19 N into the floor before they
# slip. Slamming from 0 to 100 just spins the rubber, and a spinning
# wheel has less grip than a gripping one. Ramping the command keeps
# the tyres below the slip point, so the robot actually accelerates
# faster than it would at instant full power.
RAMP_PCT_PER_TICK = 6       # ~1200 percent per second, about 0.08 s to full

# Contact is detected per side, by comparing what each side was told to
# do against what it actually did.
#
# Averaging the two sides does not work: steering can command 100 and
# -10, which averages 45 and looks like a stall even though the robot is
# driving perfectly well. Per side comparison is immune to that, and
# also to pivots, where both sides DO reach their commanded speeds.
STALL_MIN_COMMAND = 35      # ignore sides that were barely asked to move
STALL_RATIO = 0.45          # below this fraction of command = that side is stalled

# Still needed for the pushed backward test, which is about direction
# of travel rather than stalling.
COMMANDED_FORWARD_MIN = 40

PUSHED_VELOCITY_PCT = -6    # below this we are going backward under power

DEADLOCK_CONFIRM_MS = 500   # how long to shove before trying something else
PUSHED_CONFIRM_MS = 120     # react to losing ground much faster

BREAK_REVERSE_MS = 130      # back off to unload the contact (deadlock only)
BREAK_TURN_MS = 200         # swing off their centre line
BREAK_TURN_POWER = 90
BREAK_COOLDOWN_MS = 700     # don't re-trigger immediately after a break

LOOP_MS = 5                 # main loop period

# At ~23 cm/s, 280 ms of reverse is at most about 6 cm, and less in
# practice because the ramp spends part of it reversing direction.
# The border band is 5 cm, so this is tight. Confirm with an edge test
# and raise it if the robot does not fully clear the white.
ESCAPE_DRIVE_MS = 280       # backing up / driving out of the line
# Reverted to the pre-test values at the driver's call. For reference,
# the measured turn rate is 144 deg/s at power 80, so 190 ms is only
# about 22 degrees of turn.
ESCAPE_TURN_MS = 190        # spinning away from the edge
ESCAPE_TURN_POWER = 80
LIFT_HOLD_MS = 600          # pushing after the opponent leaves the sensors

ESCAPE_DRIVE_TICKS = ESCAPE_DRIVE_MS // LOOP_MS
ESCAPE_TURN_TICKS = ESCAPE_TURN_MS // LOOP_MS
LIFT_HOLD_TICKS = LIFT_HOLD_MS // LOOP_MS
SENSOR_HOLD_TICKS = SENSOR_HOLD_MS // LOOP_MS


# ============================================================
# STATE
# ============================================================

last_arm_target = -99999

# Once lifting starts, don't lower again until the opponent is lost.
lift_latched = False

# Latched for the rest of the round once the arm loses the race.
push_mode = False

# Debug
debug_last = ""

# Which side the opponent was last seen on. True = left.
last_seen_left = True

# Opening state
opening_ticks = 0

# Last commanded power, for the ramp
last_left_power = 0.0
last_right_power = 0.0

# Wedge entry state
contact_ticks = 0
wedge_ticks = 0

# Distance sensor dropout hold: [last good reading, ticks left]
left_memory = [9999, 0]
right_memory = [9999, 0]

# Shoving match state
deadlock_ticks = 0
pushed_ticks = 0
break_state = 0             # 0 none, 1 reversing, 2 turning
break_ticks = 0
break_cooldown = 0
break_turn_right = True
opponent_lost_ticks = 0

front_left_white_count = 0
front_right_white_count = 0
back_white_count = 0

ESCAPE_NONE = 0
ESCAPE_BACKWARD = 1
ESCAPE_FORWARD = 2
ESCAPE_LEFT = 3
ESCAPE_RIGHT = 4

escape_state = ESCAPE_NONE
escape_ticks = 0
turn_right_after_escape = True
alternate_direction = False


# ============================================================
# HELPERS
# ============================================================

def limit_power(power):
    if power > 100:
        return 100
    if power < -100:
        return -100
    return power


# ============================================================
# DRIVE
# ============================================================

def ramp(target, current):
    """Move current toward target by at most RAMP_PCT_PER_TICK."""
    change = target - current

    if change > RAMP_PCT_PER_TICK:
        return current + RAMP_PCT_PER_TICK

    if change < -RAMP_PCT_PER_TICK:
        return current - RAMP_PCT_PER_TICK

    return target


def drive_power(left_power, right_power):
    global last_left_power, last_right_power

    left_power = limit_power(left_power)
    right_power = limit_power(right_power)

    left_power = ramp(left_power, last_left_power)
    right_power = ramp(right_power, last_right_power)

    last_left_power = left_power
    last_right_power = right_power

    if left_power >= 0:
        left_drive.spin(FORWARD, left_power, PERCENT)
    else:
        left_drive.spin(REVERSE, -left_power, PERCENT)

    if right_power >= 0:
        right_drive.spin(FORWARD, right_power, PERCENT)
    else:
        right_drive.spin(REVERSE, -right_power, PERCENT)


def stop_drive():
    global last_left_power, last_right_power

    last_left_power = 0.0
    last_right_power = 0.0

    left_drive.stop(BRAKE)
    right_drive.stop(BRAKE)


# ============================================================
# ARM CONTROL
# ============================================================

def move_arm(target, speed):
    global last_arm_target

    # Don't resend the same command every loop
    if abs(target - last_arm_target) < 0.5:
        return

    last_arm_target = target

    arm_motor.set_velocity(speed, PERCENT)
    arm_motor.spin_to_position(target, DEGREES, False)


def arm_down():
    if not ARM_ENABLED:
        return

    move_arm(ARM_GROUND, ARM_DOWN_SPEED)


def arm_is_down():
    """True once the wedge has actually reached the floor."""
    if not ARM_ENABLED:
        return True         # nothing to wait for, never enter push mode

    return abs(arm_motor.position(DEGREES) - ARM_GROUND) <= ARM_DOWN_TOLERANCE


def arm_lift():
    if not ARM_ENABLED:
        return

    if not LIFT_ENABLED:
        # wedge stays flat on the floor, no lifting motion
        arm_down()
        return

    move_arm(ARM_LIFT, ARM_LIFT_SPEED)


# ============================================================
# OPTICAL SETUP
# ============================================================

def setup_optical_sensors():
    for sensor in (line_front_left, line_front_right, line_back):
        sensor.set_light_power(100, PERCENT)
        sensor.set_light(LedStateType.ON)

    wait(300, MSEC)


# ============================================================
# WHITE DETECTION
# ============================================================

def reads_white(sensor):
    """True if this sensor is over the white border, not a red marking."""

    if sensor.brightness() < WHITE_THRESHOLD:
        return False

    hue = sensor.hue()

    if hue >= RED_HUE_LOW or hue <= RED_HUE_HIGH:
        return False        # red start marking, not the border

    return True


def front_left_on_white():
    global front_left_white_count

    if reads_white(line_front_left):
        front_left_white_count += 1
    else:
        front_left_white_count = 0

    if front_left_white_count >= LINE_CONFIRM_COUNT:
        front_left_white_count = LINE_CONFIRM_COUNT
        return True

    return False


def front_right_on_white():
    global front_right_white_count

    if reads_white(line_front_right):
        front_right_white_count += 1
    else:
        front_right_white_count = 0

    if front_right_white_count >= LINE_CONFIRM_COUNT:
        front_right_white_count = LINE_CONFIRM_COUNT
        return True

    return False


def back_on_white():
    global back_white_count

    if reads_white(line_back):
        back_white_count += 1
    else:
        back_white_count = 0

    if back_white_count >= LINE_CONFIRM_COUNT:
        back_white_count = LINE_CONFIRM_COUNT
        return True

    return False


# ============================================================
# BORDER SAFETY - HIGHEST PRIORITY
# ============================================================

def handle_border():
    global escape_state, escape_ticks
    global turn_right_after_escape, alternate_direction

    left_white = front_left_on_white()
    right_white = front_right_on_white()
    back_white = back_on_white()

    # ---------- FRONT BORDER ----------
    if left_white or right_white:

        if escape_state != ESCAPE_BACKWARD:

            if left_white and not right_white:
                turn_right_after_escape = True

            elif right_white and not left_white:
                turn_right_after_escape = False

            else:
                alternate_direction = not alternate_direction
                turn_right_after_escape = alternate_direction

            escape_state = ESCAPE_BACKWARD
            escape_ticks = 0

        drive_power(-100, -100)
        return True

    # ---------- BACK BORDER ----------
    if back_white:

        if escape_state != ESCAPE_FORWARD:
            alternate_direction = not alternate_direction
            turn_right_after_escape = alternate_direction

            escape_state = ESCAPE_FORWARD
            escape_ticks = 0

        drive_power(100, 100)
        return True

    # ---------- KEEP REVERSING ----------
    if escape_state == ESCAPE_BACKWARD:
        drive_power(-100, -100)
        escape_ticks += 1

        if escape_ticks >= ESCAPE_DRIVE_TICKS:
            escape_ticks = 0
            escape_state = ESCAPE_RIGHT if turn_right_after_escape else ESCAPE_LEFT

        return True

    # ---------- KEEP MOVING FORWARD ----------
    if escape_state == ESCAPE_FORWARD:
        drive_power(100, 100)
        escape_ticks += 1

        if escape_ticks >= ESCAPE_DRIVE_TICKS:
            escape_ticks = 0
            escape_state = ESCAPE_RIGHT if turn_right_after_escape else ESCAPE_LEFT

        return True

    # ---------- TURN RIGHT ----------
    if escape_state == ESCAPE_RIGHT:
        drive_power(ESCAPE_TURN_POWER, -ESCAPE_TURN_POWER)
        escape_ticks += 1

        if escape_ticks >= ESCAPE_TURN_TICKS:
            escape_ticks = 0
            escape_state = ESCAPE_NONE

        return True

    # ---------- TURN LEFT ----------
    if escape_state == ESCAPE_LEFT:
        drive_power(-ESCAPE_TURN_POWER, ESCAPE_TURN_POWER)
        escape_ticks += 1

        if escape_ticks >= ESCAPE_TURN_TICKS:
            escape_ticks = 0
            escape_state = ESCAPE_NONE

        return True

    return False


# ============================================================
# DISTANCE SENSOR
# ============================================================

def get_distance(sensor):
    """Distance in mm, or 9999 for nothing there.

    The sensor's minimum range is about 20 mm. A reading below that used
    to be thrown away as noise, which meant the opponent appeared to
    vanish at the exact moment we touched them. Below minimum range means
    they are pressed against us, so report contact instead.
    """
    if sensor.is_object_detected():
        value = sensor.object_distance(MM)

        if value < 20:
            return 0        # in contact

        if value <= 2000:
            return value

    return 9999


def read_distance(sensor, memory):
    """get_distance with a short hold over dropouts.

    A small robot often sits at the edge of one beam, so that sensor
    blinks on and off. Without this, each blink flips the steering
    between "both see it" and "one sees it" and the robot twitches.
    """
    value = get_distance(sensor)

    if value <= DETECT_DISTANCE_MM:
        memory[0] = value
        memory[1] = SENSOR_HOLD_TICKS
        return value

    if memory[1] > 0:
        memory[1] -= 1
        return memory[0]

    return 9999


# ============================================================
# ATTACK
# ============================================================

def drive_velocity():
    """Average forward wheel speed in percent. Negative means going backward."""
    return (left_drive.velocity(PERCENT) + right_drive.velocity(PERCENT)) / 2.0


def debug(message):
    """Print only when the message changes, so the log stays readable."""
    global debug_last

    if not DEBUG:
        return

    if message == debug_last:
        return

    debug_last = message
    print(message)


def side_stalled(commanded, actual):
    """True if this side is moving far slower than it was told to."""
    if abs(commanded) < STALL_MIN_COMMAND:
        return False        # barely asked to move, nothing to conclude

    return abs(actual) < abs(commanded) * STALL_RATIO


def in_contact_now():
    """Both sides falling short of their command means we hit something.

    Works while steering, because each side is judged against its own
    command rather than against an average. Works during a pivot too,
    since a free pivot has both sides reaching their commanded speeds.
    The ramp is handled for free: the command itself is small during it.
    """
    left_stalled = side_stalled(last_left_power,
                                left_drive.velocity(PERCENT))
    right_stalled = side_stalled(last_right_power,
                                 right_drive.velocity(PERCENT))

    return left_stalled and right_stalled


def driving_forward():
    """True when both sides are being asked to go forward."""
    return (last_left_power >= COMMANDED_FORWARD_MIN and
            last_right_power >= COMMANDED_FORWARD_MIN)


def handle_shoving():
    """Runs while in contact. Returns True if it has taken over the drive.

    Deadlock: neither robot moving. We keep pushing, because backing off
    hands them free ground, and a true lockup gets restarted by the judge.
    After DEADLOCK_CONFIRM_MS we break off and come back at an angle,
    since hitting a corner beats hitting a wedge head on.

    Losing: wheels being driven backward. Break off immediately. Grinding
    it out against a stronger robot only moves us closer to our own edge.
    """
    global deadlock_ticks, pushed_ticks
    global break_state, break_ticks, break_cooldown, break_turn_right

    if break_cooldown > 0:
        break_cooldown -= 1

    # ---------- already breaking off ----------
    # State 1 is reverse, and it is ONLY used for deadlock. When we are
    # being pushed backward, commanding reverse adds our own motors to
    # their push and drives us off our own edge faster. In that case we
    # skip straight to state 2 and pivot, which sheds their wedge and
    # gets us off their centre line without giving up ground.
    if break_state == 1:
        drive_power(-100, -100)
        break_ticks += 1

        if break_ticks >= BREAK_REVERSE_MS // LOOP_MS:
            break_ticks = 0
            break_state = 2

        return True

    if break_state == 2:
        if break_turn_right:
            drive_power(BREAK_TURN_POWER, -BREAK_TURN_POWER)
        else:
            drive_power(-BREAK_TURN_POWER, BREAK_TURN_POWER)

        break_ticks += 1

        if break_ticks >= BREAK_TURN_MS // LOOP_MS:
            break_ticks = 0
            break_state = 0
            break_cooldown = BREAK_COOLDOWN_MS // LOOP_MS

        return True

    # ---------- measure what is happening ----------
    # Being pushed backward is about direction of travel, so this one
    # does need both sides driving forward to mean anything.
    if not driving_forward():
        pushed_ticks = 0
        deadlock_ticks = 0
        return False

    speed = drive_velocity()

    if speed <= PUSHED_VELOCITY_PCT:
        pushed_ticks += 1
    else:
        pushed_ticks = 0

    # Pushing a lifted robot is slow and looks exactly like a stall.
    # That is winning, not a deadlock, so never break off from it.
    if in_contact_now() and not lift_latched:
        deadlock_ticks += 1
    else:
        deadlock_ticks = 0

    if break_cooldown > 0:
        return False

    # ---------- losing ground, get out now ----------
    if pushed_ticks >= PUSHED_CONFIRM_MS // LOOP_MS:
        pushed_ticks = 0
        deadlock_ticks = 0
        break_turn_right = not break_turn_right
        break_state = 2         # pivot, never reverse, see note above
        break_ticks = 0
        return True

    # ---------- stuck, try a different angle ----------
    if deadlock_ticks >= DEADLOCK_CONFIRM_MS // LOOP_MS:
        deadlock_ticks = 0
        break_turn_right = not break_turn_right
        break_state = 1
        break_ticks = 0
        return True

    return False


def attack_power():
    """Full attack normally, reduced while still in the bracing opening."""
    if opening_ticks > 0:
        return OPENING_SPEED

    return ATTACK_SPEED


def drive_toward(left_distance, right_distance,
                 left_detected, right_detected):
    """Proportional steering toward the opponent."""

    forward = attack_power()
    closest = min(left_distance, right_distance)

    # Lifted, or pressed right against us: they are on the wedge.
    # Whichever sensor happens to see them, the answer is straight ahead.
    if lift_latched or closest <= LIFT_DISTANCE_MM:
        drive_power(forward, forward)
        return

    if left_detected and right_detected:
        difference = left_distance - right_distance

        if abs(difference) < CENTER_TOLERANCE_MM:
            # lined up, go straight at them
            drive_power(forward, forward)
            return

        correction = abs(difference) * STEER_GAIN

        if correction > MAX_CORRECTION:
            correction = MAX_CORRECTION

        inner = forward - correction

        if left_distance < right_distance:
            # opponent on the left
            drive_power(inner, forward)
        else:
            drive_power(forward, inner)

        return

    # ---------- only one sensor sees them ----------
    if closest <= SINGLE_NEAR_MM:
        inner = forward * SINGLE_NEAR_FACTOR
    else:
        inner = forward * SINGLE_FAR_FACTOR

    if left_detected:
        drive_power(inner, forward)
    else:
        drive_power(forward, inner)


def attack_opponent():
    global lift_latched, opponent_lost_ticks, push_mode
    global contact_ticks, wedge_ticks, last_seen_left

    left_distance = read_distance(distance_left, left_memory)
    right_distance = read_distance(distance_right, right_memory)

    left_detected = left_distance <= DETECT_DISTANCE_MM
    right_detected = right_distance <= DETECT_DISTANCE_MM

    if not left_detected and not right_detected:
        return False

    opponent_lost_ticks = 0

    # ---------- CLOSEST ----------
    closest = 9999

    if left_detected:
        closest = left_distance

    if right_detected and right_distance < closest:
        closest = right_distance

    # Remember the bearing so search can spin the short way round
    if left_detected and right_detected:
        last_seen_left = left_distance <= right_distance
    elif left_detected:
        last_seen_left = True
    else:
        last_seen_left = False

    # ---------- SHOVING MATCH ----------
    #
    # Only relevant in contact. Takes over the drive when it fires,
    # but the arm still gets commanded below it.

    if closest <= CONTACT_DISTANCE_MM:
        if handle_shoving():
            if push_mode:
                arm_down()
            elif lift_latched:
                arm_lift()
            return True

    # ---------- PUSH MODE CHECK ----------
    #
    # Decided once, at the first moment of contact. If the arm is not
    # down by then it never will be in time, so give up on the lift.

    # Only decidable during the opening. After that the wedge has had
    # plenty of time to reach the floor, and latching push mode late
    # kills the lift for no good reason.
    if not push_mode and not lift_latched and opening_ticks > 0:
        if closest <= CONTACT_DISTANCE_MM and not arm_is_down():
            push_mode = True
            debug("push mode latched: arm at %d, wanted %d"
                  % (arm_motor.position(DEGREES), ARM_GROUND))

    if push_mode:
        # Finish the drop instead of retreating. Pushing with the wedge
        # flat on the floor is correct sumo, and downward travel cannot
        # lever the opponent the way raising into them would.
        arm_down()
        debug("PUSH MODE, no lift this round")
        drive_toward(left_distance, right_distance,
                     left_detected, right_detected)
        return True

    # ---------- FORKLIFT ----------
    #
    # The lift is triggered by contact, not by distance. Distance tells
    # us where they are; the drive motors tell us when we have arrived.
    # After contact we keep driving for WEDGE_ENTRY_MS so the wedge gets
    # under them, then lift.

    if in_contact_now():
        contact_ticks += 1
    else:
        contact_ticks = 0

    in_contact = (contact_ticks >= CONTACT_CONFIRM_MS // LOOP_MS
                  or closest <= LIFT_DISTANCE_MM)

    if lift_latched:
        # already lifting, keep going to the lift height
        arm_lift()
        debug("LIFTING")

    elif in_contact:
        # wedge is against them, count the entry dwell
        wedge_ticks += 1

        if wedge_ticks >= WEDGE_ENTRY_MS // LOOP_MS:
            lift_latched = True
            arm_lift()
            debug("LIFT triggered, dist %d, arm %d"
                  % (closest, arm_motor.position(DEGREES)))
        else:
            arm_down()
            debug("contact, counting dwell, dist %d" % closest)

    elif closest <= FORK_DOWN_DISTANCE_MM or opening_ticks > 0:
        # Close in, wedge on the floor. Deliberately NOT resetting the
        # dwell here: contact flickers, and restarting the count on every
        # lost tick meant the lift could never finish counting.
        arm_down()

    else:
        # far away, start the dwell over
        wedge_ticks = 0
        arm_down()

    # ---------- STEERING ----------
    drive_toward(left_distance, right_distance,
                 left_detected, right_detected)

    return True


# ============================================================
# SEARCH
# ============================================================

def search_opponent():
    global lift_latched, opponent_lost_ticks
    global deadlock_ticks, pushed_ticks, contact_ticks, wedge_ticks

    opponent_lost_ticks += 1

    # Just lifted and lost sensor view, keep lifting and pushing
    if lift_latched and opponent_lost_ticks < LIFT_HOLD_TICKS:
        arm_lift()
        drive_power(100, 100)
        return

    if opponent_lost_ticks >= LIFT_HOLD_TICKS:
        lift_latched = False
        deadlock_ticks = 0
        pushed_ticks = 0
        contact_ticks = 0
        wedge_ticks = 0

    # Wedge stays on the floor while searching, so anything that rushes
    # us runs into it rather than into bare frame.
    arm_down()

    # ---------- OPENING: they are straight ahead ----------
    #
    # At the start the opponent is directly opposite us behind their own
    # red line. Spinning to look for someone we already know the bearing
    # of wastes the one second that decides most rounds. Creep forward
    # instead, wedge down, and let the sensors pick them up.

    if opening_ticks > 0:
        drive_power(OPENING_SPEED, OPENING_SPEED)
        return

    # ---------- spin toward where they last were ----------
    if SEARCH_TOWARD_LAST_SEEN and not last_seen_left:
        drive_power(SEARCH_SPEED, -SEARCH_SPEED)
    else:
        drive_power(-SEARCH_SPEED, SEARCH_SPEED)


# ============================================================
# MAIN
# ============================================================

def main():
    global last_arm_target, opening_ticks

    # HOLD during the countdown. The motors actively resist being moved
    # rather than just coasting, so a robot that jumps the start and
    # shoves us gets pushed back against the drive PID. Holding position
    # is not moving, so it stays inside rule 8.18.
    left_drive.set_stopping(HOLD)
    right_drive.set_stopping(HOLD)
    arm_motor.set_stopping(HOLD)

    left_drive.stop(HOLD)
    right_drive.stop(HOLD)

    setup_optical_sensors()

    # ----------------------------------------------------------
    # STARTUP
    #
    # The arm must be FULLY UP before the start button is pressed.
    # That position is zero, everything below it is negative.
    #
    # Then NOTHING moves for 5 seconds. Not the wheels, not the arm.
    # The drive motors sit in HOLD through the countdown so they resist
    # being shoved by anyone who jumps the start.
    #
    # When the countdown ends the wedge is sent straight to the floor
    # without waiting for it, so the robot drives off while it drops.
    # ----------------------------------------------------------

    arm_motor.set_position(ARM_TOP, DEGREES)
    last_arm_target = -99999

    remaining = START_DELAY_MS

    while remaining > 0:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("start in %.1f" % (remaining / 1000.0))
        wait(100, MSEC)
        remaining -= 100

    # Countdown done. Switch the drive to BRAKE for the match, since
    # HOLD fights every intentional direction change.
    left_drive.set_stopping(BRAKE)
    right_drive.set_stopping(BRAKE)

    # Start the drop, do not block on it.
    if ARM_ENABLED:
        arm_motor.set_velocity(ARM_DROP_SPEED, PERCENT)
        arm_motor.spin_to_position(ARM_GROUND, DEGREES, False)
        last_arm_target = ARM_GROUND

    brain.screen.clear_screen()
    brain.screen.print("ready")

    if DEBUG:
        wait(600, MSEC)     # let the wedge settle on the floor
        print("wedge resting at %d, ARM_GROUND is %d, off by %d"
              % (arm_motor.position(DEGREES), ARM_GROUND,
                 abs(arm_motor.position(DEGREES) - ARM_GROUND)))

    opening_ticks = OPENING_MS // LOOP_MS

    while True:

        if opening_ticks > 0:
            opening_ticks -= 1

        # PRIORITY 1: white border
        if handle_border():
            # Readings from before the escape are stale now
            left_memory[1] = 0
            right_memory[1] = 0
            wait(LOOP_MS, MSEC)
            continue

        # PRIORITY 2: attack
        if attack_opponent():
            wait(LOOP_MS, MSEC)
            continue

        # PRIORITY 3: search
        search_opponent()
        wait(LOOP_MS, MSEC)


main()

# WROsumo 2026 · Ibn Khaldoun Al Manar Boys

Autonomous sumo robot for the WROsumo 2026 category (WRO Saudi local pilot, Riyadh). Built on VEX EXP and programmed in VEXcode Python.

![Robot](photos/robot/robot_iso.jpg)

**Team:** Abdullah Alqahtani, Hisham Shaat
**Engineering notebook:** [link to notebook]

## The robot

A heavy, torque-geared pusher with a front wedge. It doesn't try to race the opponent. It drops the wedge, creeps forward, and lets the opponent ride up onto it, then wins the push.

| | |
|---|---|
| Platform | VEX EXP, EXP Robot Brain |
| Drive | 4 × Smart Motor 5.5W, 2 per side, chain 12T:36T (3:1), two driven rear wheels + front bearing wheel |
| Wheels | 6.5 cm, stock VEX tyres |
| Arm / wedge | 1 × Smart Motor 5.5W, 12T:36T, lifts about 27° |
| Sensors | 2 × Distance (front L/R), 3 × Optical (front L, front R, rear) |
| Battery | EXP Robot Battery, Li-Ion 7.2 V, 2500 mAh |
| Size | 20 × 20 × 20 cm at the start, about 32 cm long with the wedge down |
| Top speed | about 22.7 cm/s (calculated) |

## How it plays

Every 5 ms the robot runs one decision, in this priority order:

1. **Border:** an optical sensor sees white → reverse and turn away. Always wins.
2. **Attack:** a distance sensor sees the opponent within 90 cm → steer at them (proportional steering), wedge on the floor. On contact, keep driving 220 ms so the wedge gets under, then lift.
3. **Search:** nothing seen → spin toward where the opponent was last seen.

Contact is detected by the drive motors themselves: if the wheels move much slower than commanded, we've hit something. The same idea detects deadlocks (break off, come back at an angle) and being pushed backward (pivot away, never reverse).

Full details are in the engineering notebook.

## Modes

Two switches at the top of `src/sumo.py`:

| Mode | `ARM_ENABLED` | `LIFT_ENABLED` | Behaviour |
|---|---|---|---|
| Full (default) | `True` | `True` | Wedge on the floor, lift on contact |
| Wedge only | `True` | `False` | Wedge on the floor, never lifts |
| Pure push | `False` | any | Arm stays up, robot stays 20 × 20 cm |

## Running it

1. Open `src/sumo.py` in VEXcode EXP and download it to the Brain.
2. Raise the arm fully up by hand. That position is zero.
3. Place the robot behind the red start line and press Run.
4. The screen counts down 5.3 s and shows the battery level. Nothing moves until the countdown ends (rule 8.18).

## Repo layout

| Folder | Contents |
|---|---|
| `src/` | `sumo.py`, the competition code |
| `tools/` | `arm_readout.py`, `turn_test.py`, `sensor_readout.py` bench programs |
| `hardware/` | Parts list, port map, datasheet links |
| `calibration/` | Optical and distance sensor readings |
| `testing/` | Test log |
| `cad/` | Onshape link, exports, screenshots |
| `photos/` | Robot, team and build photos |
| `videos/` | Links to test and match videos |
| `notebook/` | Engineering notebook (PDF) |

## Port map

| Port | Device |
|---|---|
| 1, 2 | Right drive motors |
| 6, 7 | Left drive motors (reversed) |
| 3 / 8 | Distance sensor right / left |
| 4 / 9 / 5 | Optical front right / front left / rear |
| 10 | Arm motor |

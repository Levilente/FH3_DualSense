# Changelog

## 1.5.0

- Keyboard icons (Space, E, Q, R, Shift, C, S, W, Esc, Tab, arrows) in the game's prompts while the keyboard or mouse is the device in use; the look follows PlayStation / Xbox / keyboard live. The keys shown are the default key bindings of the keyboard gamepad. Needs platform 1.1.2.

## 1.4.0

- **Log off by default**: `DualSense.ini` `[DualSense]` `Log=1` writes the mod's ordinary lines to `platform.log`; problems are always logged.
- Hot reload (FH3 Mod Platform 1.2.0, a developer feature, off by default): the mod exports `fh3mod_shutdown`, so a rebuilt `DualSense.dll` can be swapped in with F9 while the game runs; the controller goes back to itself, the haptics end and the Xbox icons are put back first.
- Needs FH3 Mod Platform 1.1.1 or newer.
- The game's interface sounds drive haptics: menu moves, choices, page swells, tab switches, and events (skills, checkpoints, countdowns, speed traps, results, level-ups, tombola, notifications).

## 1.3.0

- PlayStation button icons (✕ ○ □ △, L1 R1 L2 R2) that follow the device in use, live.

## 1.2.0

- The device in use decides: a DualSense and an Xbox pad can both be connected; the one with the last real input gets the haptics, adaptive triggers and lights.
- L2: a brake pedal that starts with some resistance and hardens progressively; ABS pulses only while the car's ABS is really working.
- Stronger menu haptics.
- Removed the rev-limiter effects and the diagnostic logging (`RevLimiter`, `Log`).
- Needs FH3 Mod Platform 1.1.1 or later (the Extra Options mod gets the controller too: minimap follows the camera, Manufacturer button).

## 1.1.0

First release: FH2-Input's features on FH3 (see README).

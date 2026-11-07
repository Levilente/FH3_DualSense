# DualSense for Forza Horizon 3

A mod for the FH3 Mod Platform (1.1.0 or newer): FH2-Input's feel on Forza Horizon 3, over **USB and Bluetooth** alike. Copy `DualSense.dll` into `fh3-mods`.

**The controller** (the platform's part, settings in `fh3-mods\DualSense.ini` `[Controller]`): the DualSense is handed to the game as a gamepad, USB or Bluetooth, no drivers or Steam Input; Edge paddles and Fn buttons; touchpad click and swipes (D-pad); gyro steering (the mic button switches it, its light shows it); Circle/Cross swap.

**Keyboard and mouse** (the platform's part, `[Keyboard]`, `[Keys]`, `[Mouse]`): the keyboard is a gamepad of its own, merged with the controller, smooth steering and pedals; it joins at the first key press. Defaults: W/S throttle and brake, A/D steering, J L I K look, Space/Enter A, E/Backspace B, Q X, R Y, Left Shift LB, C RB, F/V stick clicks, Esc Menu, Tab View, arrows D-pad. The mouse looks around while driving (or follows its speed: `Look=Speed`); in the menus it moves the cursor, the wheel scrolls, left/right click are A/B.

**What the car feels like** (this mod), from the game's own controller feedback code (FH3's versions of the functions FH2-Input hooks in FH2), the player's Car::Update and the wheels' own contact with the road:
- **HD haptics**: the engine's hum at its revs, the road under each side of the car (gravel, dirt, grass, sand, snow, cobbles, kerbs, metal grates, bumpy tarmac), crashes by their strength, jumps and landings, gear changes, the game's own rumble, ticks and clicks in the menus. USB: the controller's audio endpoint. Bluetooth: haptics reports (0x32, 3 kHz), as found by [SAxense](https://apps.sdore.me/SAxense) (Sdore). `Vibration=1` uses the motors' emulation instead.
- **Adaptive triggers**: L2 a brake pedal that starts with some resistance and hardens progressively, pulses only while the car's ABS is really working (the front slip swinging up and down) and goes hard where it is when a wheel locks; R2 vibrates with wheel spin; gear changes knock the trigger pressed, crashes and landings jolt both, the road's texture is felt in the trigger you press.
- **Lights**: the light bar (revs, impacts, battery or a colour), player lights as a rev counter, the battery on the PS button, a low battery blinking red, the mic light for gyro steering.
- MODS page rows for the main settings; all of them in `DualSense.ini` `[DualSense]`.

Close Steam's PlayStation controller support and DS4Windows while playing. When the game ends or another window is in front, the controller goes back to itself. Nothing is written into the game's folder.

**PlayStation button icons** in the game's prompts (✕ ○ □ △, L1 R1 L2 R2) while the DualSense is in use; the game's own Xbox icons when an Xbox pad is. The look follows the device in use at once: the new icons are written over the ones in the game's memory (found by their bytes, a search that runs on a low-priority thread from 25 s after the start, as in alezwork's FH2-Input). `scripts/gen_icons.py` draws them from the game's own icons.

**The device in use decides**: the one that gave the last real input (a DualSense press, an Xbox pad's button, trigger past a quarter or stick past a third) gets the haptics, triggers and lights; switch to an Xbox pad and the DualSense goes quiet, press the DualSense and it takes over again (a switch waits 0.6 s). It starts with whichever you touch first.

Not (yet) on FH3: the game's events (skills, combos, checkpoints, level-ups) and its interface sounds as haptics, the settings inside Settings > Controls (they are on the MODS page).

Build: `cmake -S mods/dualsense -B build -DCMAKE_TOOLCHAIN_FILE=cmake/mingw-w64-x86_64.cmake && cmake --build build`.

Credits: the feature set and its feel follow [FH2-Input](https://github.com/alezwork/FH2-Input) by alezwork; report layouts from the Linux `hid-playstation` driver; trigger effects from Nielk1's notes; Bluetooth haptics from SAxense by Sdore.

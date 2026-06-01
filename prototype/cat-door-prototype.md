# Smart Cat Door Prototype

This is a first-pass concept for a Raspberry Pi cat door with night vision, a motorized flap, and Telegram approval controls.

## What It Does

1. A motion event happens near the flap.
2. The Raspberry Pi grabs a night-vision image from the camera.
3. A Telegram bot sends that image to your phone.
4. You tap `Open Door` or `Keep Closed`.
5. The actuator moves the flap.
6. A reed switch confirms the flap is shut again.

## Recommended Prototype Architecture

- `Raspberry Pi Zero 2 W`
  - Small enough to fit in a compact control box.
  - Official page: <https://www.raspberrypi.com/products/raspberry-pi-zero-2-w>
- `Raspberry Pi Camera Module 3 NoIR`
  - Official NoIR page: <https://www.raspberrypi.com/products/camera-module-3/?variant=camera-module-3-noir>
  - Camera documentation: <https://www.raspberrypi.com/documentation/hardware/camera/>
- `High-torque metal gear servo`
  - Simple prototype-friendly actuator that is easier than a custom DC gearmotor linkage.
  - Example: <https://www.adafruit.com/product/1142>
- `Magnetic reed switch`
  - Lets the Pi know whether the flap actually closed.
  - Example: <https://www.adafruit.com/product/375>
- `Mini PIR sensor`
  - Optional wake-up trigger so the Pi is not reacting to every frame all the time.
  - Example: <https://www.adafruit.com/product/4871>
- `Weatherproof enclosure`
  - Keeps the Pi, fuse, and regulators protected.
  - Example enclosure family: <https://www.polycase.com/electrical-enclosures>
- `Telegram Bot API`
  - Used to send the snapshot and receive your button press.
  - Docs: <https://core.telegram.org/bots/api>

## Why I Chose A Servo For The Prototype

For the very first version, a servo is the cleanest way to make the flap move because it already gives you controlled position without adding a separate H-bridge and feedback loop.

If your flap ends up being heavy or sticky, the next upgrade is:

- `DC geared motor`
- `motor driver`
- `limit switches`

Example driver if you go that route later:

- Adafruit DRV8871: <https://www.adafruit.com/product/3190>

## Safety Notes

- Do not drive a motor directly from Raspberry Pi GPIO.
  - Raspberry Pi warns to use a motor controller board instead: <https://www.raspberrypi.com/documentation/hardware/raspberrypi/gpio/>
- Add a manual release so you can open the flap even if power or software fails.
- Add soft-close timing so the door does not slam on a cat.
- Keep the main box indoors or in a genuinely weatherproof enclosure for the permanent build.

## Files In This Prototype Pack

- `cat-door-overview.svg`
- `cat-door-cutaway.svg`
- `cat-door-telegram.svg`

Render previews are generated into `rendered/`.

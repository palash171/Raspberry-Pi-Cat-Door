# Cat Door Software

This folder contains the Raspberry Pi application for the cat door project.
The current live workflow is:

1. The PIR sensor detects motion.
2. The Raspberry Pi captures a photo.
3. The photo is sent to Telegram.
4. The user chooses `Open Door` or `Keep Closed`.
5. The door only opens after approval.

At the moment, manual approval is the main operating mode. The code also
includes hooks for a servo, a reed switch, and optional image-based detection,
but those parts depend on the final hardware setup.

## Files you will usually use

- `run_cat_door.sh` - easiest way to run the software
- `setup_pi.sh` - first-time Raspberry Pi setup
- `.env` - local settings such as Telegram values and GPIO pins
- `HOOKUP_AND_RUN.md` - full setup and testing order
- `TELEGRAM_SETUP.md` - bot setup and chat ID guide

## What you normally need to edit

For a standard setup, only edit `.env`.

These are the values most likely to change:

- `CAT_DOOR_TELEGRAM_BOT_TOKEN`
- `CAT_DOOR_TELEGRAM_CHAT_ID`
- `CAT_DOOR_PIR_PIN`
- `CAT_DOOR_REED_SWITCH_PIN`
- `CAT_DOOR_SERVO_PIN`
- `CAT_DOOR_ENABLE_GPIO_HARDWARE`
- `CAT_DOOR_ENABLE_SERVO_HARDWARE`
- `CAT_DOOR_CAMERA_CAPTURE_TIMEOUT_MS`
- `CAT_DOOR_PIR_SETTLE_SECONDS`

## Run commands

Run commands from inside `software/`.

```bash
./run_cat_door.sh show-chat-id
./run_cat_door.sh status
./run_cat_door.sh debug-updates
./run_cat_door.sh text-test
./run_cat_door.sh approval-test
./run_cat_door.sh photo-test
./run_cat_door.sh monitor-once
./run_cat_door.sh monitor-loop
```

## If you need to change code

- `cat_door/config.py` - loads `.env` values
- `cat_door/workflow.py` - main event flow
- `cat_door/camera.py` - camera capture command and timing
- `cat_door/telegram_bot.py` - Telegram messages and approval buttons
- `cat_door/sensors.py` - PIR and reed switch handling
- `cat_door/door_controller.py` - servo behaviour
- `cat_door/detector.py` - detector integration

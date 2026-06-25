# Hookup And Run

This guide is for getting the cat door software running on a Raspberry Pi.
It is written for the normal case where the code is already cloned and the next
job is to configure the Pi, wire the hardware, and test each stage in order.

## 1. Open the project on the Pi

From the cloned repository:

```bash
cd software
```

## 2. Run the first-time setup

```bash
./setup_pi.sh
```

This creates the virtual environment, installs the Python packages, and creates
`.env` from `.env.example` if it does not already exist.

## 3. Edit `.env`

Open the local config file:

```bash
nano .env
```

For a normal setup, these are the main values to fill in or check:

```env
CAT_DOOR_TELEGRAM_BOT_TOKEN=
CAT_DOOR_TELEGRAM_CHAT_ID=
CAT_DOOR_PIR_PIN=17
CAT_DOOR_REED_SWITCH_PIN=27
CAT_DOOR_SERVO_PIN=18
CAT_DOOR_GPIOZERO_PIN_FACTORY=lgpio
CAT_DOOR_ENABLE_GPIO_HARDWARE=true
CAT_DOOR_ENABLE_SERVO_HARDWARE=true
CAT_DOOR_NOTIFY_ON_ANY_MOTION=true
CAT_DOOR_DETECTOR_MODE=disabled
CAT_DOOR_CAMERA_CAPTURE_TIMEOUT_MS=250
CAT_DOOR_PIR_SETTLE_SECONDS=90
```

## 4. What each important setting means

- `CAT_DOOR_TELEGRAM_BOT_TOKEN`: token from BotFather
- `CAT_DOOR_TELEGRAM_CHAT_ID`: your private Telegram chat ID
- `CAT_DOOR_PIR_PIN`: GPIO pin used by the PIR output wire
- `CAT_DOOR_REED_SWITCH_PIN`: GPIO pin used by the reed switch
- `CAT_DOOR_SERVO_PIN`: GPIO pin used for the servo signal
- `CAT_DOOR_ENABLE_GPIO_HARDWARE`: set this to `true` when the hardware is attached
- `CAT_DOOR_ENABLE_SERVO_HARDWARE`: set this to `false` if the servo is not attached yet
- `CAT_DOOR_CAMERA_CAPTURE_TIMEOUT_MS`: how quickly the snapshot is taken after trigger
- `CAT_DOOR_PIR_SETTLE_SECONDS`: how long the PIR gets to settle before arming

## 5. Test in this order

Run these one by one from inside `software/`:

```bash
./run_cat_door.sh status
./run_cat_door.sh text-test
./run_cat_door.sh approval-test
./run_cat_door.sh photo-test
./run_cat_door.sh monitor-once
```

What they do:

- `status` checks whether the camera, PIR, reed switch, and servo backends are available
- `text-test` checks Telegram text delivery
- `approval-test` checks the Telegram approval buttons
- `photo-test` captures and sends one photo immediately
- `monitor-once` waits for one PIR event and runs the full workflow once

## 6. Before the servo or reed switch is attached

If you are only testing the camera and PIR first, keep this in `.env`:

```env
CAT_DOOR_ENABLE_SERVO_HARDWARE=false
```

That lets the system run without trying to move the door.

## 7. Start continuous monitoring only after single tests pass

```bash
./run_cat_door.sh monitor-loop
```

## 8. Install the boot service only after everything is stable

```bash
./install_cat_door_service.sh
```

Then check it with:

```bash
sudo systemctl status cat-door-monitor.service --no-pager
```

That service is the final always-on mode. Do not enable it until the single-run
checks above are working properly.

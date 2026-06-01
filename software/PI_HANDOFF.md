# Raspberry Pi Handoff

## Purpose

This document is for the teammate performing the first Raspberry Pi hardware
deployment of the cat door software.

## Delivered software scope

The delivered software already supports:

- Telegram bot messaging
- Telegram approval buttons
- PIR-triggered event handling
- camera-to-Telegram event flow
- servo-control abstraction
- reed-switch state reporting

The first deployment mode is manual approval:

1. Motion is detected by the PIR sensor
2. The Raspberry Pi captures a photo
3. Telegram sends the photo to the operator
4. The operator approves or rejects the event
5. The door opens only when approved

## Files to use

Work inside the `software/` directory.

Primary documents:

- `README.md`
- `HOOKUP_AND_RUN.md`
- `TELEGRAM_SETUP.md`
- `SOFTWARE_STATUS_REPORT.md`

Primary runtime command:

```bash
./run_cat_door.sh <mode>
```

## Raspberry Pi setup steps

1. Copy or pull the project onto the Raspberry Pi
2. Open a terminal in `software/`
3. Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

4. Populate `.env` with:

```env
CAT_DOOR_TELEGRAM_BOT_TOKEN=
CAT_DOOR_TELEGRAM_CHAT_ID=
CAT_DOOR_PIR_PIN=17
CAT_DOOR_REED_SWITCH_PIN=27
CAT_DOOR_SERVO_PIN=18
CAT_DOOR_ENABLE_GPIO_HARDWARE=true
CAT_DOOR_ENABLE_SERVO_HARDWARE=true
CAT_DOOR_NOTIFY_ON_ANY_MOTION=true
CAT_DOOR_DETECTOR_MODE=disabled
```

## Hardware checklist

- Pi camera connected and enabled
- PIR sensor wired to the configured GPIO pin
- reed switch wired to the configured GPIO pin
- servo signal wired to the configured GPIO pin
- common ground shared between Pi and servo power
- separate safe power source used for the servo

## Validation order

Run these commands in order:

```bash
./run_cat_door.sh status
./run_cat_door.sh text-test
./run_cat_door.sh approval-test
./run_cat_door.sh photo-test
./run_cat_door.sh monitor-once
```

Move to continuous monitoring only after the single-event test is stable:

```bash
./run_cat_door.sh monitor-loop
```

## Expected outcomes

- `status`: confirms runtime backend availability
- `text-test`: confirms Telegram delivery
- `approval-test`: confirms Telegram callback handling
- `photo-test`: confirms Pi camera capture and photo delivery
- `monitor-once`: confirms one full PIR-to-Telegram-to-door workflow

## Detector configuration

Initial deployment keeps the detector disabled. The operator makes the decision
from Telegram during first live testing.

When command-mode detection is enabled, the detector command must emit JSON in
this format:

```json
{
  "is_cat_likely": true,
  "confidence": 0.93,
  "reason": "cat detected near flap"
}
```

## Escalation points

Raise a project decision before changing any of these:

- actuator type
- GPIO pin allocation
- automatic detection policy
- known-cat identification approach

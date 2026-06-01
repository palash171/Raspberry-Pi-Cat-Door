# Software Plan

## Scope

This software is responsible for the cat door control flow from detection to
human approval to actuator control.

## My Ownership

This software section covers:

- Raspberry Pi application structure
- Camera capture flow
- Telegram bot integration
- Pretrained cat detection integration
- Sensor polling and event handling
- Door open and close control logic
- Safety checks and logging

This software section does not assume ownership of:

- final mechanical design
- final enclosure design
- electrical power delivery design
- motor driver circuit design

## System Goal

When motion happens near the flap, the Raspberry Pi should capture an image,
decide whether a cat may be present, notify the user on Telegram, and only
open the door when an allowed command is received.

## Recommended Technical Approach

### Language

Use `Python` as the main application language.

Reason:

- Raspberry Pi camera tooling is easy to call from Python
- GPIO libraries are simplest in Python
- Telegram Bot API integration is straightforward in Python
- pretrained detection examples on Raspberry Pi are commonly Python-first

### Runtime model

Use one main Python application that coordinates:

- camera capture
- detection
- Telegram messaging
- GPIO input and output
- logging and safety decisions

### Detection strategy

Use a pretrained detector rather than training a model from scratch.

Planned progression:

1. trigger on any motion
2. send captured image to Telegram
3. add pretrained cat detection
4. optionally filter alerts based on detector confidence

### Messaging strategy

Use a Telegram bot with inline buttons:

- `Open Door`
- `Keep Closed`

For the first working version, the Pi can use polling rather than webhooks so
there is no need for a public server.

### Safety strategy

Default behavior must always be:

- keep the door closed on failure
- do not open the door if the actuator state is unclear
- alert if the door does not close in time

## Delivery Phases

### Phase 1: Foundation

- create software structure
- define configuration format
- set up Git hygiene
- document responsibilities and milestones

### Phase 2: Telegram photo proof

- capture a snapshot from the Pi camera
- send the snapshot to Telegram
- verify the bot can message the owner successfully

### Phase 3: Telegram control proof

- add inline buttons for `Open Door` and `Keep Closed`
- receive button presses on the Pi
- log the selected action

### Phase 4: Sensor trigger proof

- read PIR input
- trigger camera capture on motion
- avoid duplicate spam with a cooldown

### Phase 5: Detection proof

- integrate pretrained cat detection
- record detector result and confidence
- decide whether to notify on all motion or cat-like motion only

### Phase 6: Door control proof

- connect actuator control logic
- open for a safe interval
- confirm closed state with reed switch

### Phase 7: Reliability

- add structured logging
- add retry handling
- add boot-time service setup
- document deployment on the Raspberry Pi

## Architecture Outline

### `config.py`

Loads runtime configuration such as GPIO pins, Telegram token, chat ID, timing
values, and detector settings.

### `camera.py`

Captures a still image from the Pi camera and returns the output path.

### `detector.py`

Provides one interface for determining whether a likely cat is present.

### `telegram_bot.py`

Sends alerts, photos, and action buttons. Reads updates from Telegram and
returns user commands.

### `sensors.py`

Reads PIR state and reed switch state.

### `door_controller.py`

Holds actuator logic and door safety checks.

### `workflow.py`

Coordinates the end-to-end event flow.

### `main.py`

Starts the application and initializes dependencies.

## First Coding Milestone

The first real coding target is:

`python app captures a photo and sends it to Telegram`

That is the smallest meaningful slice because it proves camera access, network
access, bot setup, and the user-facing notification path.

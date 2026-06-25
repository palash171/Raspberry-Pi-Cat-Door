# Raspberry Pi Cat Door

This repository contains the software for a Raspberry Pi cat door prototype.
The current system watches for motion with a PIR sensor, captures an image with
an attached camera, and sends that image to Telegram for manual approval. The
door only opens if the user approves the event in Telegram.

The goal of this version is reliability first. Instead of trying to fully
automate the decision, the software is set up so the user can check the photo
before opening the flap. Support for a servo, a reed switch, and optional image
classification is already built into the codebase, but those parts still need
final live hardware validation.

## What is working now

- Telegram bot setup and chat ID discovery
- Telegram text and approval-button tests
- Raspberry Pi camera capture through `rpicam-still`
- PIR-triggered monitoring flow
- Configurable GPIO setup through `.env`
- Service install script for running the monitor automatically on boot

## What still needs final hardware validation

- Servo open and close behaviour on the final door hardware
- Reed switch confirmation that the flap returned to the closed position
- Optional cat-detection model if manual approval is later replaced

## Repository layout

- `software/` - main Raspberry Pi application
- `software/cat_door/` - Python source code
- `software/tests/` - test files
- `software/HOOKUP_AND_RUN.md` - step-by-step Pi setup and test order
- `software/TELEGRAM_SETUP.md` - Telegram bot setup guide

## Normal setup flow

1. Clone the repository onto the Raspberry Pi.
2. Open a terminal in `software/`.
3. Run `./setup_pi.sh`.
4. Fill in the local `.env` file.
5. Run the checks from `software/HOOKUP_AND_RUN.md`.

## Important note about configuration

The `.env` file is not stored in Git. That is intentional because it contains
private values such as the Telegram bot token and local GPIO settings.

For a normal deployment, the main file that needs to be edited is `.env`.
Most people using this project should not need to change the Python code unless
they are changing hardware behaviour or adding a detector.

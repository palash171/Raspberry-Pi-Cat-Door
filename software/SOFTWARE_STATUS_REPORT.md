# Software Status Report

## Project area

Smart cat door software for Raspberry Pi, Telegram approval, and door-control
workflow.

## Completed work

- Software package structure created
- Local Python environment and wrapper-based run workflow created
- Telegram bot connectivity implemented and validated
- Telegram approval-button flow implemented and validated
- Runtime configuration via `.env` implemented
- Camera workflow integrated through `rpicam-still`
- PIR, reed-switch, and servo software abstractions implemented
- End-to-end event workflow implemented in software
- Manual-approval deployment mode prepared for first live hardware test

## Completed local validation

- Chat ID discovery
- Telegram text delivery
- Telegram approval-button callback handling
- Wrapper-script execution
- Non-Pi fallback behavior for GPIO-backed components

## Remaining work

- Raspberry Pi camera capture validation
- PIR hardware validation
- Servo open/close validation
- Reed-switch validation
- Final detector decision for production use

## Current deployment recommendation

Use the manual-approval workflow for first hardware deployment:

- detector disabled
- notify on any motion
- operator approves door opening in Telegram

## Current blocker

The remaining validation work depends on access to the Raspberry Pi hardware
platform and connected components.

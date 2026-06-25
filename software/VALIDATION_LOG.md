# Validation Log

## 2026-06-01

### Environment

- Local development machine
- `software/` project directory
- Python virtual environment at `.venv`

### Validation summary

- Verified Python virtual environment creation
- Verified dependency installation from `requirements.txt`
- Verified configuration loading from `.env`
- Verified inbound Telegram update retrieval with `debug-updates`
- Verified private chat ID discovery with `show-chat-id`
- Verified outbound Telegram text delivery with `text-test`
- Verified Telegram inline approval flow with `approval-test`
- Verified both approval actions: `Open Door` and `Keep Closed`

## 2026-06-02

### Environment

- Local development machine
- Wrapper-based execution through `./run_cat_door.sh`

### Validation summary

- Verified `status` command execution through the wrapper script
- Verified expected non-Pi fallback behavior for GPIO-backed components
- Re-verified Telegram text delivery with `text-test`
- Re-verified Telegram approval-button flow with `approval-test`

### Notes

- Local Mac validation confirms software behavior but not GPIO hardware access
- Camera capture, PIR events, servo movement, and reed-switch validation remain
  Raspberry Pi tasks

## 2026-06-03

### Environment

- Raspberry Pi 5
- Raspberry Pi OS
- Python 3.11.2
- `rpicam-still` available on the host

### Validation summary

- Verified project transfer and execution on Raspberry Pi 5
- Verified dependency installation in a Pi-hosted virtual environment
- Verified wrapper-script execution with the Pi 5 runtime
- Verified Telegram text delivery with `text-test`
- Verified Telegram approval-button callback handling with `approval-test`

### Notes

- Camera, PIR, reed switch, and servo were not attached during this validation
- GPIO warnings were observed before adding explicit Pi pin-factory support and
  Linux GPIO dependencies to the project setup

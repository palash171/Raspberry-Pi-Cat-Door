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

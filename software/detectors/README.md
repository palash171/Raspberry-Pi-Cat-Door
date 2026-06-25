# Detector Integration

The main software can optionally call an external detector command after each
captured image.

## Command contract

When `CAT_DOOR_DETECTOR_MODE=command`, the configured command must write JSON
to standard output in this format:

```json
{
  "is_cat_likely": true,
  "confidence": 0.93,
  "reason": "cat detected near flap"
}
```

If `is_cat_likely` is omitted, the main app falls back to the configured
confidence threshold.

## Template command

This folder includes `template_detector.py` as a minimal placeholder detector.
It is not a real model. It only proves the JSON interface works.

Example `.env` values for command-mode testing:

```env
CAT_DOOR_DETECTOR_MODE=command
CAT_DOOR_DETECTOR_COMMAND=.venv/bin/python detectors/template_detector.py {image_path}
```

## Recommended live architecture

The intended production flow is:

1. PIR sensor triggers the event
2. Camera captures an image
3. Detector command classifies the image
4. Telegram sends the image and detector result
5. Operator approves or rejects the event

The PIR sensor should be treated as the wake-up trigger, not the final cat
classifier. The image detector is the right place to distinguish a cat from a
human or other motion.

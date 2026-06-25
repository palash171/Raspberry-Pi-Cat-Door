# Detector Integration

The current project works without a detector. The main live workflow is manual
approval through Telegram.

This folder is only for the next step, where an image-based detector may be
added later to help decide whether a captured image is likely to contain a cat.

## Current behaviour

- PIR triggers the event
- the camera captures a photo
- Telegram sends the photo to the user
- the user chooses whether to open the door

## Optional command interface

If `CAT_DOOR_DETECTOR_MODE=command`, the app will run an external command after
capturing an image.

That command must print JSON like this:

```json
{
  "is_cat_likely": true,
  "confidence": 0.93,
  "reason": "cat detected near flap"
}
```

## Included template

`template_detector.py` is only a placeholder example. It is not a real model.
It just shows the JSON format expected by the main application.

Example `.env` value:

```env
CAT_DOOR_DETECTOR_MODE=command
CAT_DOOR_DETECTOR_COMMAND=.venv/bin/python detectors/template_detector.py {image_path}
```

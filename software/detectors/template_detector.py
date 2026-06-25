#!/usr/bin/env python3
"""Minimal detector command template for the cat door project."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: template_detector.py <image_path>")

    image_path = Path(sys.argv[1])

    # Replace this placeholder with a real image classifier when a cat model is
    # selected. The main app only needs valid JSON on stdout.
    payload = {
        "is_cat_likely": False,
        "confidence": 0.0,
        "reason": f"Template detector placeholder for {image_path.name}",
    }
    print(json.dumps(payload))


if __name__ == "__main__":
    main()

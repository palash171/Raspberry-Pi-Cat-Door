"""Camera capture helpers."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import subprocess


class Camera:
    """Captures still images using Raspberry Pi camera tools."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture_snapshot(self) -> Path:
        """Capture a still image and return the saved file path."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = self.output_dir / f"snapshot-{timestamp}.jpg"

        # Use the Pi camera CLI first so the early prototype avoids lower-level
        # camera integration until the full workflow is proven.
        subprocess.run(
            [
                "rpicam-still",
                "--nopreview",
                "--timeout",
                "1000",
                "--output",
                str(output_path),
            ],
            check=True,
        )

        return output_path

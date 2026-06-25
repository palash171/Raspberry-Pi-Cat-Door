"""Camera capture helpers."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import subprocess


class Camera:
    """Captures still images using Raspberry Pi camera tools."""

    def __init__(self, output_dir: str, capture_timeout_ms: int = 250) -> None:
        self.output_dir = Path(output_dir)
        self.capture_timeout_ms = max(0, capture_timeout_ms)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture_snapshot(self) -> Path:
        """Capture a still image and return the saved file path."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = self.output_dir / f"snapshot-{timestamp}.jpg"

        command = self._build_camera_command(output_path)
        subprocess.run(command, check=True)

        return output_path

    def _build_camera_command(self, output_path: Path) -> list[str]:
        """Choose the first supported Pi camera CLI on the current machine."""
        if shutil.which("rpicam-still"):
            return [
                "rpicam-still",
                "--nopreview",
                "--timeout",
                str(self.capture_timeout_ms),
                "--output",
                str(output_path),
            ]

        if shutil.which("libcamera-still"):
            return [
                "libcamera-still",
                "--nopreview",
                "--timeout",
                str(self.capture_timeout_ms),
                "--output",
                str(output_path),
            ]

        if shutil.which("raspistill"):
            return [
                "raspistill",
                "-n",
                "-t",
                str(self.capture_timeout_ms),
                "-o",
                str(output_path),
            ]

        raise RuntimeError(
            "No Raspberry Pi still-image command was found. Expected one of "
            "rpicam-still, libcamera-still, or raspistill."
        )

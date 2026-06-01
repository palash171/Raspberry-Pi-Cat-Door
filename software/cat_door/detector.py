"""Detection interfaces for deciding whether a cat is present."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import shlex
import subprocess


@dataclass(frozen=True)
class DetectionResult:
    """Structured detector output passed into the notification workflow."""

    is_cat_likely: bool
    confidence: float
    reason: str


class Detector:
    """Detector adapter that can stay disabled or call an external command."""

    def __init__(
        self,
        mode: str,
        command: str,
        confidence_threshold: float,
        timeout_seconds: int,
    ) -> None:
        self.mode = mode.strip().lower()
        self.command = command.strip()
        self.confidence_threshold = confidence_threshold
        self.timeout_seconds = timeout_seconds

    def describe(self) -> str:
        if self.mode == "disabled":
            return "Detector disabled; notifications can still use manual approval."
        if self.mode == "always-cat":
            return "Detector in always-cat test mode."
        if self.mode == "command":
            return "Detector command integration enabled."
        return f"Detector mode '{self.mode}' is unknown."

    def detect_cat(self, image_path: Path) -> DetectionResult:
        """Return a cat-likelihood result for the captured image."""
        if self.mode == "disabled":
            return DetectionResult(
                is_cat_likely=False,
                confidence=0.0,
                reason=f"Detector disabled for {image_path.name}",
            )

        if self.mode == "always-cat":
            return DetectionResult(
                is_cat_likely=True,
                confidence=1.0,
                reason="Detector test mode marked this event as cat-likely.",
            )

        if self.mode == "command":
            return self._detect_with_command(image_path)

        return DetectionResult(
            is_cat_likely=False,
            confidence=0.0,
            reason=f"Unknown detector mode '{self.mode}'",
        )

    def _detect_with_command(self, image_path: Path) -> DetectionResult:
        """Run an external detector command and parse JSON from stdout."""
        if not self.command:
            return DetectionResult(
                is_cat_likely=False,
                confidence=0.0,
                reason="Detector command mode is enabled but no command was configured.",
            )

        # The detector command can either include a {image_path} placeholder or
        # rely on the image path being appended as the last argument.
        if "{image_path}" in self.command:
            command_args = shlex.split(
                self.command.format(image_path=str(image_path))
            )
        else:
            command_args = shlex.split(self.command)
            command_args.append(str(image_path))

        try:
            completed = subprocess.run(
                command_args,
                capture_output=True,
                check=False,
                text=True,
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return DetectionResult(
                is_cat_likely=False,
                confidence=0.0,
                reason="Detector command timed out.",
            )
        except OSError as exc:
            return DetectionResult(
                is_cat_likely=False,
                confidence=0.0,
                reason=f"Detector command failed to start: {exc}",
            )

        if completed.returncode != 0:
            stderr = completed.stderr.strip() or "no stderr output"
            return DetectionResult(
                is_cat_likely=False,
                confidence=0.0,
                reason=f"Detector command failed: {stderr}",
            )

        try:
            payload = json.loads(completed.stdout.strip() or "{}")
        except json.JSONDecodeError:
            return DetectionResult(
                is_cat_likely=False,
                confidence=0.0,
                reason="Detector command did not return valid JSON.",
            )

        confidence = float(payload.get("confidence", 0.0))
        is_cat_likely = bool(
            payload.get(
                "is_cat_likely",
                confidence >= self.confidence_threshold,
            )
        )
        reason = str(
            payload.get("reason")
            or payload.get("label")
            or "Detector command completed successfully."
        )

        return DetectionResult(
            is_cat_likely=is_cat_likely,
            confidence=confidence,
            reason=reason,
        )

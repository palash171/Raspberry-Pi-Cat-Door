"""Door actuator logic."""

from __future__ import annotations

import time

try:
    from gpiozero import Servo
except Exception:  # pragma: no cover - depends on host hardware support
    Servo = None


class DoorController:
    """Controls how the cat door opens and closes."""

    def __init__(
        self,
        servo_pin: int,
        open_duration_seconds: int,
        enable_hardware: bool,
        open_value: float,
        closed_value: float,
    ) -> None:
        self.servo_pin = servo_pin
        self.open_duration_seconds = open_duration_seconds
        self.enable_hardware = enable_hardware
        self.open_value = open_value
        self.closed_value = closed_value
        self._servo = None
        self._backend_error: str | None = None

        if not enable_hardware:
            self._backend_error = "Servo hardware access disabled by configuration."
            return

        if Servo is None:
            self._backend_error = "gpiozero Servo backend is unavailable."
            return

        try:
            self._servo = Servo(servo_pin)
            self.close()
        except Exception as exc:  # pragma: no cover - depends on host hardware
            self._backend_error = str(exc)

    def is_available(self) -> bool:
        return self._servo is not None

    def describe(self) -> str:
        if self.is_available():
            return f"Servo controller on GPIO {self.servo_pin}"
        return f"Servo controller in simulation mode: {self._backend_error}"

    def close(self) -> None:
        if self._servo:
            self._servo.value = self.closed_value

    def open_temporarily(self) -> None:
        """Open the flap for a fixed interval, then close it again."""
        if self._servo:
            self._servo.value = self.open_value
            time.sleep(self.open_duration_seconds)
            self._servo.value = self.closed_value
            return

        # The simulation path keeps local development usable before hardware is
        # wired up. The same workflow can then drive the real servo on the Pi.
        print(
            f"[door] Simulating open on servo pin {self.servo_pin} for "
            f"{self.open_duration_seconds} seconds"
        )
        time.sleep(self.open_duration_seconds)
        print("[door] Simulating close")

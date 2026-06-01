"""Telegram messaging support."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import time
from typing import Any

import requests


@dataclass(frozen=True)
class CallbackResult:
    """Represents a callback button selection returned by Telegram."""

    action: str
    callback_query_id: str
    chat_id: str
    message_id: int | None
    update_id: int


class TelegramBot:
    """Small wrapper around the Telegram Bot API."""

    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def has_token(self) -> bool:
        return bool(self.token)

    def has_chat_target(self) -> bool:
        return bool(self.chat_id)

    def _require_token(self) -> None:
        if not self.has_token():
            raise RuntimeError("Telegram bot token is missing.")

    def _require_chat_target(self) -> None:
        if not self.has_chat_target():
            raise RuntimeError("Telegram chat ID is missing.")

    def _parse_result(self, response: requests.Response) -> dict[str, Any] | list[Any]:
        """Validate a Telegram API response and return its result payload."""
        response.raise_for_status()
        payload = response.json()

        if not payload.get("ok", False):
            description = payload.get("description", "Unknown Telegram API error.")
            raise RuntimeError(f"Telegram API request failed: {description}")

        return payload.get("result", {})

    @staticmethod
    def build_approval_keyboard() -> dict[str, Any]:
        """Build the standard inline keyboard used for door approval."""
        return {
            "inline_keyboard": [
                [{"text": "Open Door", "callback_data": "OPEN_DOOR"}],
                [{"text": "Keep Closed", "callback_data": "KEEP_CLOSED"}],
            ]
        }

    def send_message(
        self,
        text: str,
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a text message, optionally with inline buttons."""
        self._require_token()
        self._require_chat_target()

        payload: dict[str, Any] = {"chat_id": self.chat_id, "text": text}
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup

        response = requests.post(
            f"{self.base_url}/sendMessage",
            json=payload,
            timeout=30,
        )
        result = self._parse_result(response)
        return result if isinstance(result, dict) else {}

    def send_photo(
        self,
        image_path: Path,
        caption: str,
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a photo message, optionally with inline buttons."""
        self._require_token()
        self._require_chat_target()

        data: dict[str, Any] = {"chat_id": self.chat_id, "caption": caption}
        if reply_markup is not None:
            # Multipart requests require reply markup to be JSON serialized.
            data["reply_markup"] = json.dumps(reply_markup)

        with image_path.open("rb") as image_file:
            response = requests.post(
                f"{self.base_url}/sendPhoto",
                data=data,
                files={"photo": image_file},
                timeout=60,
            )
        result = self._parse_result(response)
        return result if isinstance(result, dict) else {}

    def send_approval_request(self, prompt_text: str) -> dict[str, Any]:
        """Send the initial approval request with inline action buttons."""
        return self.send_message(
            prompt_text,
            reply_markup=self.build_approval_keyboard(),
        )

    def send_photo_approval_request(
        self,
        image_path: Path,
        caption: str,
    ) -> dict[str, Any]:
        """Send a photo and attach the standard approval buttons."""
        return self.send_photo(
            image_path,
            caption,
            reply_markup=self.build_approval_keyboard(),
        )

    def get_updates(
        self,
        limit: int = 10,
        offset: int | None = None,
        allowed_updates: list[str] | None = None,
        timeout: int = 0,
    ) -> list[dict[str, Any]]:
        """Fetch recent bot updates from Telegram."""
        self._require_token()

        params: dict[str, Any] = {"limit": limit, "timeout": timeout}
        if offset is not None:
            params["offset"] = offset
        if allowed_updates is not None:
            params["allowed_updates"] = json.dumps(allowed_updates)

        response = requests.get(
            f"{self.base_url}/getUpdates",
            params=params,
            timeout=max(timeout + 5, 30),
        )
        result = self._parse_result(response)
        return result if isinstance(result, list) else []

    def get_latest_chat_id(self) -> str | None:
        """Return the most recent chat ID seen in standard message updates."""
        updates = self.get_updates()

        for update in reversed(updates):
            message = update.get("message") or update.get("edited_message")
            if not message:
                continue

            chat = message.get("chat", {})
            chat_id = chat.get("id")
            if chat_id is not None:
                return str(chat_id)

        return None

    def get_highest_update_id(self) -> int | None:
        """Return the highest update ID seen so far, if any updates exist."""
        updates = self.get_updates(limit=100)
        if not updates:
            return None
        return max(int(update["update_id"]) for update in updates)

    def answer_callback_query(self, callback_query_id: str, text: str) -> None:
        """Acknowledge a pressed button so Telegram clears its loading state."""
        self._require_token()

        response = requests.post(
            f"{self.base_url}/answerCallbackQuery",
            json={"callback_query_id": callback_query_id, "text": text},
            timeout=30,
        )
        self._parse_result(response)

    def clear_inline_keyboard(self, chat_id: str, message_id: int) -> None:
        """Remove inline buttons from a message after a selection is made."""
        self._require_token()

        response = requests.post(
            f"{self.base_url}/editMessageReplyMarkup",
            json={
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": {"inline_keyboard": []},
            },
            timeout=30,
        )
        self._parse_result(response)

    def wait_for_callback(
        self,
        expected_actions: set[str],
        after_update_id: int | None,
        timeout_seconds: int,
    ) -> CallbackResult | None:
        """Poll Telegram until one of the expected callback actions arrives."""
        self._require_token()
        deadline = time.monotonic() + timeout_seconds
        next_offset = None if after_update_id is None else after_update_id + 1

        while time.monotonic() < deadline:
            remaining_seconds = max(1, int(deadline - time.monotonic()))
            updates = self.get_updates(
                offset=next_offset,
                allowed_updates=["callback_query"],
                timeout=min(10, remaining_seconds),
            )

            for update in updates:
                next_offset = int(update["update_id"]) + 1
                callback_query = update.get("callback_query")
                if not callback_query:
                    continue

                data = str(callback_query.get("data", ""))
                message = callback_query.get("message", {})
                chat = message.get("chat", {})
                chat_id = str(chat.get("id", ""))

                if self.chat_id and chat_id != self.chat_id:
                    continue
                if data not in expected_actions:
                    continue

                return CallbackResult(
                    action=data,
                    callback_query_id=str(callback_query["id"]),
                    chat_id=chat_id,
                    message_id=message.get("message_id"),
                    update_id=int(update["update_id"]),
                )

        return None

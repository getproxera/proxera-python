"""Proxera configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class ProxeraConfig:
    """Configuration for the Proxera proxy.

    Args:
        api_key: Your Proxera API key (``px-live_...`` or ``px-test_...``).
            Falls back to the ``PROXERA_API_KEY`` environment variable.
        base_url: Base URL of the Proxera API.
            Falls back to ``PROXERA_BASE_URL``, defaulting to
            ``https://api.getproxera.com/v1``.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retries on transient errors.
        tags: Optional list of tags sent via the ``X-Proxera-Tags`` header.
        team: Optional team identifier sent via the ``X-Proxera-Team`` header.
        provider: Optional provider hint sent via the ``X-Proxera-Provider`` header.
    """

    api_key: str = ""
    base_url: str = ""
    timeout: float = 600.0
    max_retries: int = 2
    tags: list[str] | None = None
    team: str | None = None
    provider: str | None = None

    def __post_init__(self) -> None:
        if not self.api_key:
            self.api_key = os.environ.get("PROXERA_API_KEY", "")
        if not self.base_url:
            self.base_url = os.environ.get(
                "PROXERA_BASE_URL", "https://api.getproxera.com/v1"
            )
        if not self.api_key:
            raise ValueError(
                "A Proxera API key is required. Pass api_key= or set PROXERA_API_KEY."
            )
        if not self.api_key.startswith("px-"):
            raise ValueError(
                f"Invalid Proxera API key: must start with 'px-', got '{self.api_key[:8]}...'."
            )

    def build_headers(self) -> dict[str, str]:
        """Return extra headers to attach to every request."""
        headers: dict[str, str] = {}
        if self.tags:
            headers["X-Proxera-Tags"] = ",".join(self.tags)
        if self.team:
            headers["X-Proxera-Team"] = self.team
        if self.provider:
            headers["X-Proxera-Provider"] = self.provider
        return headers

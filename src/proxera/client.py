"""Proxera client factories and wrapper classes.

Usage::

    import proxera

    # Simple factory — returns a standard openai.OpenAI client
    client = proxera.get_client()
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}],
    )

    # Wrapper class — same interface, holds config
    client = proxera.Client(tags=["experiment-1"], team="research")
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}],
    )
"""

from __future__ import annotations

from typing import Any

import openai

from .config import ProxeraConfig


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------


def get_client(
    proxera_key: str | None = None,
    base_url: str | None = None,
    *,
    tags: list[str] | None = None,
    team: str | None = None,
    provider: str | None = None,
    **kwargs: Any,
) -> openai.OpenAI:
    """Create an :class:`openai.OpenAI` client that routes through Proxera.

    Args:
        proxera_key: Proxera API key.  Defaults to ``PROXERA_API_KEY`` env var.
        base_url: Proxera base URL.  Defaults to ``PROXERA_BASE_URL`` env var
            or ``https://api.proxera.dev/v1``.
        tags: Optional tags attached via ``X-Proxera-Tags``.
        team: Optional team identifier via ``X-Proxera-Team``.
        provider: Optional provider hint via ``X-Proxera-Provider``.
        **kwargs: Extra keyword arguments forwarded to :class:`openai.OpenAI`.

    Returns:
        A configured :class:`openai.OpenAI` instance.

    Example::

        client = get_client()
        client.chat.completions.create(model="gpt-4o", messages=[...])
    """
    config = ProxeraConfig(
        api_key=proxera_key or "",
        base_url=base_url or "",
        tags=tags,
        team=team,
        provider=provider,
    )
    headers = config.build_headers()
    if "default_headers" in kwargs:
        headers = {**headers, **kwargs.pop("default_headers")}
    return openai.OpenAI(
        api_key=config.api_key,
        base_url=config.base_url,
        timeout=kwargs.pop("timeout", config.timeout),
        max_retries=kwargs.pop("max_retries", config.max_retries),
        default_headers=headers or None,
        **kwargs,
    )


def get_async_client(
    proxera_key: str | None = None,
    base_url: str | None = None,
    *,
    tags: list[str] | None = None,
    team: str | None = None,
    provider: str | None = None,
    **kwargs: Any,
) -> openai.AsyncOpenAI:
    """Create an :class:`openai.AsyncOpenAI` client that routes through Proxera.

    Same parameters as :func:`get_client` but returns an async client.

    Example::

        client = get_async_client()
        resp = await client.chat.completions.create(model="gpt-4o", messages=[...])
    """
    config = ProxeraConfig(
        api_key=proxera_key or "",
        base_url=base_url or "",
        tags=tags,
        team=team,
        provider=provider,
    )
    headers = config.build_headers()
    if "default_headers" in kwargs:
        headers = {**headers, **kwargs.pop("default_headers")}
    return openai.AsyncOpenAI(
        api_key=config.api_key,
        base_url=config.base_url,
        timeout=kwargs.pop("timeout", config.timeout),
        max_retries=kwargs.pop("max_retries", config.max_retries),
        default_headers=headers or None,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Wrapper classes
# ---------------------------------------------------------------------------


class Client:
    """Thin wrapper around :class:`openai.OpenAI` pre-configured for Proxera.

    All attribute access is delegated to the underlying OpenAI client, so you
    can use ``client.chat.completions.create(...)`` exactly as you would with
    the OpenAI SDK.

    Args:
        proxera_key: Proxera API key.
        base_url: Proxera base URL.
        tags: Optional request tags.
        team: Optional team identifier.
        provider: Optional provider hint.
        **kwargs: Forwarded to :class:`openai.OpenAI`.

    Example::

        client = Client(tags=["my-app"])
        client.chat.completions.create(model="gpt-4o", messages=[...])
    """

    def __init__(
        self,
        proxera_key: str | None = None,
        base_url: str | None = None,
        *,
        tags: list[str] | None = None,
        team: str | None = None,
        provider: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.config = ProxeraConfig(
            api_key=proxera_key or "",
            base_url=base_url or "",
            tags=tags,
            team=team,
            provider=provider,
        )
        headers = self.config.build_headers()
        if "default_headers" in kwargs:
            headers = {**headers, **kwargs.pop("default_headers")}
        self._client = openai.OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=kwargs.pop("timeout", self.config.timeout),
            max_retries=kwargs.pop("max_retries", self.config.max_retries),
            default_headers=headers or None,
            **kwargs,
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self._client, name)


class AsyncClient:
    """Async version of :class:`Client`.

    Example::

        client = AsyncClient()
        resp = await client.chat.completions.create(model="gpt-4o", messages=[...])
    """

    def __init__(
        self,
        proxera_key: str | None = None,
        base_url: str | None = None,
        *,
        tags: list[str] | None = None,
        team: str | None = None,
        provider: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.config = ProxeraConfig(
            api_key=proxera_key or "",
            base_url=base_url or "",
            tags=tags,
            team=team,
            provider=provider,
        )
        headers = self.config.build_headers()
        if "default_headers" in kwargs:
            headers = {**headers, **kwargs.pop("default_headers")}
        self._client = openai.AsyncOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=kwargs.pop("timeout", self.config.timeout),
            max_retries=kwargs.pop("max_retries", self.config.max_retries),
            default_headers=headers or None,
            **kwargs,
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self._client, name)

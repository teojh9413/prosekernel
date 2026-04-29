from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol


class ProviderAdapter(Protocol):
    provider: str
    model: str

    def generate(self, prompt: str) -> str:
        """Generate a draft from an agent-ready Humanprint prompt."""


class ProviderError(RuntimeError):
    """Base error for provider setup or generation failures."""


class UnknownProviderError(ProviderError):
    pass


class MissingProviderCredential(ProviderError):
    def __init__(self, provider: str, env_var: str):
        self.provider = provider
        self.env_var = env_var
        super().__init__(
            f"Missing credential for provider '{provider}'. Set {env_var} or pass --api-key explicitly. "
            "No API call was made. Use `humanprint brief` for a no-credential dry run."
        )


class ProviderCallError(ProviderError):
    pass


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    env_var: str
    endpoint: str
    api_kind: str


PROVIDER_SPECS: dict[str, ProviderSpec] = {
    "openai": ProviderSpec(
        name="openai",
        env_var="OPENAI_API_KEY",
        endpoint="https://api.openai.com/v1/chat/completions",
        api_kind="openai-compatible",
    ),
    "openrouter": ProviderSpec(
        name="openrouter",
        env_var="OPENROUTER_API_KEY",
        endpoint="https://openrouter.ai/api/v1/chat/completions",
        api_kind="openai-compatible",
    ),
    "anthropic": ProviderSpec(
        name="anthropic",
        env_var="ANTHROPIC_API_KEY",
        endpoint="https://api.anthropic.com/v1/messages",
        api_kind="anthropic",
    ),
}


@dataclass
class HTTPProviderAdapter:
    provider: str
    model: str
    api_key: str
    endpoint: str
    api_kind: str
    timeout: int = 60
    max_tokens: int = 1800

    def generate(self, prompt: str) -> str:
        if self.api_kind == "anthropic":
            return self._generate_anthropic(prompt)
        if self.api_kind == "openai-compatible":
            return self._generate_openai_compatible(prompt)
        raise ProviderCallError(f"Unsupported API kind for provider '{self.provider}': {self.api_kind}")

    def _generate_openai_compatible(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are drafting with Humanprint. Follow the supplied brief exactly and avoid generic AI slop.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": self.max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.provider == "openrouter":
            headers["HTTP-Referer"] = "https://github.com/teojh9413/humanprint"
            headers["X-Title"] = "Humanprint"
        data = _post_json(self.endpoint, payload, headers, timeout=self.timeout)
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderCallError(f"Provider '{self.provider}' returned an unexpected response shape.") from exc

    def _generate_anthropic(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        data = _post_json(self.endpoint, payload, headers, timeout=self.timeout)
        try:
            parts = data["content"]
            return "".join(part.get("text", "") for part in parts).strip()
        except (KeyError, TypeError) as exc:
            raise ProviderCallError(f"Provider '{self.provider}' returned an unexpected response shape.") from exc


def provider_adapter_from_env(provider: str, model: str, *, api_key: str | None = None, timeout: int = 60) -> HTTPProviderAdapter:
    provider_key = provider.strip().lower()
    if provider_key not in PROVIDER_SPECS:
        supported = ", ".join(sorted(PROVIDER_SPECS))
        raise UnknownProviderError(
            f"Unknown provider '{provider}'. Supported providers: {supported}. "
            "No API call was made. Use `humanprint brief` for a no-credential dry run."
        )
    spec = PROVIDER_SPECS[provider_key]
    credential = api_key or os.environ.get(spec.env_var)
    if not credential:
        raise MissingProviderCredential(provider_key, spec.env_var)
    return HTTPProviderAdapter(
        provider=spec.name,
        model=model,
        api_key=credential,
        endpoint=spec.endpoint,
        api_kind=spec.api_kind,
        timeout=timeout,
    )


def _post_json(url: str, payload: dict[str, object], headers: dict[str, str], *, timeout: int) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise ProviderCallError(f"Provider HTTP error {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ProviderCallError(f"Provider connection error: {exc.reason}") from exc
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProviderCallError("Provider returned invalid JSON.") from exc
    if not isinstance(parsed, dict):
        raise ProviderCallError("Provider returned non-object JSON.")
    return parsed

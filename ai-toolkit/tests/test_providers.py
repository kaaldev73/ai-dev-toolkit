import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from providers.base_provider import BaseProvider
from providers.claude_provider import ClaudeProvider
from providers.openrouter_provider import OpenRouterProvider
from providers.provider_factory import ProviderFactory


# ── BaseProvider ──────────────────────────────────────────────────────────────

def test_base_provider_is_abstract():
    """BaseProvider cannot be instantiated directly."""
    try:
        BaseProvider()
        assert False, "Should have raised TypeError"
    except TypeError:
        pass


def test_base_provider_requires_generate():
    """A subclass without generate() cannot be instantiated."""
    class Incomplete(BaseProvider):
        pass
    try:
        Incomplete()
        assert False, "Should have raised TypeError"
    except TypeError:
        pass


def test_base_provider_concrete_subclass():
    """A subclass that implements generate() can be instantiated."""
    class Concrete(BaseProvider):
        def generate(self, prompt, system_prompt=None):
            return "ok"
    obj = Concrete()
    assert obj.generate("hi") == "ok"


# ── ProviderFactory ───────────────────────────────────────────────────────────

def test_factory_unsupported_raises_value_error():
    try:
        ProviderFactory.create("chatgpt")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "chatgpt" in str(e)
        assert "Unsupported provider" in str(e)


def test_factory_unsupported_lists_supported():
    try:
        ProviderFactory.create("unknown")
    except ValueError as e:
        msg = str(e)
        assert "claude" in msg
        assert "openrouter" in msg


def test_factory_empty_string_raises_value_error():
    try:
        ProviderFactory.create("")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ── ClaudeProvider via factory ────────────────────────────────────────────────

def test_factory_creates_claude_provider():
    with patch("providers.claude_provider.anthropic.Anthropic") as mock_anthropic:
        mock_anthropic.return_value = MagicMock()
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            provider = ProviderFactory.create("claude")
    assert isinstance(provider, ClaudeProvider)
    assert isinstance(provider, BaseProvider)


def test_factory_creates_claude_case_insensitive():
    with patch("providers.claude_provider.anthropic.Anthropic") as mock_anthropic:
        mock_anthropic.return_value = MagicMock()
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            provider = ProviderFactory.create("  claude  ")
    assert isinstance(provider, ClaudeProvider)


# ── OpenRouterProvider via factory ────────────────────────────────────────────

def test_factory_creates_openrouter_provider():
    with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
        provider = ProviderFactory.create("openrouter")
    assert isinstance(provider, OpenRouterProvider)
    assert isinstance(provider, BaseProvider)


# ── ClaudeProvider.generate ───────────────────────────────────────────────────

def test_claude_generate_returns_text():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="Claude response")]
    )
    provider = ClaudeProvider.__new__(ClaudeProvider)
    provider._client = mock_client
    provider._model = "claude-sonnet-4-6"

    result = provider.generate("Hello")
    assert result == "Claude response"


def test_claude_generate_with_system_prompt():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="answer")]
    )
    provider = ClaudeProvider.__new__(ClaudeProvider)
    provider._client = mock_client
    provider._model = "claude-sonnet-4-6"

    provider.generate("Hello", system_prompt="Be concise.")
    call_kwargs = mock_client.messages.create.call_args[1]
    assert call_kwargs["system"] == "Be concise."


def test_claude_generate_no_system_prompt_omits_system_key():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="answer")]
    )
    provider = ClaudeProvider.__new__(ClaudeProvider)
    provider._client = mock_client
    provider._model = "claude-sonnet-4-6"

    provider.generate("Hello")
    call_kwargs = mock_client.messages.create.call_args[1]
    assert "system" not in call_kwargs


# ── OpenRouterProvider.generate ───────────────────────────────────────────────

def test_openrouter_generate_returns_text():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "OpenRouter response"}}]
    }
    with patch("providers.openrouter_provider.requests.post", return_value=mock_response):
        provider = OpenRouterProvider.__new__(OpenRouterProvider)
        provider._api_key = "test-key"
        provider._model = "openai/gpt-4o"
        result = provider.generate("Hello")
    assert result == "OpenRouter response"


def test_openrouter_generate_includes_system_prompt():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "ok"}}]
    }
    with patch("providers.openrouter_provider.requests.post", return_value=mock_response) as mock_post:
        provider = OpenRouterProvider.__new__(OpenRouterProvider)
        provider._api_key = "test-key"
        provider._model = "openai/gpt-4o"
        provider.generate("Hello", system_prompt="Be brief.")
    payload = mock_post.call_args[1]["json"]
    roles = [m["role"] for m in payload["messages"]]
    assert roles[0] == "system"
    assert roles[1] == "user"


# ── ClaudeProvider missing API key ───────────────────────────────────────────

def test_claude_missing_api_key_raises_runtime_error():
    with patch("providers.claude_provider.anthropic.Anthropic"):
        with patch.dict("os.environ", {}, clear=True):
            try:
                ClaudeProvider()
                assert False, "Should have raised RuntimeError"
            except RuntimeError as e:
                assert "ANTHROPIC_API_KEY" in str(e)


def test_claude_missing_api_key_message_mentions_env_file():
    with patch("providers.claude_provider.anthropic.Anthropic"):
        with patch.dict("os.environ", {}, clear=True):
            try:
                ClaudeProvider()
            except RuntimeError as e:
                assert ".env" in str(e)


# ── ClaudeProvider empty response ─────────────────────────────────────────────

def test_claude_empty_content_raises_runtime_error():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(content=[])
    provider = ClaudeProvider.__new__(ClaudeProvider)
    provider._client = mock_client
    provider._model = "claude-sonnet-4-6"
    try:
        provider.generate("Hello")
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "empty" in str(e).lower()


def test_claude_empty_response_never_raises_index_error():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(content=[])
    provider = ClaudeProvider.__new__(ClaudeProvider)
    provider._client = mock_client
    provider._model = "claude-sonnet-4-6"
    try:
        provider.generate("Hello")
    except IndexError:
        assert False, "Must not raise IndexError"
    except RuntimeError:
        pass  # expected


# ── OpenRouterProvider missing API key ────────────────────────────────────────

def test_openrouter_missing_api_key_raises_runtime_error():
    with patch.dict("os.environ", {}, clear=True):
        try:
            OpenRouterProvider()
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "OPENROUTER_API_KEY" in str(e)


def test_openrouter_missing_api_key_message_mentions_env_file():
    with patch.dict("os.environ", {}, clear=True):
        try:
            OpenRouterProvider()
        except RuntimeError as e:
            assert ".env" in str(e)


# ── OpenRouterProvider error response ─────────────────────────────────────────

def test_openrouter_error_body_raises_runtime_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"error": {"message": "Rate limit exceeded"}}
    with patch("providers.openrouter_provider.requests.post", return_value=mock_response):
        provider = OpenRouterProvider.__new__(OpenRouterProvider)
        provider._api_key = "test-key"
        provider._model = "m"
        try:
            provider.generate("Hello")
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "Rate limit exceeded" in str(e)


def test_openrouter_error_body_never_raises_key_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"error": {"message": "Bad request"}}
    with patch("providers.openrouter_provider.requests.post", return_value=mock_response):
        provider = OpenRouterProvider.__new__(OpenRouterProvider)
        provider._api_key = "test-key"
        provider._model = "m"
        try:
            provider.generate("Hello")
        except KeyError:
            assert False, "Must not raise KeyError"
        except RuntimeError:
            pass  # expected


def test_openrouter_empty_choices_raises_runtime_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"choices": []}
    with patch("providers.openrouter_provider.requests.post", return_value=mock_response):
        provider = OpenRouterProvider.__new__(OpenRouterProvider)
        provider._api_key = "test-key"
        provider._model = "m"
        try:
            provider.generate("Hello")
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "empty" in str(e).lower()


# ── DEFAULT_PROVIDER in config ────────────────────────────────────────────────

def test_default_provider_config_default():
    import importlib
    import os
    env = os.environ.copy()
    env.pop("AI_PROVIDER", None)
    with patch.dict("os.environ", env, clear=True):
        import config.config as cfg
        importlib.reload(cfg)
        assert cfg.DEFAULT_PROVIDER == "claude"


def test_default_provider_config_override():
    import importlib
    with patch.dict("os.environ", {"AI_PROVIDER": "openrouter"}):
        import config.config as cfg
        importlib.reload(cfg)
        assert cfg.DEFAULT_PROVIDER == "openrouter"


if __name__ == "__main__":
    tests = [
        test_base_provider_is_abstract,
        test_base_provider_requires_generate,
        test_base_provider_concrete_subclass,
        test_factory_unsupported_raises_value_error,
        test_factory_unsupported_lists_supported,
        test_factory_empty_string_raises_value_error,
        test_factory_creates_claude_provider,
        test_factory_creates_claude_case_insensitive,
        test_factory_creates_openrouter_provider,
        test_claude_generate_returns_text,
        test_claude_generate_with_system_prompt,
        test_claude_generate_no_system_prompt_omits_system_key,
        test_claude_missing_api_key_raises_runtime_error,
        test_claude_missing_api_key_message_mentions_env_file,
        test_claude_empty_content_raises_runtime_error,
        test_claude_empty_response_never_raises_index_error,
        test_openrouter_generate_returns_text,
        test_openrouter_generate_includes_system_prompt,
        test_openrouter_missing_api_key_raises_runtime_error,
        test_openrouter_missing_api_key_message_mentions_env_file,
        test_openrouter_error_body_raises_runtime_error,
        test_openrouter_error_body_never_raises_key_error,
        test_openrouter_empty_choices_raises_runtime_error,
        test_default_provider_config_default,
        test_default_provider_config_override,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")

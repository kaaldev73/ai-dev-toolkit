import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services.ai_task_service import AITaskService


def _mock_factory(response_text: str = "result"):
    """Return a patcher that makes ProviderFactory.create() return a mock provider."""
    mock_provider = MagicMock()
    mock_provider.generate.return_value = response_text
    return patch(
        "services.ai_task_service.ProviderFactory.create",
        return_value=mock_provider,
    )


# ── Provider selection ────────────────────────────────────────────────────────

def test_uses_default_provider_from_config():
    with patch("services.ai_task_service.DEFAULT_PROVIDER", "claude"):
        with patch("services.ai_task_service.ProviderFactory.create") as mock_create:
            mock_create.return_value = MagicMock()
            mock_create.return_value.generate.return_value = ""
            AITaskService()
    mock_create.assert_called_once_with("claude")


def test_accepts_explicit_provider_name():
    with patch("services.ai_task_service.ProviderFactory.create") as mock_create:
        mock_create.return_value = MagicMock()
        mock_create.return_value.generate.return_value = ""
        AITaskService(provider_name="openrouter")
    mock_create.assert_called_once_with("openrouter")


def test_explicit_provider_overrides_default():
    with patch("services.ai_task_service.DEFAULT_PROVIDER", "claude"):
        with patch("services.ai_task_service.ProviderFactory.create") as mock_create:
            mock_create.return_value = MagicMock()
            mock_create.return_value.generate.return_value = ""
            AITaskService(provider_name="openrouter")
    mock_create.assert_called_once_with("openrouter")


# ── Successful generation ─────────────────────────────────────────────────────

def test_generate_returns_provider_response():
    with _mock_factory("Hello from AI") as _:
        service = AITaskService()
        result = service.generate("Say hello")
    assert result == "Hello from AI"


def test_generate_passes_prompt_to_provider():
    with patch("services.ai_task_service.ProviderFactory.create") as mock_create:
        mock_provider = MagicMock()
        mock_provider.generate.return_value = "ok"
        mock_create.return_value = mock_provider
        service = AITaskService()
        service.generate("My prompt")
    mock_provider.generate.assert_called_once_with("My prompt", None)


def test_generate_passes_system_prompt_to_provider():
    with patch("services.ai_task_service.ProviderFactory.create") as mock_create:
        mock_provider = MagicMock()
        mock_provider.generate.return_value = "ok"
        mock_create.return_value = mock_provider
        service = AITaskService()
        service.generate("My prompt", system_prompt="Be concise.")
    mock_provider.generate.assert_called_once_with("My prompt", "Be concise.")


def test_generate_without_system_prompt_passes_none():
    with patch("services.ai_task_service.ProviderFactory.create") as mock_create:
        mock_provider = MagicMock()
        mock_provider.generate.return_value = "ok"
        mock_create.return_value = mock_provider
        service = AITaskService()
        service.generate("prompt only")
    _, passed_system = mock_provider.generate.call_args[0]
    assert passed_system is None


# ── Unsupported provider ──────────────────────────────────────────────────────

def test_unsupported_provider_raises_value_error():
    try:
        AITaskService(provider_name="gemini")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "gemini" in str(e)


def test_unsupported_provider_error_message_lists_supported():
    try:
        AITaskService(provider_name="chatgpt")
    except ValueError as e:
        msg = str(e)
        assert "claude" in msg
        assert "openrouter" in msg


# ── Error propagation ─────────────────────────────────────────────────────────

def test_provider_error_propagates():
    with patch("services.ai_task_service.ProviderFactory.create") as mock_create:
        mock_provider = MagicMock()
        mock_provider.generate.side_effect = RuntimeError("API timeout")
        mock_create.return_value = mock_provider
        service = AITaskService()
        try:
            service.generate("test")
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "API timeout" in str(e)


def test_service_does_not_swallow_exceptions():
    with patch("services.ai_task_service.ProviderFactory.create") as mock_create:
        mock_provider = MagicMock()
        mock_provider.generate.side_effect = ConnectionError("no network")
        mock_create.return_value = mock_provider
        service = AITaskService()
        try:
            service.generate("test")
            assert False, "Should have raised ConnectionError"
        except ConnectionError:
            pass


if __name__ == "__main__":
    tests = [
        test_uses_default_provider_from_config,
        test_accepts_explicit_provider_name,
        test_explicit_provider_overrides_default,
        test_generate_returns_provider_response,
        test_generate_passes_prompt_to_provider,
        test_generate_passes_system_prompt_to_provider,
        test_generate_without_system_prompt_passes_none,
        test_unsupported_provider_raises_value_error,
        test_unsupported_provider_error_message_lists_supported,
        test_provider_error_propagates,
        test_service_does_not_swallow_exceptions,
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

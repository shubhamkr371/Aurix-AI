"""
conftest.py
───────────
Pytest fixtures for Aurix AI test suite.

Provides a Flask test client with all heavy AI dependencies mocked out,
so tests run in seconds without needing torch, whisper, or API keys.
"""

import sys
import types
from unittest.mock import MagicMock
from importlib.machinery import ModuleSpec

import pytest


# ── Mock heavy modules BEFORE any app imports ────────────────────────────────
# These modules are imported transitively by core/ and services/ but are
# NOT needed for route-level testing.

_HEAVY_MODULES = [
    # PyTorch / Whisper
    "torch", "torchaudio", "whisper",
    # LangChain ecosystem
    "langchain", "langchain.text_splitter", "langchain.chains",
    "langchain_core", "langchain_core.prompts", "langchain_core.output_parsers",
    "langchain_core.runnables", "langchain_core.documents",
    "langchain_community", "langchain_community.document_loaders",
    "langchain_community.embeddings",
    "langchain_mistralai", "langchain_mistralai.chat_models",
    "langchain_chroma",
    "langchain_huggingface", "langchain_huggingface.embeddings",
    "langchain_text_splitters",
    # Vector DB / Embeddings
    "chromadb", "sentence_transformers",
    # Mistral client
    "mistralai",
    # Audio / Video processing
    "yt_dlp", "pydub", "pydub.AudioSegment",
    "ffmpeg",
    # Translation
    "deep_translator",
    # PDF
    "reportlab", "fpdf2", "fpdf",
    # Misc
    "tiktoken", "huggingface_hub",
]


def _make_mock_module(mod_name):
    """Create a MagicMock that behaves like a proper Python module.

    Python 3.12+ import machinery inspects __spec__ during imports.
    Without it, 'from X import Y' statements raise AttributeError.
    """
    mock_mod = MagicMock()
    # Set essential module attributes
    mock_mod.__name__ = mod_name
    mock_mod.__loader__ = None
    mock_mod.__package__ = mod_name
    mock_mod.__path__ = []
    mock_mod.__file__ = f"<mocked:{mod_name}>"
    mock_mod.__spec__ = ModuleSpec(mod_name, None)
    return mock_mod


def _install_mock_modules():
    """Inject mock modules into sys.modules so imports don't fail."""
    for mod_name in _HEAVY_MODULES:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = _make_mock_module(mod_name)


_install_mock_modules()


@pytest.fixture
def app():
    """Create a Flask application instance for testing."""
    from server import create_app

    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Provide a Flask test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Provide a Flask CLI test runner."""
    return app.test_cli_runner()

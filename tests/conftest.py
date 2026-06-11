"""Shared fixtures for tests."""

import warnings

import pytest
from pathlib import Path
import tempfile
import shutil

# Suppress PIL warning about palette images with transparency (from agent icons)
warnings.filterwarnings("ignore", message="Palette images with Transparency")


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test data."""
    dirpath = tempfile.mkdtemp()
    yield Path(dirpath)
    # Use ignore_errors=True because TantivyIndex may still be flushing
    # data to disk in background threads when teardown runs
    shutil.rmtree(dirpath, ignore_errors=True)


@pytest.fixture(autouse=True)
def isolate_settings():
    """Keep tests independent of the user's real settings file.

    Tests that need specific settings patch load_settings themselves; their
    inner patch takes precedence over this one.
    """
    from unittest.mock import patch

    from fast_resume.settings import DEFAULTS

    with (
        patch("fast_resume.tui.app.load_settings", return_value=dict(DEFAULTS)),
        patch("fast_resume.tui.app.save_settings"),
    ):
        yield

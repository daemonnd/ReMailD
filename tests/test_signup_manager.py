"""
File for testing the hole sign up process
"""
import pytest
import shutil
from pathlib import Path

from . . src.utils.launch_reader import launch_data

@pytest.fixture
def cleanup_recovery():
    yield
    shutil.rmtree(path=str(Path(launch_data.folder / "recovery")), ignore_errors=True)
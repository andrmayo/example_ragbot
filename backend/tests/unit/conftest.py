import os
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

# an invalid key should still allow for client setup, but will
# lead to errors when actual calls get made
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("GOOGLE_API_KEY", "test-key")


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def sample_docx() -> Path:
    return FIXTURES_DIR / "engineering_resume25.docx"


@pytest.fixture
def sample_odt() -> Path:
    return FIXTURES_DIR / "engineering_resume25.odt"


@pytest.fixture
def sample_pdf() -> Path:
    return FIXTURES_DIR / "engineering_resume25.pdf"


@pytest.fixture
def sample_txt() -> Path:
    return FIXTURES_DIR / "engineering_resume25.txt"

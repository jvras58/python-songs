"""Configuração do pytest."""

import pytest
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


@pytest.fixture
def sample_gesture_config():
    """Fixture com configuração de gestos de exemplo."""
    return {
        8: {"sound": "assets/sounds/notes/piano_c4.wav", "name": "C4"},
        12: {"sound": "assets/sounds/notes/piano_d4.wav", "name": "D4"},
    }


@pytest.fixture
def sample_note_to_gesture():
    """Fixture com mapeamento de notas para gestos."""
    return {
        "C4": ("Left", 8),
        "D4": ("Left", 12),
        "E4": ("Right", 8),
    }

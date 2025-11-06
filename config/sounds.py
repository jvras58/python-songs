"""Configurações de áudio."""

# Volume padrão (0.0 a 1.0)
DEFAULT_VOLUME = 0.5

# Caminhos para efeitos sonoros
SOUND_EFFECTS = {
    "success": "assets/sounds/effects/success.wav",
    "fail": "assets/sounds/effects/fail.wav",
}

# Configurações do mixer do pygame
MIXER_CONFIG = {
    "frequency": 44100,
    "size": -16,
    "channels": 2,
    "buffer": 512,
}

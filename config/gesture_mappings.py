"""Mapeamentos de gestos para notas musicais."""

# Configuração de gestos para mão esquerda
# Formato: {finger_landmark_id: {"sound": "path", "name": "note_name"}}
LEFT_HAND_GESTURES = {
    # Indicador + Polegar
    8: {
        "sound": "assets/sounds/notes/piano_c4.wav",
        "name": "C4",
    },
    # Médio + Polegar
    12: {
        "sound": "assets/sounds/notes/piano_d4.wav",
        "name": "D4",
    },
    # Anelar + Polegar
    16: {
        "sound": "assets/sounds/notes/piano_e4.wav",
        "name": "E4",
    },
    # Mindinho + Polegar
    20: {
        "sound": "assets/sounds/notes/piano_f4.wav",
        "name": "F4",
    },
}

# Configuração de gestos para mão direita
RIGHT_HAND_GESTURES = {
    # Indicador + Polegar
    8: {
        "sound": "assets/sounds/notes/piano_e4.wav",
        "name": "E4",
    },
    # Médio + Polegar
    12: {
        "sound": "assets/sounds/notes/piano_f4.wav",
        "name": "F4",
    },
    # Anelar + Polegar
    16: {
        "sound": "assets/sounds/notes/piano_g4.wav",
        "name": "G4",
    },
    # Mindinho + Polegar
    20: {
        "sound": "assets/sounds/notes/piano_cs4(fake).wav",
        "name": "C#4",
    },
}

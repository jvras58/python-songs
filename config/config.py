"""Configuração principal do Gesto Songs."""

from .gesture_mappings import LEFT_HAND_GESTURES, RIGHT_HAND_GESTURES
from .sounds import DEFAULT_VOLUME

CONFIG = {
    "volume": DEFAULT_VOLUME,
    "camera_index": 0,
    "hands_config": {
        "max_num_hands": 2,
        "min_detection_confidence": 0.7,
        "min_tracking_confidence": 0.7,
    },
    "fps": 60,
    "recording_mode": False,
    "playback_mode": False,
    "gesture_touch_threshold": 40,  # Distância em pixels para detectar toque
    "left_hand_gestures": LEFT_HAND_GESTURES,
    "right_hand_gestures": RIGHT_HAND_GESTURES,
}

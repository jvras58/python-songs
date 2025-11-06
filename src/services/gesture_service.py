"""Serviço de detecção de gestos."""

import logging
import time
from typing import Callable, Dict, Set

import numpy as np

logger = logging.getLogger(__name__)


class GestureService:
    """Detecta e processa gestos de toque entre dedos."""

    def __init__(self, touch_threshold: float = 40):
        """
        Inicializa o serviço de detecção de gestos.
        
        Args:
            touch_threshold: Distância em pixels para considerar um toque
        """
        self.touch_threshold = touch_threshold
        self.active_gestures: Dict[int, Set[int]] = {}
        self.active_notes: Dict[str, float] = {}  # {note_name: timestamp}

    def detect_finger_gestures(
        self,
        hand_landmarks,
        hand_idx: int,
        gesture_config: dict,
        w: int,
        h: int,
        on_gesture: Callable[[str, dict], None],
    ) -> Set[int]:
        """
        Detecta gestos de toque entre dedos e polegar.
        
        Args:
            hand_landmarks: Landmarks da mão do MediaPipe
            hand_idx: Índice da mão
            gesture_config: Configuração de gestos para esta mão
            w: Largura do frame
            h: Altura do frame
            on_gesture: Callback chamado quando um gesto é detectado
            
        Returns:
            Conjunto de IDs de dedos atualmente tocando o polegar
        """
        thumb_tip = hand_landmarks.landmark[4]
        thumb_pos = np.array([thumb_tip.x * w, thumb_tip.y * h])

        if hand_idx not in self.active_gestures:
            self.active_gestures[hand_idx] = set()

        current_touches = set()

        for finger_id, gesture_data in gesture_config.items():
            finger_tip = hand_landmarks.landmark[finger_id]
            finger_pos = np.array([finger_tip.x * w, finger_tip.y * h])
            distance = np.linalg.norm(finger_pos - thumb_pos)

            if distance < self.touch_threshold:
                current_touches.add(finger_id)

                # Gesto novo (não estava tocando antes)
                if finger_id not in self.active_gestures[hand_idx]:
                    note_name = gesture_data["name"]
                    self.active_notes[note_name] = time.time()
                    
                    # Chama callback
                    on_gesture(note_name, gesture_data)
                    
                    logger.info(f"Gesture detected: {note_name}")

        self.active_gestures[hand_idx] = current_touches
        return current_touches

    def get_active_gestures(self, hand_idx: int) -> Set[int]:
        """
        Retorna os gestos ativos para uma mão.
        
        Args:
            hand_idx: Índice da mão
            
        Returns:
            Conjunto de IDs de dedos atualmente ativos
        """
        return self.active_gestures.get(hand_idx, set())

    def clear_old_notes(self, max_age: float = 0.5) -> None:
        """
        Remove notas antigas do registro.
        
        Args:
            max_age: Idade máxima em segundos para manter uma nota
        """
        current_time = time.time()
        notes_to_remove = [
            note_name
            for note_name, timestamp in self.active_notes.items()
            if current_time - timestamp > max_age
        ]
        
        for note_name in notes_to_remove:
            del self.active_notes[note_name]

    def reset(self) -> None:
        """Reseta todos os gestos ativos."""
        self.active_gestures.clear()
        self.active_notes.clear()

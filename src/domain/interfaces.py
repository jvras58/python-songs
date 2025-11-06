"""Interfaces e protocolos para o Gesto Songs."""

from typing import Protocol, Dict, Set, Callable, Optional
import numpy as np


class SoundServiceProtocol(Protocol):
    """Protocolo para serviços de som."""
    
    def initialize(self) -> None:
        """Inicializa o sistema de som."""
        ...
    
    def load_sounds_from_config(
        self,
        left_hand_config: dict,
        right_hand_config: dict,
    ) -> None:
        """Carrega todos os sons das configurações."""
        ...
    
    def play_sound(self, sound_path: str) -> bool:
        """Reproduz um som."""
        ...
    
    def set_volume(self, volume: float) -> None:
        """Define o volume."""
        ...
    
    def stop_all(self) -> None:
        """Para todos os sons que estão tocando."""
        ...
    
    def cleanup(self) -> None:
        """Libera recursos do mixer."""
        ...


class GestureServiceProtocol(Protocol):
    """Protocolo para serviços de detecção de gestos."""
    
    def detect_finger_gestures(
        self,
        hand_landmarks,
        hand_idx: int,
        gesture_config: dict,
        w: int,
        h: int,
        on_gesture: Callable[[str, dict], None],
    ) -> Set[int]:
        """Detecta gestos de toque entre dedos."""
        ...
    
    def get_active_gestures(self, hand_idx: int) -> Set[int]:
        """Retorna os gestos ativos para uma mão."""
        ...
    
    def clear_old_notes(self, max_age: float = 0.5) -> None:
        """Remove notas antigas do registro."""
        ...
    
    def reset(self) -> None:
        """Reseta todos os gestos ativos."""
        ...


class ChallengeManagerProtocol(Protocol):
    """Protocolo para gerenciamento de desafios."""
    
    def generate_challenge(self) -> None:
        """Gera um novo desafio."""
        ...
    
    def check_completion(self, note_name: str, hand_label: str) -> bool:
        """Verifica se o desafio foi completado."""
        ...
    
    def check_timeout(self) -> bool:
        """Verifica se o desafio expirou."""
        ...
    
    def should_generate_new_challenge(self) -> bool:
        """Verifica se deve gerar um novo desafio."""
        ...
    
    def get_challenge_progress(self) -> Optional[float]:
        """Retorna o progresso atual do desafio (0 a 1)."""
        ...
    
    def get_remaining_time(self) -> Optional[float]:
        """Retorna o tempo restante do desafio atual."""
        ...
    
    def clear_result(self, display_duration: float = 1.0) -> bool:
        """Remove o resultado exibido após um tempo."""
        ...
    
    def reset_stats(self) -> None:
        """Reseta todas as estatísticas do jogo."""
        ...


class UIRendererProtocol(Protocol):
    """Protocolo para renderização de interface."""
    
    def draw_ui(
        self,
        frame: np.ndarray,
        game_stats,
        current_challenge,
        challenge_result,
        game_mode: str,
        challenge_progress: Optional[float] = None,
        remaining_time: Optional[float] = None,
    ) -> None:
        """Desenha a interface do usuário."""
        ...
    
    def draw_hand_gesture_guide(
        self,
        frame: np.ndarray,
        x: int,
        y: int,
        hand_label: str,
        finger_id: int,
        size: int = 100,
    ) -> None:
        """Desenha uma mini visualização do gesto da mão."""
        ...
    
    def draw_visual_feedback(
        self,
        frame: np.ndarray,
        hand_landmarks,
        active_gestures,
        gesture_config: dict,
        w: int,
        h: int,
    ) -> None:
        """Desenha feedback visual colorido para os gestos ativos."""
        ...
    
    def draw_footer(
        self,
        frame: np.ndarray,
        game_mode: str,
        w: int,
        h: int,
    ) -> None:
        """Desenha instruções na parte inferior."""
        ...


class CameraServiceProtocol(Protocol):
    """Protocolo para serviço de câmera."""
    
    def initialize(self) -> bool:
        """Inicializa a captura de vídeo."""
        ...
    
    def read_frame(self):
        """Lê um frame da câmera."""
        ...
    
    def get_frame_size(self):
        """Obtém as dimensões do frame."""
        ...
    
    def set_resolution(self, width: int, height: int) -> bool:
        """Define a resolução da câmera."""
        ...
    
    def cleanup(self) -> None:
        """Libera os recursos da câmera."""
        ...


class HandTrackingServiceProtocol(Protocol):
    """Protocolo para serviço de rastreamento de mãos."""
    
    def initialize(self) -> bool:
        """Inicializa o MediaPipe Hands."""
        ...
    
    def process_frame(self, frame):
        """Processa um frame para detectar mãos."""
        ...
    
    def cleanup(self) -> None:
        """Libera os recursos do MediaPipe."""
        ...

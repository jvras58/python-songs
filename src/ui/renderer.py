"""Renderizador principal de interface gráfica."""

import time
import cv2
import numpy as np

from src.domain.models import Challenge, GameStats
from .components.challenge_panel import ChallengePanel
from .components.stats_panel import StatsPanel
from .components.gesture_guide import GestureGuide
from .components.result_popup import ResultPopup
from .styles import UIStyles


class UIRenderer:
    """Responsável por desenhar todos os elementos visuais na tela."""

    def __init__(self):
        """Inicializa o renderizador de UI."""
        self.challenge_panel = ChallengePanel()
        self.stats_panel = StatsPanel()
        self.gesture_guide = GestureGuide()
        self.result_popup = ResultPopup()
        self.styles = UIStyles()

    def draw_ui(
        self,
        frame: np.ndarray,
        game_stats: GameStats,
        current_challenge: Challenge = None,
        challenge_result: tuple = None,
        game_mode: str = "challenge",
        challenge_progress: float = None,
        remaining_time: float = None,
    ) -> None:
        """
        Desenha toda a interface do usuário.
        
        Args:
            frame: Frame a ser desenhado
            game_stats: Estatísticas do jogo
            current_challenge: Desafio atual (se houver)
            challenge_result: Resultado do último desafio
            game_mode: Modo de jogo atual
            challenge_progress: Progresso do desafio (0-1)
            remaining_time: Tempo restante em segundos
        """
        h, w = frame.shape[:2]
        
        # Desenha estatísticas
        self.stats_panel.draw(frame, game_stats, w, h)
        
        # Desenha desafio se houver
        if current_challenge and challenge_progress is not None:
            self.challenge_panel.draw(
                frame,
                current_challenge,
                w,
                h,
                challenge_progress,
                remaining_time or 0,
            )
        
        # Desenha resultado se houver
        if challenge_result:
            result_text, timestamp = challenge_result
            self.result_popup.draw(frame, result_text, timestamp, w, h)
        
        # Desenha footer
        self.draw_footer(frame, game_mode, w, h)

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
        self.gesture_guide.draw(frame, x, y, hand_label, finger_id, size)

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
        for finger_id in active_gestures:
            if finger_id in gesture_config:
                # Pega posição do dedo
                finger = hand_landmarks.landmark[finger_id]
                fx, fy = int(finger.x * w), int(finger.y * h)

                # Pega cor baseada na nota
                note_name = gesture_config[finger_id]["name"]
                color = self.styles.NOTE_COLORS.get(note_name, (255, 255, 255))

                # Desenha círculo pulsante
                pulse = int(20 + 10 * abs(np.sin(time.time() * 10)))
                cv2.circle(frame, (fx, fy), pulse, color, 3)
                cv2.circle(frame, (fx, fy), 8, color, -1)

                # Desenha linha do polegar ao dedo
                thumb = hand_landmarks.landmark[4]
                tx, ty = int(thumb.x * w), int(thumb.y * h)
                cv2.line(frame, (tx, ty), (fx, fy), color, 2)

    def draw_footer(
        self,
        frame: np.ndarray,
        game_mode: str,
        w: int,
        h: int,
    ) -> None:
        """Desenha instruções na parte inferior."""
        mode_text = "CHALLENGE MODE" if game_mode == "challenge" else "FREE PLAY"
        cv2.putText(
            frame,
            f"Mode: {mode_text} | [M]Toggle | [Q]Quit",
            (10, h - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

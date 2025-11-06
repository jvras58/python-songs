"""Componente de painel de desafio."""

import cv2
import numpy as np
from src.domain.models import Challenge


class ChallengePanel:
    """Desenha o painel de desafio atual."""
    
    def draw(
        self,
        frame: np.ndarray,
        challenge: Challenge,
        w: int,
        h: int,
        progress: float,
        remaining: float,
    ) -> None:
        """
        Desenha o painel de desafio.
        
        Args:
            frame: Frame a ser desenhado
            challenge: Desafio atual
            w: Largura do frame
            h: Altura do frame
            progress: Progresso do desafio (0-1)
            remaining: Tempo restante em segundos
        """
        # Painel no topo centro
        panel_w = 450
        panel_h = 220
        panel_x = (w - panel_w) // 2
        panel_y = 30

        # Fundo com transparência
        overlay = frame.copy()
        cv2.rectangle(
            overlay,
            (panel_x, panel_y),
            (panel_x + panel_w, panel_y + panel_h),
            (0, 0, 0),
            -1,
        )
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)

        # Borda colorida baseada no tempo
        if progress > 0.5:
            border_color = (0, 255, 0)
        elif progress > 0.25:
            border_color = (0, 255, 255)
        else:
            border_color = (0, 0, 255)
        cv2.rectangle(
            frame,
            (panel_x, panel_y),
            (panel_x + panel_w, panel_y + panel_h),
            border_color,
            3,
        )

        # Título
        cv2.putText(
            frame,
            "PLAY THIS NOTE!",
            (panel_x + 20, panel_y + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
        )

        # Nota musical
        note_y = panel_y + 120
        cv2.putText(
            frame,
            challenge.note_name,
            (panel_x + 50, note_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            3.0,
            (0, 255, 255),
            5,
        )

        # Mini visualização do gesto (importado localmente para evitar circular)
        from .gesture_guide import GestureGuide
        guide = GestureGuide()
        guide_x = panel_x + panel_w - 140
        guide_y = panel_y + 50
        guide.draw(
            frame,
            guide_x,
            guide_y,
            challenge.hand_label,
            challenge.finger_id,
            120,
        )

        # Barra de tempo
        bar_x = panel_x + 20
        bar_y = panel_y + panel_h - 35
        bar_w = panel_w - 40
        bar_h = 18

        cv2.rectangle(
            frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (60, 60, 60), -1
        )

        progress_w = int(bar_w * progress)
        cv2.rectangle(
            frame, (bar_x, bar_y), (bar_x + progress_w, bar_y + bar_h), border_color, -1
        )

        cv2.putText(
            frame,
            f"{remaining:.1f}s",
            (bar_x + bar_w + 10, bar_y + 14),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 255, 255),
            1,
        )

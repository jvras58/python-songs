"""Componente de painel de estatísticas."""

import cv2
import numpy as np
from src.domain.models import GameStats


class StatsPanel:
    """Desenha o painel de estatísticas."""
    
    def draw(
        self,
        frame: np.ndarray,
        stats: GameStats,
        w: int,
        h: int,
    ) -> None:
        """
        Desenha o painel de estatísticas no canto superior direito.
        
        Args:
            frame: Frame a ser desenhado
            stats: Estatísticas do jogo
            w: Largura do frame
            h: Altura do frame
        """
        panel_x = w - 280
        panel_y = 30
        panel_w = 250
        panel_h = 230

        # Fundo
        overlay = frame.copy()
        cv2.rectangle(
            overlay,
            (panel_x, panel_y),
            (panel_x + panel_w, panel_y + panel_h),
            (0, 0, 0),
            -1,
        )
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        cv2.rectangle(
            frame,
            (panel_x, panel_y),
            (panel_x + panel_w, panel_y + panel_h),
            (255, 255, 255),
            2,
        )

        # Título
        cv2.putText(
            frame,
            "GAME STATS",
            (panel_x + 15, panel_y + 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        y = panel_y + 70
        spacing = 30

        # Score
        cv2.putText(
            frame,
            f"Score: {stats.score}",
            (panel_x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 0),
            2,
        )
        y += spacing

        # Level
        cv2.putText(
            frame,
            f"Level: {stats.level}",
            (panel_x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (147, 20, 255),
            2,
        )
        y += spacing

        # Streak
        streak_color = (0, 255, 0) if stats.streak > 3 else (255, 255, 255)
        cv2.putText(
            frame,
            f"Streak: {stats.streak}",
            (panel_x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            streak_color,
            2,
        )
        y += spacing

        # Max Streak
        cv2.putText(
            frame,
            f"Best Streak: {stats.max_streak}",
            (panel_x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 215, 0),
            1,
        )
        y += spacing

        # Accuracy
        cv2.putText(
            frame,
            f"Accuracy: {stats.accuracy:.1f}%",
            (panel_x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            1,
        )
        y += spacing

        # Perfect hits
        cv2.putText(
            frame,
            f"Perfect: {stats.perfect_hits}",
            (panel_x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 215, 0),
            1,
        )
        y += spacing

        # Challenges
        cv2.putText(
            frame,
            f"Played: {stats.total_challenges}",
            (panel_x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            1,
        )

"""Componente de popup de resultado."""

import time
import cv2
import numpy as np


class ResultPopup:
    """Desenha popup de resultado (acerto/erro)."""
    
    def draw(
        self,
        frame: np.ndarray,
        result_text: str,
        timestamp: float,
        w: int,
        h: int,
    ) -> None:
        """
        Desenha o popup de resultado.
        
        Args:
            frame: Frame a ser desenhado
            result_text: Texto do resultado
            timestamp: Timestamp do resultado
            w: Largura do frame
            h: Altura do frame
        """
        elapsed = time.time() - timestamp

        # Efeito de fade out
        alpha = 1.0 - (elapsed / 1.0)
        alpha = max(0, alpha)

        # Cor baseada no resultado
        if "PERFECT" in result_text:
            color = (255, 215, 0)  # Dourado
            scale = 2.0
        elif "LEVEL UP" in result_text:
            color = (147, 20, 255)  # Roxo
            scale = 1.8
        elif "MISSED" in result_text:
            color = (0, 0, 255)  # Vermelho
            scale = 1.5
        else:
            color = (0, 255, 0)  # Verde
            scale = 1.2

        # Centraliza texto
        text_size = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, scale, 3)[0]
        text_x = (w - text_size[0]) // 2
        text_y = int(h * 0.6)

        # Efeito de escala
        current_scale = scale * (1 + 0.2 * np.sin(elapsed * 10))

        # Aplica alpha à cor
        display_color = tuple(int(c * alpha) for c in color)

        cv2.putText(
            frame,
            result_text,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            current_scale,
            display_color,
            3,
        )

"""Componente de guia visual de gesto."""

import time
import cv2
import numpy as np


class GestureGuide:
    """Desenha uma mini visualização do gesto da mão."""
    
    def draw(
        self,
        frame: np.ndarray,
        x: int,
        y: int,
        hand_label: str,
        finger_id: int,
        size: int = 100,
    ) -> None:
        """
        Desenha o guia de gesto da mão.
        
        Args:
            frame: Frame a ser desenhado
            x: Posição X
            y: Posição Y
            hand_label: "Left" ou "Right"
            finger_id: ID do dedo (8, 12, 16, 20)
            size: Tamanho do guia
        """
        is_left = hand_label == "Left"

        # Posições dos dedos (proporções mais realistas)
        if is_left:
            # Mão esquerda - espelhada
            finger_positions = {
                4: (0.85, 0.65),   # Polegar (à direita)
                8: (0.65, 0.15),   # Indicador
                12: (0.5, 0.08),   # Médio
                16: (0.35, 0.12),  # Anelar
                20: (0.2, 0.25),   # Mínimo
            }
            finger_bases = {
                4: (0.75, 0.75),
                8: (0.62, 0.55),
                12: (0.5, 0.5),
                16: (0.38, 0.53),
                20: (0.27, 0.58),
            }
        else:
            # Mão direita - normal
            finger_positions = {
                4: (0.15, 0.65),   # Polegar (à esquerda)
                8: (0.35, 0.15),   # Indicador
                12: (0.5, 0.08),   # Médio
                16: (0.65, 0.12),  # Anelar
                20: (0.8, 0.25),   # Mínimo
            }
            finger_bases = {
                4: (0.25, 0.75),
                8: (0.38, 0.55),
                12: (0.5, 0.5),
                16: (0.62, 0.53),
                20: (0.73, 0.58),
            }

        # Fundo
        cv2.rectangle(frame, (x, y), (x + size, y + size), (40, 40, 40), -1)
        cv2.rectangle(frame, (x, y), (x + size, y + size), (255, 255, 255), 2)

        # Desenha a palma da mão
        palm_points = [
            (x + int(0.25 * size), y + int(0.75 * size)),
            (x + int(0.35 * size), y + int(0.85 * size)),
            (x + int(0.65 * size), y + int(0.85 * size)),
            (x + int(0.75 * size), y + int(0.6 * size)),
            (x + int(0.65 * size), y + int(0.5 * size)),
            (x + int(0.5 * size), y + int(0.45 * size)),
            (x + int(0.35 * size), y + int(0.5 * size)),
        ]
        palm_array = np.array(palm_points, dtype=np.int32)
        cv2.fillPoly(frame, [palm_array], (180, 140, 120))
        cv2.polylines(frame, [palm_array], True, (120, 100, 90), 2)

        # Desenha os dedos
        for fid in finger_positions:
            base_x = x + int(finger_bases[fid][0] * size)
            base_y = y + int(finger_bases[fid][1] * size)
            tip_x = x + int(finger_positions[fid][0] * size)
            tip_y = y + int(finger_positions[fid][1] * size)

            if fid == finger_id or fid == 4:
                line_color = (100, 200, 100)
                line_thickness = 8
            else:
                line_color = (160, 130, 110)
                line_thickness = 6

            cv2.line(frame, (base_x, base_y), (tip_x, tip_y), line_color, line_thickness)

        # Desenha as pontas dos dedos
        for fid, (fx, fy) in finger_positions.items():
            finger_x = x + int(fx * size)
            finger_y = y + int(fy * size)

            if fid == finger_id or fid == 4:
                color = (0, 255, 0)
                radius = 14
                pulse = int(18 + 4 * abs(np.sin(time.time() * 5)))
                cv2.circle(frame, (finger_x, finger_y), pulse, (0, 255, 0), 2)
            else:
                color = (200, 160, 140)
                radius = 10

            cv2.circle(frame, (finger_x, finger_y), radius, color, -1)
            cv2.circle(frame, (finger_x, finger_y), radius, (100, 80, 70), 2)

        # Linha de conexão animada
        if finger_id in finger_positions:
            thumb_x = x + int(finger_positions[4][0] * size)
            thumb_y = y + int(finger_positions[4][1] * size)
            target_x = x + int(finger_positions[finger_id][0] * size)
            target_y = y + int(finger_positions[finger_id][1] * size)

            cv2.line(frame, (thumb_x, thumb_y), (target_x, target_y), (0, 200, 0), 6)
            cv2.line(frame, (thumb_x, thumb_y), (target_x, target_y), (0, 255, 0), 3)

            mid_x = (thumb_x + target_x) // 2
            mid_y = (thumb_y + target_y) // 2
            cv2.circle(frame, (mid_x, mid_y), 8, (255, 255, 0), -1)

        # Label da mão
        label_text = hand_label + " Hand"
        label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
        label_x = x + (size - label_size[0]) // 2
        label_y = y + size - 8

        cv2.rectangle(
            frame,
            (label_x - 3, label_y - label_size[1] - 3),
            (label_x + label_size[0] + 3, label_y + 3),
            (0, 0, 0),
            -1,
        )
        cv2.putText(
            frame,
            label_text,
            (label_x, label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 255, 255),
            1,
        )

"""Gesto Songs - Aplicação principal."""

import logging
from typing import Dict, Optional

import cv2
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.python.solutions.hands import HAND_CONNECTIONS

from config.config import CONFIG
from src.services.sound_service import SoundService
from src.services.gesture_service import GestureService
from src.services.camera_service import CameraService
from src.services.hand_tracking_service import HandTrackingService
from src.game.challenge_manager import ChallengeManager
from src.ui.renderer import UIRenderer

logger = logging.getLogger(__name__)


class GestoSongs:
    """Classe principal para o Gesto Songs com interação baseada em gestos."""

    def __init__(self):
        self.hand_labels: Dict[int, str] = {}

        # Serviços
        self.sound_service = SoundService(volume=CONFIG["volume"])
        self.gesture_service = GestureService(
            touch_threshold=CONFIG.get("gesture_touch_threshold", 40)
        )
        self.camera_service = CameraService(camera_index=CONFIG["camera_index"])
        self.hand_tracking_service = HandTrackingService(
            **CONFIG["hands_config"]
        )
        self.ui_renderer = UIRenderer()

        # Mapeamento reverso: note_name -> (hand, finger_id)
        self.note_to_gesture: Dict[str, tuple] = {}

        # Gerenciador de desafios (será inicializado após setup)
        self.challenge_manager: Optional[ChallengeManager] = None

        # Modo de jogo
        self.game_mode: str = "challenge"  # "free" ou "challenge"

    def setup(self) -> None:
        """Inicializa serviços e recursos."""
        # Inicializa som
        self.sound_service.initialize()
        self.sound_service.load_sounds_from_config(
            CONFIG["left_hand_gestures"],
            CONFIG["right_hand_gestures"],
        )

        # Inicializa rastreamento de mãos
        if not self.hand_tracking_service.initialize():
            raise RuntimeError("Failed to initialize hand tracking service")

        # Inicializa câmera
        if not self.camera_service.initialize():
            raise RuntimeError("Failed to initialize camera service")
        
        self.camera_service.set_resolution(1280, 720)

        # Constrói mapeamento de notas
        self._build_note_mapping()

        # Inicializa gerenciador de desafios
        self.challenge_manager = ChallengeManager(self.note_to_gesture)

        logger.info("Gesto Songs initialized successfully")

    def _build_note_mapping(self) -> None:
        """Constrói mapeamento reverso de notas para gestos."""
        for hand_label in ["Left", "Right"]:
            gesture_config = (
                CONFIG["left_hand_gestures"]
                if hand_label == "Left"
                else CONFIG["right_hand_gestures"]
            )

            for finger_id, gesture_data in gesture_config.items():
                note_name = gesture_data["name"]
                self.note_to_gesture[note_name] = (hand_label, finger_id)

    def _on_gesture_detected(
        self, note_name: str, gesture_data: dict, hand_label: str
    ) -> None:
        """
        Callback chamado quando um gesto é detectado.

        Args:
            note_name: Nome da nota
            gesture_data: Dados do gesto
            hand_label: Mão utilizada
        """
        # Toca o som
        sound_path = gesture_data["sound"]
        self.sound_service.play_sound(sound_path)

        # Verifica se completou o desafio
        if self.game_mode == "challenge" and self.challenge_manager:
            self.challenge_manager.check_completion(note_name, hand_label)

        logger.info(f"{hand_label} hand - Gesture: {note_name}")

    def update_loop(self) -> None:
        """Processa um frame do vídeo."""
        # Lê frame da câmera
        success, frame = self.camera_service.read_frame()
        if not success or frame is None:
            logger.warning("Failed to read frame from camera.")
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hand_tracking_service.process_frame(rgb)

        w, h = frame.shape[1], frame.shape[0]

        # Processa mãos
        multi_hand_landmarks = getattr(result, "multi_hand_landmarks", None)
        multi_handedness = getattr(result, "multi_handedness", None)

        if multi_hand_landmarks and multi_handedness:
            for idx, (hand_landmarks, handedness) in enumerate(
                zip(multi_hand_landmarks, multi_handedness)
            ):
                hand_label = handedness.classification[0].label
                self.hand_labels[idx] = hand_label

                # Seleciona configuração de gestos
                gesture_config = (
                    CONFIG["left_hand_gestures"]
                    if hand_label == "Left"
                    else CONFIG["right_hand_gestures"]
                )

                # Detecta gestos
                active_gestures = self.gesture_service.detect_finger_gestures(
                    hand_landmarks,
                    idx,
                    gesture_config,
                    w,
                    h,
                    lambda note, data: self._on_gesture_detected(
                        note, data, hand_label
                    ),
                )

                # Desenha feedback visual
                self.ui_renderer.draw_visual_feedback(
                    frame,
                    hand_landmarks,
                    active_gestures,
                    gesture_config,
                    w,
                    h,
                )

                # Desenha landmarks da mão
                draw_landmarks(frame, hand_landmarks, list(HAND_CONNECTIONS))

                # Label da mão
                wrist = hand_landmarks.landmark[0]
                text_x, text_y = int(wrist.x * w), int(wrist.y * h) - 20
                cv2.putText(
                    frame,
                    hand_label,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                )

        # Gerencia desafios no modo challenge
        if self.game_mode == "challenge" and self.challenge_manager:
            # Verifica timeout
            self.challenge_manager.check_timeout()

            # Gera novo desafio se necessário
            if self.challenge_manager.should_generate_new_challenge():
                self.challenge_manager.generate_challenge()

            # Desenha UI do jogo usando o novo método unificado
            progress = self.challenge_manager.get_challenge_progress()
            remaining = self.challenge_manager.get_remaining_time()
            
            self.ui_renderer.draw_ui(
                frame,
                self.challenge_manager.game_stats,
                self.challenge_manager.current_challenge,
                self.challenge_manager.challenge_result,
                self.game_mode,
                progress,
                remaining,
            )
            
            # Limpa resultado
            if self.challenge_manager.challenge_result:
                self.challenge_manager.clear_result()
        else:
            # Modo free - apenas desenha stats
            if self.challenge_manager:
                self.ui_renderer.draw_ui(
                    frame,
                    self.challenge_manager.game_stats,
                    None,
                    None,
                    self.game_mode,
                    None,
                    None,
                )

        cv2.imshow("Gesto Songs", frame)

        # Teclas
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            logger.info("Exit requested by user.")
            raise SystemExit
        elif key == ord("m"):
            # Alterna modo
            self.game_mode = "free" if self.game_mode == "challenge" else "challenge"
            if self.challenge_manager:
                self.challenge_manager.current_challenge = None
            logger.info(f"Switched to {self.game_mode} mode")

    def cleanup(self) -> None:
        """Libera recursos."""
        self.camera_service.cleanup()
        cv2.destroyAllWindows()
        self.hand_tracking_service.cleanup()
        self.sound_service.cleanup()
        logger.info("Resources cleaned up.")

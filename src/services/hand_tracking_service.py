"""Serviço de rastreamento de mãos usando MediaPipe."""

import logging
from typing import Optional, Any

from mediapipe.python.solutions.hands import Hands

logger = logging.getLogger(__name__)


class HandTrackingService:
    """Wrapper para o MediaPipe Hands."""

    def __init__(
        self,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.7,
    ):
        """
        Inicializa o serviço de rastreamento de mãos.
        
        Args:
            max_num_hands: Número máximo de mãos a detectar
            min_detection_confidence: Confiança mínima para detecção
            min_tracking_confidence: Confiança mínima para rastreamento
        """
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.hands: Optional[Hands] = None
        self._initialized = False

    def initialize(self) -> bool:
        """
        Inicializa o MediaPipe Hands.
        
        Returns:
            True se foi inicializado com sucesso
        """
        try:
            self.hands = Hands(
                max_num_hands=self.max_num_hands,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            )
            self._initialized = True
            logger.info("Hand tracking service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MediaPipe Hands: {e}")
            return False

    def process_frame(self, frame) -> Any:
        """
        Processa um frame para detectar mãos.
        
        Args:
            frame: Frame RGB a ser processado
            
        Returns:
            Resultados do processamento do MediaPipe
        """
        if not self._initialized or self.hands is None:
            logger.warning("Hand tracking service not initialized")
            return None
        
        try:
            return self.hands.process(frame)
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return None

    def cleanup(self) -> None:
        """Libera os recursos do MediaPipe."""
        if self.hands is not None:
            self.hands.close()
            self._initialized = False
            logger.info("Hand tracking service cleaned up")

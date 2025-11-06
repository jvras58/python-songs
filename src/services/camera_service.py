"""Serviço de gerenciamento de câmera."""

import logging
from typing import Optional, Tuple

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class CameraService:
    """Gerencia a captura de vídeo da câmera."""

    def __init__(self, camera_index: int = 0):
        """
        Inicializa o serviço de câmera.
        
        Args:
            camera_index: Índice da câmera a ser utilizada
        """
        self.camera_index = camera_index
        self.cap: Optional[cv2.VideoCapture] = None
        self._initialized = False

    def initialize(self) -> bool:
        """
        Inicializa a captura de vídeo.
        
        Returns:
            True se a câmera foi inicializada com sucesso
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera at index {self.camera_index}")
                return False
            
            self._initialized = True
            logger.info(f"Camera initialized successfully at index {self.camera_index}")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            return False

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Lê um frame da câmera.
        
        Returns:
            Tupla (sucesso, frame) onde sucesso indica se a leitura foi bem-sucedida
        """
        if not self._initialized or self.cap is None:
            logger.warning("Camera not initialized")
            return False, None
        
        try:
            success, frame = self.cap.read()
            if not success:
                logger.warning("Failed to read frame from camera")
            return success, frame
        except Exception as e:
            logger.error(f"Error reading frame: {e}")
            return False, None

    def get_frame_size(self) -> Tuple[int, int]:
        """
        Obtém as dimensões do frame.
        
        Returns:
            Tupla (largura, altura)
        """
        if not self._initialized or self.cap is None:
            return (0, 0)
        
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)

    def set_resolution(self, width: int, height: int) -> bool:
        """
        Define a resolução da câmera.
        
        Args:
            width: Largura desejada
            height: Altura desejada
            
        Returns:
            True se a resolução foi configurada com sucesso
        """
        if not self._initialized or self.cap is None:
            logger.warning("Camera not initialized")
            return False
        
        try:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            logger.info(f"Camera resolution set to {width}x{height}")
            return True
        except Exception as e:
            logger.error(f"Error setting resolution: {e}")
            return False

    def cleanup(self) -> None:
        """Libera os recursos da câmera."""
        if self.cap is not None:
            self.cap.release()
            self._initialized = False
            logger.info("Camera resources released")

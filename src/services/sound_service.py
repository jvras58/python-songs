"""Serviço de gerenciamento de som."""

import logging
import os
import sys
from typing import Dict, Set

from pygame import mixer

logger = logging.getLogger(__name__)


class SoundService:
    """Gerencia o carregamento e reprodução de sons."""

    def __init__(self, volume: float = 0.7):
        """
        Inicializa o serviço de sons.
        
        Args:
            volume: Volume inicial (0.0 a 1.0)
        """
        self.volume = volume
        self.loaded_sounds: Dict[str, mixer.Sound] = {}
        self._initialized = False
        # Determina o caminho base para arquivos de dados
        if hasattr(sys, '_MEIPASS'):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.getcwd()

    def initialize(self) -> None:
        """Inicializa o mixer do pygame."""
        try:
            mixer.init()
            mixer.music.set_volume(self.volume)
            self._initialized = True
            logger.info("Sound service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")
            raise

    def load_sounds_from_config(
        self,
        left_hand_config: dict,
        right_hand_config: dict,
    ) -> None:
        """
        Carrega todos os sons das configurações.
        
        Args:
            left_hand_config: Configuração de gestos da mão esquerda
            right_hand_config: Configuração de gestos da mão direita
        """
        if not self._initialized:
            raise RuntimeError("Sound service not initialized. Call initialize() first.")

        # Coleta todos os caminhos de som únicos
        all_sounds: Set[str] = set()
        
        for gesture_config in [left_hand_config, right_hand_config]:
            for finger_id, gesture in gesture_config.items():
                all_sounds.add(gesture["sound"])

        # Carrega cada som
        for sound_path in all_sounds:
            try:
                full_path = os.path.join(self.base_path, sound_path)
                sound = mixer.Sound(full_path)
                sound.set_volume(self.volume)
                self.loaded_sounds[sound_path] = sound
                logger.info(f"Loaded sound: {sound_path}")
            except Exception as e:
                logger.error(f"Failed to load sound {sound_path}: {e}")

    def play_sound(self, sound_path: str) -> bool:
        """
        Reproduz um som.
        
        Args:
            sound_path: Caminho do arquivo de som
            
        Returns:
            True se o som foi reproduzido com sucesso
        """
        if sound_path not in self.loaded_sounds:
            logger.warning(f"Sound not loaded: {sound_path}")
            return False

        try:
            self.loaded_sounds[sound_path].play()
            return True
        except Exception as e:
            logger.error(f"Error playing sound {sound_path}: {e}")
            return False

    def set_volume(self, volume: float) -> None:
        """
        Define o volume global.
        
        Args:
            volume: Novo volume (0.0 a 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        
        if self._initialized:
            mixer.music.set_volume(self.volume)
            
            for sound in self.loaded_sounds.values():
                sound.set_volume(self.volume)
        
        logger.info(f"Volume set to {self.volume}")

    def stop_all(self) -> None:
        """Para todos os sons que estão tocando."""
        if self._initialized:
            mixer.stop()
            logger.info("All sounds stopped")

    def cleanup(self) -> None:
        """Libera recursos do mixer."""
        if self._initialized:
            mixer.quit()
            self._initialized = False
            logger.info("Sound service cleaned up")

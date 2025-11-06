"""Gerenciador de desafios do jogo."""

import logging
import random
import time
from typing import Dict, Optional, Tuple

from src.domain.models import Challenge, GameStats

logger = logging.getLogger(__name__)


class ChallengeManager:
    """Gerencia a criação, validação e pontuação de desafios."""

    def __init__(self, note_to_gesture: Dict[str, Tuple[str, int]]):
        """
        Inicializa o gerenciador de desafios.
        
        Args:
            note_to_gesture: Mapeamento de nota para (hand_label, finger_id)
        """
        self.note_to_gesture = note_to_gesture
        self.game_stats = GameStats()
        self.current_challenge: Optional[Challenge] = None
        self.challenge_result: Optional[Tuple[str, float]] = None
        self.last_challenge_time: float = 0
        self.challenge_cooldown: float = 1.0  # segundos entre desafios

    def generate_challenge(self) -> None:
        """Gera um novo desafio aleatório."""
        if not self.note_to_gesture:
            logger.warning("No notes available for challenge generation")
            return

        note_name = random.choice(list(self.note_to_gesture.keys()))
        hand_label, finger_id = self.note_to_gesture[note_name]

        # Tempo limite diminui com o nível (mais difícil)
        time_limit = max(1.5, 3.5 - (self.game_stats.level * 0.2))

        self.current_challenge = Challenge(
            note_name=note_name,
            finger_id=finger_id,
            hand_label=hand_label,
            start_time=time.time(),
            time_limit=time_limit,
        )
        self.game_stats.total_challenges += 1
        logger.info(
            f"New challenge: {note_name} - {hand_label} hand, finger {finger_id}"
        )

    def check_completion(self, note_name: str, hand_label: str) -> bool:
        """
        Verifica se o desafio foi completado corretamente.
        
        Args:
            note_name: Nome da nota tocada
            hand_label: Mão usada
            
        Returns:
            True se o desafio foi completado
        """
        if not self.current_challenge:
            return False

        current_time = time.time()
        elapsed = current_time - self.current_challenge.start_time

        # Verifica se acertou
        if (
            note_name == self.current_challenge.note_name
            and hand_label == self.current_challenge.hand_label
        ):
            # Calcula pontuação baseada na velocidade
            time_bonus = max(
                0, int((self.current_challenge.time_limit - elapsed) * 100)
            )
            base_points = 100
            points = base_points + time_bonus

            self.game_stats.score += points
            self.game_stats.correct_hits += 1
            self.game_stats.streak += 1

            if self.game_stats.streak > self.game_stats.max_streak:
                self.game_stats.max_streak = self.game_stats.streak

            # Hit perfeito (< 0.5s)
            if elapsed < 0.5:
                self.game_stats.perfect_hits += 1
                self.challenge_result = ("PERFECT!", current_time)
            else:
                self.challenge_result = (f"+{points}", current_time)

            # Aumenta nível a cada 5 acertos
            if self.game_stats.correct_hits % 5 == 0:
                self.game_stats.level += 1
                self.challenge_result = (
                    f"LEVEL UP! {self.game_stats.level}",
                    current_time,
                )

            self.current_challenge = None
            self.last_challenge_time = current_time
            return True

        return False

    def check_timeout(self) -> bool:
        """
        Verifica se o desafio expirou.
        
        Returns:
            True se o desafio expirou
        """
        if not self.current_challenge:
            return False

        elapsed = time.time() - self.current_challenge.start_time
        if elapsed > self.current_challenge.time_limit:
            self.game_stats.streak = 0
            self.challenge_result = ("MISSED!", time.time())
            self.current_challenge = None
            self.last_challenge_time = time.time()
            return True

        return False

    def should_generate_new_challenge(self) -> bool:
        """Verifica se deve gerar um novo desafio."""
        current_time = time.time()
        return (
            not self.current_challenge
            and current_time - self.last_challenge_time > self.challenge_cooldown
        )

    def get_challenge_progress(self) -> Optional[float]:
        """
        Retorna o progresso atual do desafio (0 a 1).
        
        Returns:
            Progresso normalizado ou None se não há desafio ativo
        """
        if not self.current_challenge:
            return None

        current_time = time.time()
        elapsed = current_time - self.current_challenge.start_time
        progress = 1 - (elapsed / self.current_challenge.time_limit)
        return max(0, min(1, progress))

    def get_remaining_time(self) -> Optional[float]:
        """
        Retorna o tempo restante do desafio atual.
        
        Returns:
            Tempo restante em segundos ou None se não há desafio ativo
        """
        if not self.current_challenge:
            return None

        current_time = time.time()
        elapsed = current_time - self.current_challenge.start_time
        return max(0, self.current_challenge.time_limit - elapsed)

    def clear_result(self, display_duration: float = 1.0) -> bool:
        """
        Remove o resultado exibido após um tempo.
        
        Args:
            display_duration: Duração em segundos para exibir o resultado
            
        Returns:
            True se o resultado foi removido
        """
        if not self.challenge_result:
            return False

        _, timestamp = self.challenge_result
        elapsed = time.time() - timestamp

        if elapsed > display_duration:
            self.challenge_result = None
            return True

        return False

    def reset_stats(self) -> None:
        """Reseta todas as estatísticas do jogo."""
        self.game_stats.reset()
        self.current_challenge = None
        self.challenge_result = None
        self.last_challenge_time = 0
        logger.info("Game stats reset")

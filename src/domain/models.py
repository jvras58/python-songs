"""Modelos de dados para o Gesto Songs."""

from dataclasses import dataclass


@dataclass
class Challenge:
    """Representa um desafio de nota."""
    note_name: str
    finger_id: int
    hand_label: str
    start_time: float
    time_limit: float = 3.0  # segundos para completar


class GameStats:
    """Estatísticas do jogo."""
    def __init__(self):
        self.score: int = 0
        self.total_challenges: int = 0
        self.correct_hits: int = 0
        self.streak: int = 0
        self.max_streak: int = 0
        self.level: int = 1
        self.perfect_hits: int = 0  # hits com < 0.5s

    @property
    def accuracy(self) -> float:
        """Calcula a precisão atual."""
        if self.total_challenges == 0:
            return 0.0
        return (self.correct_hits / self.total_challenges) * 100

    def reset(self) -> None:
        """Reseta todas as estatísticas."""
        self.score = 0
        self.total_challenges = 0
        self.correct_hits = 0
        self.streak = 0
        self.max_streak = 0
        self.level = 1
        self.perfect_hits = 0

"""Testes para o módulo de modelos."""

import pytest
from src.domain.models import Challenge, GameStats


class TestChallenge:
    """Testes para a classe Challenge."""
    
    def test_challenge_creation(self):
        """Testa a criação de um desafio."""
        challenge = Challenge(
            note_name="C4",
            finger_id=8,
            hand_label="Left",
            start_time=0.0,
            time_limit=3.0
        )
        
        assert challenge.note_name == "C4"
        assert challenge.finger_id == 8
        assert challenge.hand_label == "Left"
        assert challenge.start_time == 0.0
        assert challenge.time_limit == 3.0


class TestGameStats:
    """Testes para a classe GameStats."""
    
    def test_initial_stats(self):
        """Testa estatísticas iniciais."""
        stats = GameStats()
        
        assert stats.score == 0
        assert stats.total_challenges == 0
        assert stats.correct_hits == 0
        assert stats.streak == 0
        assert stats.max_streak == 0
        assert stats.level == 1
        assert stats.perfect_hits == 0
    
    def test_accuracy_calculation(self):
        """Testa cálculo de precisão."""
        stats = GameStats()
        
        # Sem desafios
        assert stats.accuracy == 0.0
        
        # Com desafios
        stats.total_challenges = 10
        stats.correct_hits = 7
        assert stats.accuracy == 70.0
    
    def test_reset(self):
        """Testa reset das estatísticas."""
        stats = GameStats()
        stats.score = 1000
        stats.total_challenges = 10
        stats.correct_hits = 8
        stats.streak = 5
        stats.max_streak = 7
        stats.level = 3
        stats.perfect_hits = 2
        
        stats.reset()
        
        assert stats.score == 0
        assert stats.total_challenges == 0
        assert stats.correct_hits == 0
        assert stats.streak == 0
        assert stats.max_streak == 0
        assert stats.level == 1
        assert stats.perfect_hits == 0

"""Testes para o gerenciador de desafios."""

import pytest
import time
from src.game.challenge_manager import ChallengeManager
from src.domain.models import GameStats


class TestChallengeManager:
    """Testes para a classe ChallengeManager."""
    
    def test_initialization(self, sample_note_to_gesture):
        """Testa inicialização do gerenciador."""
        manager = ChallengeManager(sample_note_to_gesture)
        
        assert manager.note_to_gesture == sample_note_to_gesture
        assert isinstance(manager.game_stats, GameStats)
        assert manager.current_challenge is None
        assert manager.challenge_result is None
    
    def test_generate_challenge(self, sample_note_to_gesture):
        """Testa geração de desafio."""
        manager = ChallengeManager(sample_note_to_gesture)
        manager.generate_challenge()
        
        assert manager.current_challenge is not None
        assert manager.current_challenge.note_name in sample_note_to_gesture
        assert manager.game_stats.total_challenges == 1
    
    def test_check_completion_correct(self, sample_note_to_gesture):
        """Testa completar desafio corretamente."""
        manager = ChallengeManager(sample_note_to_gesture)
        manager.generate_challenge()
        
        challenge = manager.current_challenge
        result = manager.check_completion(
            challenge.note_name,
            challenge.hand_label
        )
        
        assert result is True
        assert manager.game_stats.correct_hits == 1
        assert manager.game_stats.streak == 1
        assert manager.current_challenge is None
    
    def test_check_completion_incorrect(self, sample_note_to_gesture):
        """Testa completar desafio incorretamente."""
        manager = ChallengeManager(sample_note_to_gesture)
        manager.generate_challenge()
        
        result = manager.check_completion("WRONG", "Wrong")
        
        assert result is False
        assert manager.game_stats.correct_hits == 0
        assert manager.current_challenge is not None
    
    def test_reset_stats(self, sample_note_to_gesture):
        """Testa reset de estatísticas."""
        manager = ChallengeManager(sample_note_to_gesture)
        manager.game_stats.score = 1000
        manager.game_stats.level = 5
        
        manager.reset_stats()
        
        assert manager.game_stats.score == 0
        assert manager.game_stats.level == 1
        assert manager.current_challenge is None

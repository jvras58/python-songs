"""Estilos e cores da interface."""

class UIStyles:
    """Constantes de estilos para a UI."""
    
    # Cores para cada tipo de nota
    NOTE_COLORS = {
        "C4": (255, 0, 0),      # Vermelho
        "C#4": (255, 128, 0),   # Laranja
        "D4": (255, 255, 0),    # Amarelo
        "D#4": (128, 255, 0),   # Verde-amarelo
        "E4": (0, 255, 0),      # Verde
        "F4": (0, 255, 255),    # Ciano
        "F#4": (0, 128, 255),   # Azul claro
        "G4": (0, 0, 255),      # Azul
        "G#4": (128, 0, 255),   # Roxo
        "A4": (255, 0, 255),    # Magenta
    }
    
    # Cores gerais
    COLOR_SUCCESS = (0, 255, 0)
    COLOR_WARNING = (0, 255, 255)
    COLOR_ERROR = (0, 0, 255)
    COLOR_PERFECT = (255, 215, 0)
    COLOR_LEVEL_UP = (147, 20, 255)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    
    # Fontes
    FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE_SMALL = 0.5
    FONT_SCALE_MEDIUM = 0.8
    FONT_SCALE_LARGE = 1.5
    FONT_SCALE_XLARGE = 3.0

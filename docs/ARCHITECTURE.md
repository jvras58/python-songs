# Arquitetura do Gestos Songs - Diagrama de Classes

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            GestoSongs                                   │
│  (Classe Principal - Orquestrador)                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  Atributos:                                                             │
│  - hands: MediaPipe Hands                                               │
│  - cap: VideoCapture                                                    │
│  - sound_manager: SoundManager                                          │
│  - gesture_detector: GestureDetector                                    │
│  - ui_renderer: UIRenderer                                              │
│  - challenge_manager: ChallengeManager                                  │
│  - note_to_gesture: Dict[str, Tuple]                                    │
│  - game_mode: str                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  Métodos:                                                               │
│  + setup()                                                              │
│  + update_loop()                                                        │
│  + cleanup()                                                            │
│  - _build_note_mapping()                                                │
│  - _on_gesture_detected()                                               │
└─────────────────────────────────────────────────────────────────────────┘
                    │
                    │ usa
        ┌───────────┼───────────┬─────────────┬────────────────┐
        │           │           │             │                │
        ▼           ▼           ▼             ▼                ▼
┌──────────────┐ ┌──────────┐ ┌─────────────┐ ┌──────────────┐ ┌────────────┐
│ SoundManager │ │ Gesture  │ │ Challenge   │ │ UIRenderer   │ │  Models    │
│              │ │ Detector │ │ Manager     │ │              │ │            │
├──────────────┤ ├──────────┤ ├─────────────┤ ├──────────────┤ ├────────────┤
│ + initialize │ │ + detect_│ │ + generate_ │ │ + draw_      │ │ Challenge  │
│ + load_sounds│ │  finger_ │ │   challenge │ │   challenge_ │ │            │
│ + play_sound │ │  gestures│ │ + check_    │ │   panel      │ │ GameStats  │
│ + set_volume │ │ + get_   │ │   completion│ │ + draw_stats_│ │            │
│ + cleanup    │ │  active_ │ │ + check_    │ │   panel      │ │            │
│              │ │  gestures│ │   timeout   │ │ + draw_      │ │            │
│              │ │ + reset  │ │ + should_   │ │   result_    │ │            │
│              │ │          │ │   generate_ │ │   popup      │ │            │
│              │ │          │ │   new_      │ │ + draw_      │ │            │
│              │ │          │ │   challenge │ │   visual_    │ │            │
│              │ │          │ │ + reset_    │ │   feedback   │ │            │
│              │ │          │ │   stats     │ │ + draw_      │ │            │
│              │ │          │ │             │ │   footer     │ │            │
└──────────────┘ └──────────┘ └─────────────┘ └──────────────┘ └────────────┘
                                     │
                                     │ usa
                                     ▼
                              ┌────────────┐
                              │  Models    │
                              ├────────────┤
                              │ Challenge  │
                              │ GameStats  │
                              └────────────┘
```

## Fluxo de Dados

```
┌──────────────┐
│   Câmera     │
└──────┬───────┘
       │ frame
       ▼
┌──────────────┐
│  MediaPipe   │
│    Hands     │
└──────┬───────┘
       │ landmarks
       ▼
┌──────────────────────────────────────────────────────────────┐
│                     GestoSongs                               │
│                                                              │
│  ┌─────────────┐     ┌──────────────┐                        │
│  │   Gesture   │────▶│    Sound     │                        │
│  │  Detector   │     │   Manager    │                        │
│  └─────┬───────┘     └──────────────┘                        │
│        │                                                     │
│        │ nota detectada                                      │
│        ▼                                                     │
│  ┌──────────────┐                                            │
│  │  Challenge   │                                            │
│  │   Manager    │                                            │
│  └──────┬───────┘                                            │
│         │                                                    │
│         │ estado do jogo                                     │
│         ▼                                                    │
│  ┌──────────────┐                                            │
│  │ UI Renderer  │                                            │
│  └──────┬───────┘                                            │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │ frame anotado
          ▼
    ┌──────────┐
    │  Display │
    └──────────┘
```

## Responsabilidades por Módulo

### GestoSongs (Orquestrador)
```
Entrada: Frame da câmera
Saída: Frame processado com UI
```
- Coordena todos os componentes
- Gerencia o loop principal
- Processa eventos de teclado

### GestureDetector
```
Entrada: Landmarks das mãos
Saída: Gestos detectados (callbacks)
```
- Calcula distâncias entre dedos
- Detecta transições de estado
- Mantém histórico de gestos

### SoundManager
```
Entrada: Caminho do som
Saída: Som reproduzido
```
- Carrega sons em memória
- Reproduz sons sob demanda
- Controla volume global

### ChallengeManager
```
Entrada: Gestos do jogador
Saída: Estado do jogo, pontuação
```
- Gera desafios aleatórios
- Valida respostas
- Calcula pontuação
- Gerencia progressão

### UIRenderer
```
Entrada: Estado do jogo, landmarks
Saída: Frame com UI desenhada
```
- Desenha painéis e popups
- Renderiza feedback visual
- Mostra estatísticas

### Models
```
Estruturas de dados puras
```
- Define Challenge
- Define GameStats
- Sem lógica de negócio

## Padrões de Design Utilizados

### 1. **Separation of Concerns**
Cada módulo tem uma responsabilidade única e bem definida.

### 2. **Dependency Injection**
GestoSongs recebe/cria instâncias dos gerenciadores, facilitando testes.

### 3. **Callback Pattern**
GestureDetector usa callbacks para notificar gestos detectados.

### 4. **Strategy Pattern**
Diferentes modos de jogo (challenge/free) alteram comportamento.

### 5. **Facade Pattern**
GestoSongs fornece interface simples para funcionalidades complexas.

## Dependências entre Módulos

```
gesto_songs.py
├── models.py (Challenge, GameStats)
├── challenge_manager.py
│   └── models.py
├── gesture_detector.py
├── sound_manager.py
└── ui_renderer.py
    └── models.py
```

**Observação**: Nenhum módulo secundário depende do GestoSongs,
permitindo testá-los e reutilizá-los independentemente.

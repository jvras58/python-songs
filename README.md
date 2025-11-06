# 🎹 Gesto Songs - Piano Virtual por Detecção de Gestos

[![Python](https://img.shields.io/badge/python-3.12%2B-blue)]()
[![Version](https://img.shields.io/badge/version-2.0.0-green)]()

Um piano virtual interativo que usa **visão computacional** e **MediaPipe** para detectar gestos das mãos e tocar notas musicais em tempo real, com sistema de desafios e gamificação.

## ✨ Características Principais

- 🖐️ **Detecção de gestos em tempo real**: Toque notas aproximando dedos do polegar
- 👐 **Suporte para 2 mãos**: Cada mão trabalha independentemente
- 🎮 **Modo Challenge**: Sistema de desafios com pontuação e níveis
- 🎵 **Modo Free Play**: Toque livremente sem restrições
- 📊 **Estatísticas completas**: Score, accuracy, streaks e mais
- 🎨 **Interface visual rica**: Feedback colorido e animações
- 🏗️ **Arquitetura modular**: Código limpo e bem organizado

## 🎮 Modos de Jogo

### 🏆 Challenge Mode
- Desafios cronometrados
- Sistema de pontuação
- Níveis progressivos
- Tracking de accuracy e streaks
- Hits perfeitos (< 0.5s)

### 🎹 Free Play Mode
- Toque livremente
- Sem pressão de tempo
- Experimente diferentes notas
- Pratique seus gestos

**Alternar modos**: Pressione `M` durante o jogo

## 📁 Estrutura do Projeto

```
python-keys/
├── main.py                          # Entry point
├── config/                          # Configurações
│   ├── config.py                    # Config principal
│   ├── gesture_mappings.py          # Mapeamentos de gestos
│   └── sounds.py                    # Configurações de áudio
│
├── src/                             # Código fonte
│   ├── core/                        # Núcleo da aplicação
│   │   └── app.py                   # GestoSongs (classe principal)
│   │
│   ├── domain/                      # Lógica de negócio
│   │   ├── models.py                # Challenge, GameStats
│   │   └── interfaces.py            # Protocolos
│   │
│   ├── services/                    # Serviços
│   │   ├── camera_service.py
│   │   ├── sound_service.py
│   │   ├── gesture_service.py
│   │   └── hand_tracking_service.py
│   │
│   ├── game/                        # Lógica do jogo
│   │   └── challenge_manager.py
│   │
│   └── ui/                          # Interface
│       ├── renderer.py
│       ├── components/
│       └── styles.py
│
├── assets/                          # Recursos
│   └── sounds/
│       ├── notes/                   # Sons de notas
│       └── effects/                 # Efeitos sonoros
│
└── tests/                           # Testes
    ├── unit/
    └── integration/
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.12+
- Webcam
- Sistema operacional: Linux, macOS ou Windows

### Passos

1. **Clone o repositório**:
```bash
git clone https://github.com/jvras58/python-keys.git
cd python-keys
```

2. **Instale as dependências**:
```bash
# Usando uv (recomendado)
uv sync

# Ou usando pip
pip install -r requirements.txt
```

3. **Execute o aplicativo**:
```bash
# Usando uv
uv run python main.py

# Ou diretamente
python main.py
```

## 🎮 Como Jogar

### Gestos Básicos
Cada dedo que toca no polegar produz uma nota diferente:

**Mão Esquerda:**
- 👆 Indicador + Polegar = C4
- 🖕 Médio + Polegar = D4
- 💍 Anelar + Polegar = E4
- 🤙 Mindinho + Polegar = F4

**Mão Direita:**
- 👆 Indicador + Polegar = E4
- 🖕 Médio + Polegar = F4
- 💍 Anelar + Polegar = G4
- 🤙 Mindinho + Polegar = C#4

### Controles
- `M`: Alternar entre Challenge e Free Play
- `Q`: Sair do jogo

### Dicas
- Mantenha as mãos visíveis para a câmera
- Faça gestos claros e deliberados
- No modo Challenge, seja rápido para ganhar mais pontos
- Hits perfeitos (< 0.5s) valem mais pontos

## ⚙️ Configuração

### Personalizar Gestos
Edite `config/gesture_mappings.py` para customizar os mapeamentos de gestos:

```python
LEFT_HAND_GESTURES = {
    8: {"sound": "assets/sounds/notes/piano_c4.wav", "name": "C4"},
    # Adicione ou modifique gestos aqui
}
```

### Ajustar Volume
Modifique `config/sounds.py`:
```python
DEFAULT_VOLUME = 0.5  # 0.0 a 1.0
```

### Configurar Câmera
Ajuste `config/config.py`:
```python
"camera_index": 0,  # Mude se tiver múltiplas câmeras
```

## 🧪 Testes

Execute os testes:
```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/unit/test_models.py

# Com coverage
pytest --cov=src

# Verificar estrutura
uv run python scripts/verify.py 
```

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas:

- **Core**: Lógica principal da aplicação
- **Domain**: Modelos e regras de negócio
- **Services**: Serviços isolados (câmera, som, gestos)
- **Game**: Lógica específica do jogo
- **UI**: Renderização e componentes visuais

Esta estrutura facilita:
- ✅ Testes
- ✅ Manutenção
- ✅ Extensibilidade
- ✅ Compreensão do código

## 📊 Estatísticas do Jogo

O painel de estatísticas mostra:
- **Score**: Pontuação total
- **Level**: Nível atual (aumenta a cada 5 acertos)
- **Streak**: Sequência de acertos consecutivos
- **Accuracy**: Precisão geral (%)
- **Perfect Hits**: Hits com < 0.5s
- **Total Played**: Total de desafios jogados

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- [MediaPipe](https://google.github.io/mediapipe/) - Framework de ML
- [OpenCV](https://opencv.org/) - Processamento de imagem
- [Pygame](https://www.pygame.org/) - Sistema de áudio

## 📮 Contato

Jonathas Vinicius - [@jvras58](https://github.com/jvras58)

Link do Projeto: [https://github.com/jvras58/python-keys](https://github.com/jvras58/python-keys)


⭐ Se este projeto te ajudou, considere dar uma estrela!

#!/usr/bin/env python3
"""Script de verificação rápida."""

import sys
from pathlib import Path

def check_structure():
    """Verifica se a estrutura foi criada corretamente."""
    root = Path(__file__).parent.parent
    
    required_dirs = [
        "src",
        "src/core",
        "src/domain",
        "src/services",
        "src/game",
        "src/ui",
        "src/ui/components",
        "assets/sounds/notes",
        "tests/unit",
        "tests/integration",
        "config",
    ]
    
    required_files = [
        "src/core/app.py",
        "src/domain/models.py",
        "src/domain/interfaces.py",
        "src/services/camera_service.py",
        "src/services/sound_service.py",
        "src/services/gesture_service.py",
        "src/services/hand_tracking_service.py",
        "src/game/challenge_manager.py",
        "src/ui/renderer.py",
        "src/ui/styles.py",
        "src/ui/components/challenge_panel.py",
        "src/ui/components/stats_panel.py",
        "src/ui/components/gesture_guide.py",
        "src/ui/components/result_popup.py",
        "config/config.py",
        "config/gesture_mappings.py",
        "config/sounds.py",
        "tests/conftest.py",
    ]
    
    print("🔍 Verificando estrutura de diretórios...")
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = root / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)
            print(f"❌ Diretório faltando: {dir_path}")
        else:
            print(f"✅ {dir_path}")
    
    print("\n🔍 Verificando arquivos...")
    missing_files = []
    for file_path in required_files:
        full_path = root / file_path
        if not full_path.exists():
            missing_files.append(file_path)
            print(f"❌ Arquivo faltando: {file_path}")
        else:
            print(f"✅ {file_path}")
    
    print("\n🔍 Verificando arquivos de som...")
    sounds_dir = root / "assets/sounds/notes"
    sound_files = list(sounds_dir.glob("*.wav"))
    print(f"✅ {len(sound_files)} arquivos de som encontrados")
    
    print("\n" + "="*50)
    if missing_dirs or missing_files:
        print("❌ Verificação falhou!")
        print(f"Diretórios faltando: {len(missing_dirs)}")
        print(f"Arquivos faltando: {len(missing_files)}")
        return False
    else:
        print("✅ Verificação completa! Estrutura OK!")
        return True


def check_imports():
    """Verifica se os imports estão funcionando."""
    print("\n🔍 Verificando imports...")
    
    # Adiciona o diretório raiz ao path
    root = Path(__file__).parent.parent
    sys.path.insert(0, str(root))
    
    try:
        from config.config import CONFIG
        print("✅ config.config")
        
        from src.core.app import GestoSongs
        print("✅ src.core.app")
        
        from src.domain.models import Challenge, GameStats
        print("✅ src.domain.models")
        
        from src.services.sound_service import SoundService
        print("✅ src.services.sound_service")
        
        from src.services.gesture_service import GestureService
        print("✅ src.services.gesture_service")
        
        from src.game.challenge_manager import ChallengeManager
        print("✅ src.game.challenge_manager")
        
        from src.ui.renderer import UIRenderer
        print("✅ src.ui.renderer")
        
        print("\n✅ Todos os imports funcionando!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao importar: {e}")
        return False


if __name__ == "__main__":
    print("="*50)
    print("🚀 Verificação  - Gesto Songs")
    print("="*50 + "\n")
    
    structure_ok = check_structure()
    imports_ok = check_imports()
    
    print("\n" + "="*50)
    if structure_ok and imports_ok:
        print("🎉 SUCESSO! Tudo funcionando!")
        print("\n💡 Próximos passos:")
        print("  1. Execute: python main.py")
        print("  2. Execute: pytest")
        sys.exit(0)
    else:
        print("❌ Algo deu errado. Verifique os erros acima.")
        sys.exit(1)

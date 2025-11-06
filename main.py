import asyncio
import platform
import logging
from src.core.app import GestoSongs
from config.config import CONFIG

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Função assíncrona principal para compatibilidade com Pyodide."""
    app = GestoSongs()
    try:
        app.setup()
        while True:
            app.update_loop()
            await asyncio.sleep(1.0 / CONFIG["fps"])
    except SystemExit:
        pass
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
    finally:
        app.cleanup()


if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask

from api.routes.notes import notes_bp
from settings import API_HOST, API_PORT

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    level=logging.INFO,
    datefmt="%d/%m/%Y %X",
)

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(notes_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    logger.info(f"Starting Notes API on {API_HOST}:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT)

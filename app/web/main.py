from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os
import logging
from logging.handlers import RotatingFileHandler

from app.web.routes.auth import auth_bp
from app.web.routes.main import main_bp
from app.web.routes.history import history_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
app.config["WTF_CSRF_ENABLED"] = True

csrf = CSRFProtect()
csrf.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(history_bp, url_prefix="/history")

# Логирование
if not app.debug:
    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler("logs/flask.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s"
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Flask app startup")


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
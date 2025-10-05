from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    """Application factory to create Flask app with routes registered."""
    app = Flask(__name__)

    # Allow CORS for local testing / front-end integration
    CORS(app)

    # ---------- Blueprints ---------- #
    from .routes import hskg_bp  # noqa: WPS433 (late import to avoid circular)

    app.register_blueprint(hskg_bp)

    # ---------- Health-check ---------- #
    @app.route("/ping")
    def _ping():  # pragma: no cover
        return {"status": "ok"}

    return app

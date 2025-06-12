from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Flask's flash is dependent on this
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'WOW_this_key_is_so_secret')

    # Import blueprints per "location"
    from .inventory import inventory_bp
    from .projects import projects_bp
    from .statistics import statistics_bp
    from .main import main_bp

    # Register the blueprints to flask
    app.register_blueprint(main_bp)
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(statistics_bp, url_prefix='/statistics')

    return app
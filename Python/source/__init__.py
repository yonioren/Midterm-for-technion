from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecret'

    from .inventory import inventory_bp
    from .projects import projects_bp
    from .statistics import statistics_bp
    from .main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(statistics_bp, url_prefix='/statistics')

    return app

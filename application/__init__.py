from flask import Flask
from flask_bootstrap import Bootstrap
from werkzeug.debug import DebuggedApplication


# Globally accessible libraries
#db = SQLAlchemy()
#r = FlaskRedis()
bootstrap = Bootstrap()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, static_url_path='/', instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    #db.init_app(app)
    #r.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        # Include routes
        from . import routes

        # Globally accessible context variables
        from .modules.branchname import branchname
        dict(branchname=branchname())

        return app

from flask import Flask, send_from_directory, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babel import Babel
# from flask_meld import Meld
from flask_admin.contrib.fileadmin import FileAdmin
from flask_bootstrap import Bootstrap5
from views import HomeView
from forms import DropzoneForm, CKTextAreaField
from oryx_api import create_srs_admin_blueprint
from models import db, Upload
from plugins import Plugins 
from werkzeug.middleware.proxy_fix import ProxyFix
from utils import build_sample_db, handle_form_data

# from config import Config
import os.path as op
import os

bs = Bootstrap5()
babel = Babel()
# meld = Meld()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    dirs = ['static', 'files', 'uploads', 'files/videos']    

    # Create directory for file fields to use
    for dire in dirs:
        file_path = op.join(op.dirname(__file__), dire)
        try:
            os.mkdir(file_path)
        except OSError:
            pass
            
    # app.config.from_object(config_class)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'
    app.config['SECRET_KEY'] = '134975049820347'
    app.config['DATABASE_FILE'] = 'admin.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['FILE_PATH'] = op.join(op.dirname(__file__), 'files')
    app.config['UPLOAD_PATH'] = op.join(op.dirname(__file__), 'uploads')
    app.config['VIDEO_PATH'] = op.join(op.dirname(__file__), 'files/videos')
    app.config['APP_USERNAME'] = os.environ.get('APP_USERNAME')

    app.config['SRS_API_URL'] = 'http://live.savantlab.org:1985'
    app.config['SRS_USERNAME'] = 'admin'
    app.config['SRS_PASSWORD'] = 'admin'

    # Create and register blueprints
    oryx_api = create_srs_admin_blueprint(
        app.config['SRS_API_URL'],
        app.config['SRS_USERNAME'],
        app.config['SRS_PASSWORD']
    )
    
    app.register_blueprint(oryx_api)
    
    # Initialize extensions
    db.init_app(app)
    bs.init_app(app)
    babel.init_app(app)
    # meld.init_app(app)
    Plugins.load_plugins()
    
    # Apply ProxyFix middleware for proper handling of proxy headers
    # app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Add admin views
    from views import HomeView
    admin = Admin(app, '', url='/admin', index_view=HomeView(), base_template='admin/base.html', template_mode='bootstrap5')
    path = op.join(op.dirname(__file__), 'uploads')
    admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))
    return app


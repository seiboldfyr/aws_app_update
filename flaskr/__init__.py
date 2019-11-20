import os
from logging.config import dictConfig

from flask import Flask
from flaskr.blueprint import base_blueprint
from flaskr.framework.model.Io.xlsx_file import XLSXFile
from flaskr import db
from . import framework

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'filename': 'system.log',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=None)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'upload'),
        VERSION='2.3',
        DB_HOST='localhost',
        DB_NAME='FyrDatabase',
        DB_PORT=27017,
        APP_USER='test',
        APP_PASSWORD='test'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # we need several try catch, because each folder it tries to create, it could throw the OSError exception
    # in case folder already exists
    # create the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # create the upload folder
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    # create specific folders
    try:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], XLSXFile.FOLDER))
    except OSError:
        pass

    db.init_app(app)
    framework.init_framework(app)

    app.register_blueprint(base_blueprint)

    return app
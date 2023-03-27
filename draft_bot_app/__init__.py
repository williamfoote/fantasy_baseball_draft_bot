from flask import Flask

app = Flask(__name__)


if app.config['ENV'] == 'production':
    app.config.from_object('config.productionConfig')
elif app.config['ENV'] == 'testing':
    app.config.from_object('config.testingConfig')
else:  
    app.config.from_object('config.developmentConfig')

from draft_bot_app.routes import base_views
from draft_bot_app.routes import functional_views
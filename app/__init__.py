import operator
import os
import uuid
from hashlib import sha512

from flask import Flask, session, request
from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
#from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_jwt_extended import JWTManager
from flask_login._compat import text_type
from flask_recaptcha import ReCaptcha
from flask_rq import RQ
from flask_session import Session
from flask_share import Share
from flask_uploads import UploadSet, configure_uploads, IMAGES

from flask_whooshee import Whooshee
from app.utils import db, login_manager, get_cart, image_size, json_load

from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
csrf = CSRFProtect()
compress = Compress()
images = UploadSet('images', IMAGES)
docs = UploadSet('docs', ('rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'pdf'))
share = Share()
moment = Moment()
jwt = JWTManager()
sess = Session()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'

# import app.models as models

whooshee = Whooshee()
recaptcha = ReCaptcha()

def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    Config[config_name].init_app(app)

    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)
    configure_uploads(app, images)
    configure_uploads(app, docs)
    CKEditor(app)
    share.init_app(app)
    moment.init_app(app)
    jwt.init_app(app)
    sess.init_app(app)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .booking import booking as booking_blueprint
    app.register_blueprint(booking_blueprint, url_prefix='/booking')
    
    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint, url_prefix='/search')
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/dashboard')

    from .payment import payment as payment_blueprint
    app.register_blueprint(payment_blueprint, url_prefix='/payment')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    from .notification import notification as notification_blueprint
    app.register_blueprint(notification_blueprint)

    #from .search import search as search_blueprint
    #app.register_blueprint(search_blueprint)

    from .invite import invite as invite_blueprint
    app.register_blueprint(invite_blueprint)
    
    from .public import public as public_blueprint
    app.register_blueprint(public_blueprint)

    @app.before_request
    def before_request():
        try:
            session['cart_id']
        except:
            u = uuid.uuid4()
            user_agent = request.headers.get('User-Agent')
            if user_agent is not None:
                user_agent = user_agent.encode('utf-8')
            base = 'cart: {0}|{1}|{2}'.format(_get_remote_addr(), user_agent, u)
            if str is bytes:
                base = text_type(base, 'utf-8', errors='replace')  # pragma: no cover
            h = sha512()
            h.update(base.encode('utf8'))
            session['cart_id'] = h.hexdigest()

    @app.cli.command()
    def reindex():
        with app.app_context():
            whooshee.reindex()

    @app.cli.command()
    def routes():
        rules = []
        for rule in app.url_map.iter_rules():
            subdomain = "no subdomain" if not rule.subdomain else rule.subdomain
            methods = ','.join(sorted(rule.methods))
            rules.append((rule.endpoint, methods, str(rule), subdomain))

        sort_by_rule = operator.itemgetter(2)
        for endpoint, methods, rule, subdomain in sorted(rules, key=sort_by_rule):
            route = '{:25s} {:60s} {:25s} {}'.format(subdomain, endpoint, methods, rule)
            print(route)

    whooshee.init_app(app)
    recaptcha.init_app(app)

    return app

# encoding=utf-8

import os
import time

from redis import Redis

from flask import Flask, request, g
from flaskext.assets import Environment, Bundle


app = Flask(__name__)
app.config.from_object('gummiognina.config.%s' % os.environ.get('GUMMIOGNINA_CONFIG', 'production'))


assets = Environment(app)
assets.register('js', Bundle(
    
    'lib/modernizer-2.0.6.js',
    'lib/jquery-1.6.1.js', 
    'lib/jquery.appear.js', 
    'lib/underscore.js', 
    'lib/backbone.js', 
    'js/gummiognina.js', 
    
    # filters='jsmin', 
    output='gen/gummiognina.js'))

#if not app.debug:
#    from .loggers import configure_logging
#    configure_logging(app)


from gummiognina import helpers

@app.template_filter()
def timesince(value):
    return helpers.timesince(value)
    
@app.template_filter()
def linebreaks(value):
    return helpers.linebreaks(value)


@app.before_request
def connect_services():
    g.redis = Redis(host='localhost', port=6379, db=0)

@app.before_request
def set_globals():
    g.instagram_id = "32cfd6227bdb4cabaa95ca6d48aa9b10"
    g.instagram_secret = "7d0b75b60b4d4ab392c90c0e3ba61662"

try:
    def file_string(path):
        return ''.join(file(path).read().splitlines()).strip()
    STATIC_VERSION = file_string(os.path.join(os.path.dirname(__file__), 'deploy'))
except IOError, e:
    STATIC_VERSION = ''


@app.context_processor
def template_context():
    from .views import get_photos
    photos, max_tag_id = get_photos()
    js_namespace = {
        'STATIC_URL': url_for('static', filename="", _external=True),
        'photos': list(photos),
        'max_tag_id': max_tag_id
    }
    return dict(
        revision=STATIC_VERSION, 
        js_namespace=js_namespace)


from gummiognina.models import Photo
from gummiognina.extensions import db
db.init_app(app)

from gummiognina.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5052, debug=True)


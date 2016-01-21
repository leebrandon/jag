from flask import Flask
from flask.ext.thumbnails import Thumbnail
from flask_bootstrap import Bootstrap
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

app.config['MEDIA_FOLDER'] = '/Users/blee/workspace/blee/jinja1/media'
app.config['MEDIA_URL'] = '/media/'

thumb = Thumbnail(app)
Bootstrap(app)

from app import views
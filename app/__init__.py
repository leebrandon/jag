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

app.config.from_pyfile("settings.cfg")
app.config['MEDIA_FOLDER'] = '/home/blee/workspace/blee/jag/media'
app.config['MEDIA_URL'] = '/home/blee/workspace/media/'

thumb = Thumbnail(app)
Bootstrap(app)

from app import views

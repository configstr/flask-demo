from flask import Flask
from . import config

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello {}!'.format(config.WHERE)

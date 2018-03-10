from flask import Flask
from flask import send_from_directory, jsonify
from .. import get_template

import glob
import os.path
import yaml

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')


@app.route('/templates')
def templates():
    """List the name and descriptors of every available template."""
    def get_name(path):
        parts = os.path\
            .relpath(path, '../templates')\
            .split(os.sep)
        parts[-1] = parts[-1].replace('.yml', '')

        return '.'.join(parts)

    paths = glob.glob('../templates/**/*.yml')
    names = map(get_name, paths)

    return jsonify({name: get_template(name)[0] for name in names})


@app.route('/saves')
def saves():
    """List the name and content of every saved diffusion."""
    def get_name(path):
        return os.path.split(path)[1].replace('.yml', '')

    def get_content(path):
        with open(path) as file:
            return yaml.load(file)

    paths = glob.glob('storage/*.yml')
    return jsonify({get_name(path): get_content(path) for path in paths})

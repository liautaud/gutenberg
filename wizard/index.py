from flask import Flask
from flask import request
from flask import send_from_directory
from flask import jsonify

from gutenberg import parse, render, get_template

import glob
import os.path
import yaml
import time
import uuid

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


@app.route('/render', methods=['POST'])
def preview():
    """Display a HTML rendering for a given source."""
    try:
        data = parse(request.json)
        _, source_relpath = get_template(data['template'])
        return render(source_relpath, data)
    except Exception as e:
        return "Une erreur s'est produite durant le rendu " +\
               "de la diffusion :\n%s" % e


@app.route('/save', methods=['POST'])
def save():
    """Saves a given diffusion given its content."""
    data = request.json
    name = request.args.get('name')

    if name is None:
        when = time.strftime("%Y-%m-%d-%H%M%S")
        name = when + '-' + str(uuid.uuid1())

    with open(os.path.join('storage', name + '.yml'), 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
        return jsonify({'name': name})

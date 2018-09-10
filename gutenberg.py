import argparse
import yaml
import os.path
import jinja2

from fields import FIELD_TYPES, FIELD_CASTS

META_FIELDS = [
    {'id': 'title', 'name': "Nom de la diffusion", 'type': 'text'},
    {'id': 'author', 'name': "Nom de l'auteurice", 'type': 'text'},
    {'id': 'date', 'name': "Date de la diffusion", 'type': 'date'}]


class DescriptorError(Exception):
    """An error when parsing a template descriptor."""
    pass


class DataError(Exception):
    """An error when parsing template data."""
    pass


def main():
    """Entrypoint for the `gutenberg` command-line utility."""
    parser = argparse.ArgumentParser(
        description='Génère des diffusions au format HTML.')

    parser.add_argument('source', type=open,
                        help='La chemin du fichier YAML de description.')
    parser.add_argument('target', type=str,
                        help='Le chemin du fichier HTML à générer.')

    args = parser.parse_args()
    data = yaml.load(args.source)

    descriptor, source_relpath = get_template(data['template'])
    validate_and_cast_data(data, descriptor)
    output = render(source_relpath, data)

    with open(args.target, 'w') as target:
        target.write(output)


def get_template(template_name):
    """
    Return the (descriptor, source_relpath) tuple for a given
    template name (e.g. `enscene.ensortie`).
    """
    base_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')

    parts = template_name.split('.')
    desc_dir = os.path.join(templates_dir, *parts[:-1])
    desc_file = parts[-1] + '.yml'
    desc_path = os.path.join(desc_dir, desc_file)

    with open(desc_path) as desc_file:
        desc = yaml.load(desc_file)
        desc['id'] = template_name

    source_path = os.path.join(desc_dir, desc['source'])
    source_relpath = os.path.relpath(source_path, templates_dir)

    return (desc, source_relpath)


def validate_descriptor(descriptor):
    """Validate some template descriptor."""
    if 'title' not in descriptor:
        raise DescriptorError(
            "Le descripteur doit contenir un titre (champ `title`).")

    if 'source' not in descriptor:
        raise DescriptorError(
            "Le descripteur doit contenir un chemin vers la source "
            "HTML du template (champ `source`).")

    if 'root' not in descriptor:
        raise DescriptorError(
            "Le descripteur doit contenir une définition de racine "
            "(champ `root`).")

    if 'sections' not in descriptor:
        raise DescriptorError(
            "Le descripteur doit contenir une définition de section "
            "(champ `sections`).")

    def validate_item(item):
        if 'id' not in item:
            raise DescriptorError(
                "Chaque élément déclaré dans le descripteur doit avoir un "
                "identifiant (champ `id`).")

        if 'name' not in item:
            raise DescriptorError(
                "L'élément d'identifiant %s déclaré dans le descripteur doit "
                "avoir un nom d'affichage (champ `name`)." % (item['id']))

        if 'type' not in item:
            raise DescriptorError(
                "L'élément d'identifiant %s déclaré dans le descripteur doit "
                "avoir un type (champ `type`). Valeurs possibles : %s." %
                (item['id'], FIELD_TYPES.join(', ')))

    for item in descriptor['root']:
        validate_item(item)

    for item in descriptor['sections']:
        validate_item(item)


def validate_and_cast_item(container, item_id, item_desc):
    """Validate and cast some item according to its descriptor."""
    required = 'required' in item_desc and item_desc['required']

    if item_id not in container and required:
        raise DataError("L'élément `%s` est manquant." % (item_desc['name']))

    if item_id in container:
        cast = FIELD_CASTS[item_desc['type']]
        container[item_id] = cast(container[item_id], item_desc)


def validate_and_cast_data(data, desc):
    """Validate and cast the input data according to its descriptor."""
    for item_desc in desc['root'] + META_FIELDS:
        validate_and_cast_item(data, item_desc['id'], item_desc)

    if 'sections' in data:
        for (section, item_desc) in zip(data['sections'], desc['sections']):
            validate_and_cast_item(section, item_desc['id'], item_desc)


def render(path, variables={}):
    """Render the given template using the given variables."""
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('gutenberg'),
        trim_blocks=True,
        lstrip_blocks=True)

    template = env.get_template(path)
    return template.render(variables)

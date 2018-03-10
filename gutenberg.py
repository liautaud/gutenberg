import argparse
import yaml
import dateutil.parser
import markdown
import os.path
import jinja2


def main():
    """Entrypoint for the `gutenberg` command-line utility."""
    parser = argparse.ArgumentParser(
        description='Génère des diffusions au format HTML.')

    parser.add_argument('source', type=open,
                        help='La chemin du fichier YAML de description.')
    parser.add_argument('target', type=str,
                        help='Le chemin du fichier HTML à générer.')

    args = parser.parse_args()
    parsed = parse(args.source)

    descriptor, source_relpath = get_template(args.source['template'])
    output = render(source_relpath, parsed)

    with open(args.target, 'w') as target:
        target.write(output)


def get_template(template_name):
    """
    Return the (descriptor, source_relpath) tuple for a given
    template name (e.g. `enscene.ensortie`).
    """
    parts = template_name.split('.')
    desc_folder = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'templates',
        *parts[:-1])
    desc_file = parts[-1] + '.yml'
    desc_path = os.path.join(desc_folder, desc_file)

    with open(desc_path) as desc_file:
        desc = yaml.load(desc_file)

    source_path = os.path.join(desc_folder, desc['source'])
    source_relpath = os.path.relpath(source_path, 'templates')

    return (desc, source_relpath)


def parse(source):
    """Parse and validate the input YAML file."""
    data = yaml.load(source)

    # Conversion functions.
    date = dateutil.parser.parse

    def strip(s):
        start = s.find('>') + 1
        end = len(s) - s[::-1].find('<') - 1

        return s[start:end]

    def mark(text):
        md = markdown.Markdown()
        return md.convert(text)

    def paragraphs(text):
        return [strip(mark(s)) for s in text.splitlines()]

    # TODO(liautaud):
    # Remove the previous validation routine, and replace it with
    # data from the new template description files.

    # Validate the YAML schema.
    required(data, 'author')
    required(data, 'title')
    required(data, 'date', date)
    required(data, 'template')
    optional(data, 'greeting')
    optional(data, 'introduction', mark)
    required(data, 'sections.title')
    optional(data, 'sections.color')
    optional(data, 'sections.image')
    optional(data, 'sections.align', ('left', 'right'))
    optional(data, 'sections.date')
    optional(data, 'sections.place')
    required(data, 'sections.content', mark)
    optional(data, 'sections.appendices.*', paragraphs)
    optional(data, 'closing')

    # Return the converted data.
    return data


def required(data, name, cast=str):
    return optional(data, name, cast, True)


def optional(data, name, cast=str, required=False):
    """
    Check whether `data` contains the field `name`, and cast
    the field using a given function if necessary.
    """
    parts = name.split('.', 1)
    name = parts[0]

    if name not in data:
        if required and not len(parts) > 1:
            raise Exception(
                'Le champ %s est manquant' % (name))
        else:
            return None

    value = data[name]

    if len(parts) > 1:
        if parts[1] == '*':
            data[name] = list(map(cast, value))
        else:
            for entry in value:
                optional(entry, parts[1], cast, required)

        return None

    if isinstance(cast, tuple):
        if value not in cast:
            raise Exception(
                'Le champ %s doit contenir %s (trouvé %s)' %
                (name, ' ou '.join(cast), value))

    data[name] = cast(value)

    return None


def render(path, variables={}):
    """Render the given template using the given variables."""
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('gutenberg'),
        trim_blocks=True,
        lstrip_blocks=True)

    template = env.get_template(path)
    return template.render(variables)

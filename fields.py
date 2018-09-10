import re
import markdown
import collections
import dateutil.parser

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def parse_text(t, desc):
    """Check that a given value is some text."""
    return t


def parse_color(c, desc):
    """Check that a given value is a color."""
    return c


def parse_choice(c, desc):
    """Check that a given value is one of a few."""
    from gutenberg import DescriptorError, DataError

    if 'choices' not in desc:
        raise DescriptorError(
            "L'élément %s est de type `choice`, il doit donc être accompagné "
            "d'une liste de `choices`." % (desc['name']))
    if c not in desc['choices']:
        raise DataError(
            "L'élément %s ne peut pas contenir la valeur `%s`. Valeurs "
            "possibles : %s." % (desc['name'], c, ', '.join(desc['choices'])))

    return c


def parse_image(url, desc):
    """Check that a given value is an image URL."""
    from gutenberg import DataError

    if re.match(URL_REGEX, url) is None:
        raise DataError(
            "L'élément %s est de type `image`, il doit donc contenir une URL. "
            "%s n'est pas une URL valide." % (desc['name'], url))

    return url


def parse_list(l, desc):
    """Check that a given value is a list with items of a given type."""
    from gutenberg import DescriptorError, DataError

    if 'items' not in desc:
        raise DescriptorError(
            "L'élément %s est de type `list`, il doit donc être accompagné "
            "d'un type pour ses `items`." % (desc['name']))
    elif desc['items'] not in FIELD_TYPES:
        raise DescriptorError(
            "L'élement %s a un type d'item invalide `%s`. Valeurs possibles : "
            "%s." % (desc['name'], desc['choices'], ', '.join(FIELD_TYPES)))
    elif not isinstance(l, collections.Iterable):
        raise DataError(
            "L'élément %s est de type `list`, mais la valeur `%s` n'est "
            "pas itérable." % (desc['name'], l))

    cast = FIELD_CASTS[desc['items']]

    # Generate a "fake" descriptor for the list item, so that
    # we can pass it to the parsing function.
    def item_desc(index):
        return {'id': '%s[%d]' % (desc['id'], index),
                'name': 'Élément de `%s`' % desc['name'],
                'type': desc['items']}

    return [cast(item, item_desc(i)) for i, item in enumerate(l)]


def parse_date(d, desc):
    """Check that a given value is a valid date and converts it."""
    from gutenberg import DataError

    try:
        return dateutil.parser.parse(d)
    except ValueError:
        raise DataError(
            "L'élément %s est de type `date`, il doit donc contenir une "
            "date valide. %s n'est pas une date valide." % (desc['name'], d))


def parse_datetime(d, desc):
    """Check that a given value is a valid timestamp and converts it."""
    from gutenberg import DataError

    try:
        return dateutil.parser.parse(d)
    except ValueError:
        raise DataError(
            "L'élément %s est de type `datetime`, il doit donc contenir un "
            "timestamp valide. %s n'est pas un timestamp valide."
            % (desc['name'], d))


def parse_markdown(m, desc):
    """Parse Markdown-formatted text into HTML."""
    parser = markdown.Markdown()
    return parser.convert(m)


def parse_paragraphs(m, desc):
    """Parse Markdown-formatted paragraphs into a list of HTML paragraphs."""
    def strip(s):
        start = s.find('>') + 1
        end = len(s) - s[::-1].find('<') - 1

        return s[start:end]

    return [strip(parse_markdown(s)) for s in m.splitlines()]


FIELD_TYPES = [
    'text', 'color', 'choice', 'image', 'list',
    'date', 'datetime', 'markdown', 'paragraphs']

FIELD_CASTS = {k: globals()['parse_' + k] for k in FIELD_TYPES}

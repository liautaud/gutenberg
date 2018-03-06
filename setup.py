from setuptools import setup, find_packages

setup(
    name='gutenberg',
    version='1.0.0',
    description='Un générateur automatique de diffusions.',
    url='https://github.com/liautaud/gutenberg',

    author='Romain Liautaud',
    author_email='romain@liautaud.fr',
    license='MIT',

    packages=find_packages(exclude=['tests', 'wizard']),
    install_requires=[
        'pyyaml',
        'python-dateutil',
        'markdown',
        'jinja2',
    ],

    entry_points={
        'console_scripts': [
            'gutenberg=gutenberg:main',
        ],
    })


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import dematic

config = {
    'description': 'Dematic MultiShuttle Monitoring ',
    'author': 'FabrizioMargaroli',
    'version': dematic.__version__,
    'download_url': 'Where to download it.',
    'url': '',
    'author_email': '',
    'install_requires': ['bottle'],
    'packages': ['dematic'],
    'scripts': [],
    'name': 'Dematic',
    'long_description': open('README.md').read(),
    'package_data': {
        'dematic': ['views/*.tpl'],
       },
        'include_package_data': True
}

setup(**config)
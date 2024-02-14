# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kitstandard']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['kitstandard = kitstandard.cli:cli']}

setup_kwargs = {
    'name': 'kitstandard',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Michael Verhulst',
    'author_email': 'michael@terminallabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

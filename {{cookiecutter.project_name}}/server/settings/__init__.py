"""
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

import logging
from os import environ
from pprint import pformat

logger = logging.getLogger('server.settings')

# Managing environment via DJANGO_ENV variable:
environ.setdefault('DJANGO_ENV', 'development')
ENV = environ['DJANGO_ENV']

from .components import env, PROJECT_ROOT, SOURCE_FOLDER, SETTINGS_FOLDER  # noqa
from .components.common import *                                           # noqa
from .components.logging import *                                          # noqa
from .components.csp import *                                              # noqa
from .components.caches import *                                           # noqa

# Load settings overrides from environment module
try:
    environment_file = (
        SETTINGS_FOLDER / 'environments' / f'{ENV}.py'
    ).resolve(strict=True)

    with environment_file.open('rb') as ef:
        exec(compile(ef.read(), str(environment_file), 'exec'), globals())
    logger.debug('Settings for environment "%s" was loaded. File: %s',
                 ENV, environment_file)
except FileNotFoundError:
    logger.warning('Environment module for DJANGO_ENV="%s" was not found!', ENV)


# Optional local environment overrides
try:
    from .environments.local import *  # noqa
except ModuleNotFoundError:
    pass

logger.debug(pformat(env.dump()))

import os

env = os.environ.get('ENVIRONMENT', 'ENV')


class ConfigurationNotFound(Exception):
    pass


if env == 'ENV':
    from .settings_env import *
else:
    raise ConfigurationNotFound()
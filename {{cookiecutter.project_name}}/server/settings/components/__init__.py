from pathlib import PurePath

from environs import Env

SETTINGS_FOLDER = PurePath(__file__).parents[1]
SOURCE_FOLDER = SETTINGS_FOLDER.parent
PROJECT_ROOT = SOURCE_FOLDER.parent

env = Env()
try:
    env.read_env(PROJECT_ROOT / 'config')
except FileNotFoundError:
    pass

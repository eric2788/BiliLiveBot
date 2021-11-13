
from os import listdir
from os.path import isfile, join
import importlib, inspect
from plugin import BotPlugin
import logging

PLUGINS_DIR = 'plugins'

def load_plugins():
    plugins = [f[:-3] for f in listdir(PLUGINS_DIR) if isfile(join(PLUGINS_DIR, f)) and f.endswith('.py')]
    bot_plugins = []
    for plugin in plugins:
        module = importlib.import_module(f'plugins.{plugin}')
        for (name, cs) in inspect.getmembers(module, inspect.isclass):
            if cs.__base__ == BotPlugin:
                logging.info(f'正在加載插件 {plugin} ({name})')
                bot_plugins.append(cs())
                break
    return bot_plugins
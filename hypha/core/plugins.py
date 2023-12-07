from hypha.core.logging import *
from enum import Enum
import importlib
import os

plugins = []

def importPlugins():
    if (not os.path.isdir("plugins")): return

    log("Loading plugins...")
    for module in os.listdir("plugins"):
        if (not module.startswith("-")):
            __import__("plugins." + module, locals(), globals())

def registerPlugin(pluginObj):
    if (pluginObj not in plugins):
        pluginObj.onRegister()
        plugins.append(pluginObj)
        return True
    return False

def executeHook(hook, *args):
    for plugin in plugins:
        if (hook not in plugin.hooks):
            continue
        plugin.hooks[hook](args)

def executeOverwriteHook(hook, initialVal, *args):
    res = initialVal
    for plugin in plugins:
        if (hook not in plugin.hooks):
            continue
        res = plugin.hooks[hook](res, *args)
    return res

def executeAdditiveHook(hook, initialVal, *args, isArray=False):
    res = initialVal
    for plugin in plugins:
        if (hook not in plugin.hooks):
            continue
        if (not isArray):
            res += plugin.hooks[hook](res, *args)
        else:
            res.append(plugin.hooks[hook](res, *args))
    return res

class Hooks(Enum):
    PAGE_CSS_RENDER = 0
    PAGE_HEAD_RENDER = 1

class Plugin(object):

    def __init__(self):
        self.hooks = {}
        self.onInit()

    def onInit(self):
        pass

    def onRegister(self):
        pass

    def registerHook(self, hook, hookFunction):
        self.hooks[hook] = hookFunction

    def init(self):
        pass
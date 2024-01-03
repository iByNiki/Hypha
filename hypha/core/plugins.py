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

    deps = []
    loaded = []
    for plugin in plugins:
        if (hasattr(plugin, "DEPENDENCIES")):
            for dep in plugin.DEPENDENCIES:
                deps.append([plugin.NAME, dep])
        loaded.append(plugin.NAME)
    
    for dep in deps:
        if (dep[1] not in loaded):
            error("The plugin " + dep[0] + " requires " + dep[1])
            os._exit(1)

    for plugin in plugins:
        if (hasattr(plugin, "onPostRegister")):
            plugin.onPostRegister()

def registerPlugin(pluginObj):
    if (pluginObj not in plugins):
        if (hasattr(pluginObj, "onRegister")): pluginObj.onRegister()
        plugins.append(pluginObj)
        log("Loaded Plugin: " + pluginObj.NAME)
        return True
    return False

def getByName(name):
    for plugin in plugins:
        if (plugin.NAME == name):
            return plugin
    return None

def executeHook(hook, *args):
    for plugin in plugins:
        if (hook not in plugin.hooks):
            continue

        if (len(args) == 0):
            plugin.hooks[hook]()
        else:
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
    PAGE_BODY_RENDER = 2
    PAGE_JS_RENDER_BUNDLED = 3
    PAGE_JS_RENDER_NONBUNDLED = 4
    PAGE_FULL_RENDER = 5
    RENDER_START = 6

class Plugin(object):

    def __init__(self):
        self.hooks = {}
        self.init()

    def init(self):
        pass

    def onRegister(self):
        pass

    def registerHook(self, hook, hookFunction):
        self.hooks[hook] = hookFunction

    def init(self):
        pass
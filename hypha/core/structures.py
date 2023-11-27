from enum import Enum

class Component(object):
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.css = ""
        self.config = {}
        self.requiredComponents = []
        self.attributes = [] # {"name": "data"}
        self.scripts = []

class Page(object):
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.css = ""
        self.config = {}
        self.layout = None
        self.requiredComponents = []
        self.scripts = []

class Layout(object):
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.css = ""
        self.config = {}
        self.requiredComponents = []
        self.scripts = []

class JSLang(Enum):
    VANILLA = []
    #TYPESCRIPT = ["ts", "typescript"]
    COFFEE = ["coffee", "coffeescript", "cs"]
    BABEL = ["babel", "babeljs", "b"]

class Script(object):
    def __init__(self, lang=JSLang.VANILLA, code="", defer=False, bundle=True, requires=[]):
        self.defer = defer
        self.lang = lang
        self.code = code
        self.bundle = bundle
        self.requires = requires
    def getLangDeps(self):
        dep = []
        #if (self.lang == JSLang.TYPESCRIPT):
            #dep.append("dep/system.js")
        if (self.lang == JSLang.BABEL):
            dep.append("dep/babel-polyfill.js")

        for require in self.requires:
            if (not require.endswith(".js")):
                require += ".js"
            dep.append("scripts/" + require)

        return dep
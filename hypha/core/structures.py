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
    TYPESCRIPT = ["ts", "typescript"]
    COFFEE = ["coffee", "coffeescript", "cs"]
    BABEL = ["babel", "babeljs", "b"]

class Script(object):
    def __init__(self, lang=JSLang.VANILLA, code="", defer=False):
        self.defer = defer
        self.lang = lang
        self.code = code
class Component(object):
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.css = ""
        self.config = {}
        self.requiredComponents = []
        self.attributes = [] # {"name": "data"}

class Page(object):
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.css = ""
        self.config = {}
        self.layout = None
        self.requiredComponents = []

class Layout(object):
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.css = ""
        self.config = {}
        self.requiredComponents = []
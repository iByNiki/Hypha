from enum import Enum
from collections.abc import MutableSequence
import dukpy

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
    
    def getCompiledCode(self):
        if (self.lang == JSLang.VANILLA):
            return self.code
        elif (self.lang == JSLang.COFFEE):
            return dukpy.coffee_compile(self.code)
        elif (self.lang == JSLang.BABEL):
            return dukpy.babel_compile(self.code)["code"]
        
        return self.code


class HTMLAttribute(object):
    def __init__(self, name: str, value, noValue=False):
        self.name = name
        self.value = str(value)
        self.noValue = noValue
    def __str__(self):
        if (self.noValue):
            return self.name
        
        return self.name + '="' + self.value + '"'

class HTMLElement(object):
    def __init__(self, type: str, innerHTML: str="", attribs: MutableSequence[HTMLAttribute]=[], endTag=True):
        self.type = type.lower()
        self.innerHTML = innerHTML

        if (attribs == []):
            self.attribs: MutableSequence[HTMLAttribute] = []
        else:
            self.attribs = attribs

        self.children = []

        self.endTag = endTag

    def addChild(self, child):
        self.children.append(child)
    
    def addAttrib(self, attrib):
        self.attribs.append(attrib)

    def getFullInnerHTML(self):
        return "".join([str(child) for child in self.children]) + self.innerHTML

    def __str__(self):
        return "<" + self.type + (" " if len(self.attribs) > 0 else "") + " ".join([str(attrib) for attrib in self.attribs]) + ">" + self.getFullInnerHTML() + ("</" + self.type + ">" if self.endTag else "")
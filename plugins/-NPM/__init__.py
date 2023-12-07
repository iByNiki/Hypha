import hypha.core.plugins as plugins
from hypha.core.structures import *

class NPM(plugins.Plugin):
    def init(self):
        self.NAME = "NPM"

        self.APIURL = "https://cdn.jsdelivr.net/npm/"
        self.modules = {}

    def onRegister(self):
        self.registerHook(plugins.Hooks.PAGE_HEAD_RENDER, self.onPageHeadRender)

    def addModule(self, moduleName, version="latest"):
        if (moduleName not in self.modules):
            self.modules[moduleName] = version
    
    def onPageHeadRender(self, pageHead, page):

        for module in self.modules:
            moduleUrl = self.APIURL + module + ("@" + self.modules[module] if self.modules[module] != "latest" else "")
            moduleElem = HTMLElement("script", attribs=[
                HTMLAttribute("src", moduleUrl)
            ])
            pageHead.addChild(moduleElem)

        return pageHead

plugins.registerPlugin(NPM())
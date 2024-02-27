import hypha.core.plugins as plugins
from hypha.core.structures import *
from hypha.core.logging import *
import requests
import os
import shutil

class NPM(plugins.Plugin):
    def __init__(self):
        super().__init__()
        
        self.NAME = "NPM"

        self.APIURL = "https://cdn.jsdelivr.net/npm/"
        self.FOLDERPATH = "tmp/public/npm/"
        self.PUBLICPATH = "/npm/"
        self.modules = {}

    def onRegister(self):
        self.registerHook(plugins.Hooks.PAGE_HEAD_RENDER, self.onPageHeadRender)
        self.registerHook(plugins.Hooks.RENDER_START, self.onRenderStart)

    def addModule(self, moduleName: str):
        if (moduleName not in self.modules):
            self.modules[moduleName] = ""
    
    def onRenderStart(self):
        for module in self.modules:
            self.modules[module] = ""

    def onPageHeadRender(self, pageHead, page):
        for module in self.modules:
            if (self.modules[module] == ""):

                if (not os.path.isdir(self.FOLDERPATH)): os.makedirs(self.FOLDERPATH)
                scriptName = module.split("/")[-1].split("@")[0] + (".js" if not module.endswith(".js") else "")

                if (os.path.isfile(self.FOLDERPATH.replace("tmp/", "build/") + scriptName)):
                    shutil.copy(self.FOLDERPATH.replace("tmp/", "build/") + scriptName, self.FOLDERPATH + scriptName)
                    self.modules[module] = scriptName
                    log("Copied " + module + " from previous build")

                if (not os.path.isfile(self.FOLDERPATH + scriptName)):
                    log("Downloading module " + module)
                    r = requests.get(self.APIURL + module)
                    if (r.status_code == 200):
                        with (open(self.FOLDERPATH + scriptName, "w+") as f):
                            f.write(r.text)

                        self.modules[module] = scriptName
                    else:
                        error("Error downloading, code = " + r.status_code)

            moduleUrl = self.APIURL + module
            moduleElem = HTMLElement("script", attribs=[
                HTMLAttribute("src", self.PUBLICPATH + self.modules[module])
            ])
            pageHead.addChild(moduleElem)

        return pageHead

plugins.registerPlugin(NPM())
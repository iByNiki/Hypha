import hypha.core.plugins as plugins
from hypha.core.structures import *
from hypha.core.logging import *
import os
import json
import re

class Language(plugins.Plugin):
    def __init__(self):
        super().__init__()

        self.NAME = "Language"

    def onRegister(self):
        self.registerHook(plugins.Hooks.RENDER_START, self.onRenderStart)
        self.registerHook(plugins.Hooks.PRE_PAGE_HEAD_RENDER, self.onPrePageHeadRender)
        self.registerHook(plugins.Hooks.PRE_PAGE_FULL_RENDER, self.onPrePageFullRender)

    def createPayload(self):

        # Get language data

        langFolderPath = os.path.join(os.path.dirname(__file__), "lang")

        self.langData = {}

        for rawFileName in os.listdir(langFolderPath):
            fileName = ".".join(rawFileName.split(".")[:len(rawFileName.split(".")) - 1])
            
            f = open(os.path.join(langFolderPath, rawFileName), "r", encoding="utf-8")
            data = f.read()
            f.close()

            jsonData = json.loads(data)
            self.langData[fileName] = jsonData

        # Generate PHP payload
        
        finalPayload = ""

        for key in self.langData:
            payload = "["
            for val in self.langData[key]:
                payload += '"' + val + '" => "' + self.langData[key][val] + '",'
            payload += "]"

            finalPayload += '"' + key + '" => ' + payload + ','

        langDataPayload = "$langData = [" + finalPayload + "];"

        f = open(os.path.join(os.path.dirname(__file__), "payload.php"), "r", encoding="utf-8")
        defaultPayload = f.read()
        f.close()

        return defaultPayload.replace("{{payload}}", langDataPayload)


    def onRenderStart(self):
        # Load language files
        self.payload = self.createPayload()

    def onPrePageHeadRender(self, head, page):
        head.innerHTML += self.payload
        return head
    
    def onPrePageFullRender(self, page):
        matches = re.findall("\\(\\$(.*)\\)", page.content)

        for match in matches:
            page.content = page.content.replace("($" + match + ")", "<?php loc('" + match + "'); ?>")

        return page


plugins.registerPlugin(Language())
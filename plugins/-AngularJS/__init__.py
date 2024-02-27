import hypha.core.plugins as plugins
from hypha.core.logging import *
from hypha.core.structures import *

class AngularJS(plugins.Plugin):
    def __init__(self):
        super().__init__()
        
        self.NAME = "AngularJS"
        self.DEPENDENCIES = ["NPM"]
    
    def onRegister(self):
        self.registerHook(plugins.Hooks.PAGE_FULL_RENDER, self.onPageFullRender)
        self.registerHook(plugins.Hooks.PAGE_JS_RENDER_BUNDLED, self.onPageJSRender)
    
    def onPostRegister(self):
        plugins.getByName("NPM").addModule("angular@1.8.3/angular.min.js")

    def onPageFullRender(self, pageHtml: HTMLElement, page):
        for child in pageHtml.children:
            if (type(child) == HTMLElement):
                if (child.type == "body"): child.addAttrib(HTMLAttribute("ng-app", "app"))
        return pageHtml

    def onPageJSRender(self, pageScripts, page):
        code = 'var angularApp = angular.module("app", []);'
        pageScripts.insert(0, Script(
            lang=JSLang.BABEL,
            defer=True,
            code=code
        ))
        return pageScripts

plugins.registerPlugin(AngularJS())
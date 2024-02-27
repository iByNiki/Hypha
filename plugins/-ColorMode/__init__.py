import hypha.core.plugins as plugins
from hypha.core.logging import *
from hypha.core.structures import *
import os
import json
import cssutils

class ColorMode(plugins.Plugin):

    def __init__(self):
        super().__init__()

        self.NAME = "ColorMode"
        self.DEPENDENCIES = ["NPM"]

    def onRegister(self):
        self.loadConfig()

        self.registerHook(plugins.Hooks.PAGE_CSS_RENDER, self.onPageCssRender)
        self.registerHook(plugins.Hooks.PAGE_JS_RENDER_BUNDLED, self.onPageJSRender)
        self.registerHook(plugins.Hooks.PAGE_FULL_RENDER, self.onPageFullRender)
    
    def onPostRegister(self):
        plugins.getByName("NPM").addModule("js-cookie")
    
    def loadConfig(self):
        f = open(os.path.join(os.path.dirname(__file__), "config.json"), "r")
        data = f.read()
        f.close()

        self.config = json.loads(data)

        f = open(os.path.join(os.path.dirname(__file__), "script.js"), "r")
        self.scriptCode = f.read()
        f.close()

    def onPageCssRender(self, pageCss, page):

        varTexts = []
        for variable in self.config["variables"]:
            varTexts.append("--dark-" + variable["name"] + ": " + variable["dark"] + ";")
            varTexts.append("--light-" + variable["name"] + ": " + variable["light"] + ";")

        injectCss = ":root {" + "".join(varTexts) + "}"
        pageCss.add(injectCss)

        rootDark = []
        for variable in self.config["variables"]:
            rootDark.append("--" + variable["name"] + ": var(--dark-" + variable["name"] + ");")

        injectCss = ':root[data-theme="dark"] {' + "".join(rootDark) + "}"
        pageCss.add(injectCss)
        
        rootLight = []
        for variable in self.config["variables"]:
            rootLight.append("--" + variable["name"] + ": var(--light-" + variable["name"] + ");")

        injectCss = ':root[data-theme="light"] {' + "".join(rootLight) + "}"
        pageCss.add(injectCss)

        return pageCss

    def onPageJSRender(self, pageScripts, page):
        defaultThemeText = "var colorModeTheme = '" + self.config["default"] + "';"
        useSystemDefault = "var colorModeSystemDefault = " + ("true" if self.config["systemDefault"] else "false") + ";\n"
        pageScripts.insert(0, Script(
            lang=JSLang.BABEL,
            defer=True,
            code=defaultThemeText + useSystemDefault + self.scriptCode
            ))
        return pageScripts

    def onPageFullRender(self, pageHtml, page):

        pageHtml.addAttrib(HTMLAttribute("data-theme", "<?php echo (isset($_COOKIE['colormode']) ? $_COOKIE['colormode'] : '" + self.config["default"] + "'); ?>"))
        return pageHtml
    

plugins.registerPlugin(ColorMode())
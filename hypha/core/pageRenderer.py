import hypha.core.builder as builder
from css_html_js_minify import css_minify
from hypha.core.structures import *

class PageRenderer(object):
    def __init__(self, renderPath, pageBuilder):
        self.renderPath = renderPath
        self.pageBuilder = pageBuilder

        self.pagePath = self.renderPath + "/" + "pages" + "/"
        self.cssPath = self.renderPath + "/public/" + "hcss" + "/"
        self.jsPath = self.renderPath + "/public/" + "hjs" + "/"

    def recursiveCSSLoad(self, component):
        finalCss = ""
        
        for reqComp in component.requiredComponents:
            finalCss += self.pageBuilder.components[reqComp].css
            if (len(self.pageBuilder.components[reqComp].requiredComponents) > 0):
                finalCss += self.recursiveCSSLoad(reqComp)
                
        return finalCss
    
    def renderSinglePage(self, page):
        finalHTML = '<!DOCTYPE html><html lang="en">'
        finalBody = "<body>"
        finalHead = '<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
        finalCss = ""

        # Head
        if (page.config != {} and "head" in page.config):
            headData = page.config["head"]
            for elem in headData:
                attrStrings = []
                for key in elem:
                    if (key.lower() != "type" and key.lower() != "inner"):
                        attrStrings.append(key.lower() + '="' + elem[key] + '"')
                
                if (len(attrStrings) > 0):
                    attrs = " " + " ".join(attrStrings)
                else:
                    attrs = ""
                
                finalHead += "<" + elem["type"].lower() + attrs + ">"

                if ("inner" in elem):
                    finalHead += elem["inner"]
                    finalHead += "</" + elem["type"].lower() + ">"

        
        # Body
        if (page.layout != None):
            layout = self.pageBuilder.layouts[page.layout]
            layoutHTML = layout.content
            finalBody += layoutHTML.replace("<slot></slot>", page.content)
            finalCss += layout.css

            for component in layout.requiredComponents:
                finalCss += self.pageBuilder.components[component].css

        else:
            finalBody += page.content

        # Css
        finalCss += page.css

        for component in page.requiredComponents:
            finalCss += self.pageBuilder.components[component].css

        if (page.layout != None):
            layout = self.pageBuilder.layouts[page.layout]
            finalCss += layout.css

        finalRawCss = finalCss
        finalCss = css_minify(finalCss)

        if (finalRawCss != ""):
            finalHead += '<link rel="stylesheet" href="/hcss/' + page.name + '.css">'
            builder.writeFile(self.cssPath + page.name + ".css", finalCss)

        # JS

        bundled = []
        notBundled = []
        finalJs = ""
        deferredJs = ""
        jsLangDeps = []

        # TODO: Recursive JS Load

        if (page.layout != None):
            layout = self.pageBuilder.layouts[page.layout]
            for script in layout.scripts:
                if (script.bundle): bundled.append(script)
                else: notBundled.append(script)

        for script in page.scripts:
            if (script.bundle): bundled.append(script)
            else: notBundled.append(script)

        for component in page.requiredComponents:
            for script in self.pageBuilder.components[component].scripts:
                if (script.bundle): bundled.append(script)
                else: notBundled.append(script)

        for bundledScript in bundled:

            for dep in bundledScript.getLangDeps():
                if (dep not in jsLangDeps): jsLangDeps.append(dep)

            if (bundledScript.defer):
                deferredJs += bundledScript.code
            else:
                finalJs += bundledScript.code

        for unbundledScript in notBundled:
            for dep in unbundledScript.getLangDeps():
                if (dep not in jsLangDeps): jsLangDeps.append(dep)

        finalHead += '<script src="/hjs/hypha.js"></script>'

        # Dependencies
        for dep in jsLangDeps:
            finalHead += '<script src="/hjs/' + dep + '"></script>'

        for i, unbundledScript in enumerate(notBundled):
            pagePath = "unb/" + page.name + "/" + str(i) + ".js"
            builder.writeFile(self.jsPath + pagePath, unbundledScript.code)
            
            finalHead += ('<script src="/hjs/' + pagePath + '"' 
                          + (" defer" if unbundledScript.defer else "") 
                          #+ (' type="systemjs-module"' if unbundledScript.lang == JSLang.TYPESCRIPT else "")
                          + '></script>')

        # TODO: DO MINIFICATION
        if (finalJs != ""):
            pagePath = page.name + "/bundle.js"
            builder.writeFile(self.jsPath + pagePath, finalJs)
            finalHead += '<script src="/hjs/' + pagePath + '"></script>'

        if (deferredJs != ""):
            pagePath = page.name + "/bundle-def.js"
            builder.writeFile(self.jsPath + pagePath, deferredJs)
            finalHead += '<script src="/hjs/' + pagePath + '" defer></script>'

        finalHTML += finalHead + "</head>" + finalBody + "</body></html>"

        builder.writeFile(self.pagePath + page.name + ".php", finalHTML)


    def renderPages(self):
        builder.makePath(self.pagePath)
        builder.makePath(self.cssPath)
        builder.makePath(self.jsPath)

        for page in self.pageBuilder.pages:
            self.renderSinglePage(self.pageBuilder.pages[page])

    def render(self):
        self.renderPages()
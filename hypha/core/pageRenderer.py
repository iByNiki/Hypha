import hypha.core.builder as builder
import hypha.core.plugins as plugins
from css_html_js_minify import css_minify, html_minify
from hypha.core.structures import *
import cssutils

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
    
    def renderHead(self, page):

        finalHead = HTMLElement("head")
        finalHead.addChild(HTMLElement("meta", endTag=False, attribs=[HTMLAttribute("charset", "UTF-8")]))
        finalHead.addChild(HTMLElement("meta", endTag=False, attribs=[
            HTMLAttribute("name", "viewport"),
            HTMLAttribute("content", "width=device-width, initial-scale=1.0")
        ]))

        if (page.config != {} and "head" in page.config):
            headData = page.config["head"]
            for elem in headData:
                elemObj = HTMLElement(elem["elemType"], endTag=("inner" in elem))
                if ("inner" in elem):
                    elemObj.innerHTML = elem["inner"]

                for key in elem:
                    if (key.lower() != "elemType" and key.lower() != "inner"):
                        elemObj.attribs.append(HTMLAttribute(key.lower(), elem[key]))

                finalHead.addChild(elemObj)
                

        return finalHead

    def renderSinglePage(self, page):
        finalHTML = HTMLElement("html", attribs=[HTMLAttribute("lang", "en")])
        finalBody = HTMLElement("body")
        finalCss = ""

        # Head
        finalHead = self.renderHead(page)
        
        # Body
        if (page.layout != None):
            layout = self.pageBuilder.layouts[page.layout]
            layoutHTML = layout.content
            finalBody.addChild(layoutHTML.replace("<slot></slot>", page.content))
            finalCss += layout.css

            for component in layout.requiredComponents:
                finalCss += self.pageBuilder.components[component].css

        else:
            finalBody.addChild(page.content)

        # Css
        finalCss += page.css

        for component in page.requiredComponents:
            finalCss += self.pageBuilder.components[component].css

        if (page.layout != None):
            layout = self.pageBuilder.layouts[page.layout]
            finalCss += layout.css

        finalSheet = cssutils.parseString(finalCss)
        finalSheet.encoding = "utf-8"

        finalCss = plugins.executeOverwriteHook(plugins.Hooks.PAGE_CSS_RENDER, finalSheet, page).cssText.decode("utf-8")

        finalRawCss = finalCss
        finalCss = css_minify(finalCss)

        if (finalRawCss != ""):
            finalHead.addChild(HTMLElement("link", endTag=False, attribs=[
                HTMLAttribute("rel", "stylesheet"),
                HTMLAttribute("href", "/hcss/" + page.name + ".css")
            ]))

            builder.writeFile(self.cssPath + page.name + ".css", finalCss)

        # JS

        bundled = []
        notBundled = []
        finalJs = ""
        deferredJs = ""
        jsLangDeps = []

        requiredComponents = page.requiredComponents

        # Add scripts to list
        if (page.layout != None):
            layout = self.pageBuilder.layouts[page.layout]
            for script in layout.scripts:
                if (script.bundle): bundled.append(script)
                else: notBundled.append(script)
            
            requiredComponents += layout.requiredComponents

        for script in page.scripts:
            if (script.bundle): bundled.append(script)
            else: notBundled.append(script)

        for component in requiredComponents:
            for script in self.pageBuilder.components[component].scripts:
                if (script.bundle): bundled.append(script)
                else: notBundled.append(script)

        bundled = plugins.executeOverwriteHook(plugins.Hooks.PAGE_JS_RENDER_BUNDLED, bundled, page)
        notBundled = plugins.executeOverwriteHook(plugins.Hooks.PAGE_JS_RENDER_NONBUNDLED, notBundled, page)

        # Process
        for bundledScript in bundled:

            for dep in bundledScript.getLangDeps():
                if (dep not in jsLangDeps): jsLangDeps.append(dep)

            if (bundledScript.defer):
                deferredJs += bundledScript.getCompiledCode()
            else:
                finalJs += bundledScript.getCompiledCode()

        for unbundledScript in notBundled:
            for dep in unbundledScript.getLangDeps():
                if (dep not in jsLangDeps): jsLangDeps.append(dep)

        finalHead.addChild(HTMLElement("script", attribs=[HTMLAttribute("src", "/hjs/hypha.js")]))

        # Dependencies
        for dep in jsLangDeps:
            finalHead.addChild(HTMLElement("script", attribs=[HTMLAttribute("src", "/hjs/" + dep)]))

        for i, unbundledScript in enumerate(notBundled):
            pagePath = "unb/" + page.name + "/" + str(i) + ".js"
            builder.writeFile(self.jsPath + pagePath, unbundledScript.getCompiledCode())

            scriptElem = HTMLElement("script", attribs=[HTMLAttribute("src", "/hjs/" + pagePath)])
            if (unbundledScript.defer): scriptElem.addAttrib(HTMLAttribute("defer", "", noValue=True))
            finalHead.addChild(scriptElem)

        # TODO: DO MINIFICATION
        if (finalJs != ""):
            pagePath = page.name + "/bundle.js"
            builder.writeFile(self.jsPath + pagePath, finalJs)
            finalHead.addChild(HTMLElement("script", attribs=[HTMLAttribute("src", "/hjs/" + pagePath)]))

        if (deferredJs != ""):
            pagePath = page.name + "/bundle-def.js"
            builder.writeFile(self.jsPath + pagePath, deferredJs)
            finalHead.addChild(HTMLElement("script", attribs=[
                HTMLAttribute("src", "/hjs/" + pagePath),
                HTMLAttribute("defer", "", noValue=True)
            ]))

        finalHead = plugins.executeOverwriteHook(plugins.Hooks.PAGE_HEAD_RENDER, finalHead, page)
        finalBody = plugins.executeOverwriteHook(plugins.Hooks.PAGE_BODY_RENDER, finalBody, page)

        finalHTML.addChild(finalHead)
        finalHTML.addChild(finalBody)
        #finalHTML = html_minify(finalHTML)

        finalHTML = plugins.executeOverwriteHook(plugins.Hooks.PAGE_FULL_RENDER, finalHTML, page)
        finalHTMLString = str(finalHTML).replace("&gt;", ">").replace("<!--<?php", "<?php").replace("?>-->", "?>")
        finalHTMLString = finalHTMLString.replace("&lt;!--&lt;?php", "<?php")

        builder.writeFile(self.pagePath + page.name + ".php", "<!DOCTYPE html>" + finalHTMLString)


    def renderPages(self):
        builder.makePath(self.pagePath)
        builder.makePath(self.cssPath)
        builder.makePath(self.jsPath)

        for page in self.pageBuilder.pages:
            self.renderSinglePage(self.pageBuilder.pages[page])

    def render(self):
        self.renderPages()
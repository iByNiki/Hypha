import hypha.core.builder as builder
from bs4 import BeautifulSoup
import re
import json
import cssutils
from hypha.core.structures import *

# TODO: CSS, scripts and config

class PageBuilder(object):
    def __init__(self):
        self.pageDir = "pages"
        self.layoutDir = "layouts"
        self.componentDir = "components"

        self.components = {}
        self.layouts = {}
        self.pages = {}

        self.scopedClasses = []

    def parseConfig(self, configText):
        return json.loads(configText)
    
    def parseTemplate(self, template, scopePrefix, parentComponent=None):

        # CSS Scoping
        elements = template.find_all(class_=True)
        for element in elements:
            if (not element.has_attr("class")): continue
            classListRaw = element["class"].split(" ")
            classList = []
            initialName = element["class"]

            toScope = 0

            for className in classListRaw:

                if (className in self.scopedClasses):
                    newClassName = scopePrefix + "-" + className
                    toScope += 1
                else: newClassName = className

                classList.append(newClassName)
            
            newClassName = " ".join(classList)

            replaceElem = template.find(attrs={"class", element["class"]})
            while (replaceElem != None and toScope > 0):
                template.find(attrs={"class", initialName})["class"] = newClassName
                
                replaceElem = template.find(attrs={"class", initialName})

        # Component replacement
        foundComponents = []

        innerHTML = builder.getInnerHTML(template)
        matches = re.findall("<[a-zA-z]*.*/>", innerHTML)

        componentList = [builder.dirName(p) for p in builder.getComponentPaths()]

        for elem in template.findAll():
            processElem = False
            if (elem.name in self.components):
                processElem = True
                componentName = elem.name

                foundComponents.append(componentName)
                component = self.components[componentName]   

            elif (elem.name in componentList):
                processElem = True
                componentName = elem.name

                foundComponents.append(componentName)
                component = self.buildSingleComponent(builder.getSoup("components/" + componentName + ".php"), componentName)
                self.components[componentName] = component

            if (processElem):
                newContent = component.content

                if (elem.attrs != None):
                    varMatches = re.findall("\|\|.*?\|\|", newContent)
                    for varMatch in varMatches:
                        matchName = varMatch[2:len(varMatch) - 2]
                        matchReplace = ""
                        if (matchName in elem.attrs):
                            matchReplace = elem.attrs[matchName]

                        newContent = newContent.replace(varMatch, matchReplace)

                elemInner = builder.getInnerHTML(elem)
                processedSlot, temp = self.parseTemplate(BeautifulSoup("<xml>" + elemInner + "</xml>", "xml"), scopePrefix)
                processedSlot = processedSlot.replace("<xml>", "").replace("</xml>", "")
                newContent = newContent.replace("<slot/>", processedSlot).replace("<slot />", processedSlot)

                innerHTML = innerHTML.replace(str(elem), newContent)


        """for match in matches:
            componentString = match.replace("<", "").replace("/>", "")
            componentName = componentString.split(" ")[0]
            rawAttribs = componentString.split(" ")[1:]
            componentAttribs = {}
            
            for attrib in rawAttribs:
                parsedValue = attrib.split("=")[1]
                if (parsedValue[0] == '"' and parsedValue[-1] == '"'):
                    parsedValue = parsedValue[1:len(parsedValue) - 1]
                componentAttribs[attrib.split("=")[0]] = parsedValue

            if (componentName == "slot"): continue

            foundComponents.append(componentName)

            if (componentName == parentComponent): # TODO: MAKE THIS CHECK WORK WTF
                raise Exception("Component infinite loop? Between " + componentName + " and " + parentComponent)
            
            if (componentName not in self.components):
                component = self.buildSingleComponent(builder.getSoup("components/" + componentName + ".php"), componentName)
                self.components[componentName] = component
            else:
                component = self.components[componentName]

            innerHTML = innerHTML.replace(match, component.content)"""

        return innerHTML, foundComponents

    def parseCss(self, style, scopePrefix):

        innerHTML = builder.getInnerHTML(style)
        parser = cssutils.CSSParser()
        sheet = parser.parseString(innerHTML)

        if ("scoped" not in style.attrs):
            return sheet.cssText.decode("utf-8")

        for rule in sheet:
            if (rule.type != rule.STYLE_RULE):
                continue
            
            for selector in rule.selectorList:
                matches = re.findall("\\.[a-zA-z0-9_-]*", selector.selectorText)
                for match in matches:
                    self.scopedClasses.append(match.lstrip("."))
                    parsedMatch = "." + scopePrefix + "-" + match.lstrip(".")
                    newText = selector.selectorText.replace(match, parsedMatch)
                    selector._setSelectorText(newText)

        return sheet.cssText.decode("utf-8")

    def buildSingleComponent(self, soup, name):
        templateElem = soup.find("template")
        styleElem = soup.find("style")
        configElem = soup.find("config")

        component = Component(name)

        scopePrefix = "c" + str(len(self.components))

        if (styleElem != None):
            component.css = self.parseCss(styleElem, scopePrefix)

        if (templateElem != None):
            component.content, component.requiredComponents = self.parseTemplate(templateElem, scopePrefix, parentComponent=name)
        
        return component


    def buildComponents(self):
        for componentPath in builder.getComponentPaths():
            soup = builder.getSoup(componentPath)
            name = builder.dirName(componentPath)

            if (name not in self.components):
                self.components[name] = self.buildSingleComponent(soup, name)

    def buildDefaultComponents(self):
        for componentPath in builder.getDefaultComponentPaths():
            soup = builder.getSoup(componentPath)
            name = builder.dirName(builder.dirName(componentPath))

            if (name not in self.components):
                self.components[name] = self.buildSingleComponent(soup, name)
            
    def buildSingleLayout(self, soup, name):
        templateElem = soup.find("template")
        styleElem = soup.find("style")
        configElem = soup.find("config")

        layout = Layout(name)

        scopePrefix = "l" + str(len(self.layouts))

        if (styleElem != None):
            layout.css = self.parseCss(styleElem, scopePrefix)

        if (templateElem != None):
            layout.content, layout.requiredComponents = self.parseTemplate(templateElem, scopePrefix)
        
        return layout

    def buildLayouts(self):
        for layoutPath in builder.getLayoutPaths():
            soup = builder.getSoup(layoutPath)
            name = builder.dirName(layoutPath)

            if (name not in self.layouts):
                self.layouts[name] = self.buildSingleLayout(soup, name)
    
    def buildSinglePage(self, soup, name):
        templateElem = soup.find("template")
        styleElem = soup.find("style")
        configElem = soup.find("config")

        page = Page(name)

        scopePrefix = "p" + str(len(self.pages))

        if (styleElem != None):
            page.css = self.parseCss(styleElem, scopePrefix)

        if (templateElem != None):
            page.content, page.requiredComponents = self.parseTemplate(templateElem, scopePrefix)
        
        if (configElem != None):
            parsedConfig = self.parseConfig(builder.getInnerHTML(configElem))
            page.config = parsedConfig

            if ("layout" in page.config):
                layoutName = page.config["layout"]
                if (layoutName != "none"):
                    if (layoutName not in self.layouts):
                        raise Exception("Layout " + str(layoutName) + " not found. Error in page " + str(name))
                    page.layout = layoutName
            else:
                if ("default" in self.layouts):
                    page.layout = "default"
        else:
            if ("default" in self.layouts):
                page.layout = "default"
        
        return page

    def buildPages(self):
        for pagePath in builder.getPagePaths():
            soup = builder.getSoup(pagePath)
            name = builder.dirName(pagePath)

            if (name not in self.pages):
                self.pages[name] = self.buildSinglePage(soup, name)

    def build(self):
        self.buildDefaultComponents()
        self.buildComponents()
        self.buildLayouts()
        self.buildPages()
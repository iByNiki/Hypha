import hypha.core.builder as builder
from hypha.core.structures import *
import cssutils
import dukpy
import re

def parseCss(style, scopedClasses, scopePrefix):

    innerHTML = builder.getInnerHTML(style)
    parser = cssutils.CSSParser()
    sheet = parser.parseString(innerHTML)

    if ("scoped" not in style.attrs):
        return sheet.cssText.decode("utf-8")

    for rule in sheet:
        if (rule.type != rule.STYLE_RULE):
            if (rule.type == rule.MEDIA_RULE):
                for subrule in rule:
                    for selector in subrule.selectorList:
                        matches = re.findall("\\.[a-zA-z0-9_-]*", selector.selectorText)
                        for match in matches:
                            scopedClasses.append(match.lstrip("."))
                            parsedMatch = "." + scopePrefix + "-" + match.lstrip(".")
                            newText = selector.selectorText.replace(match, parsedMatch)
                            selector._setSelectorText(newText)
            continue

        for selector in rule.selectorList:
            matches = re.findall("\\.[a-zA-z0-9_-]*", selector.selectorText)
            for match in matches:
                scopedClasses.append(match.lstrip("."))
                parsedMatch = "." + scopePrefix + "-" + match.lstrip(".")
                newText = selector.selectorText.replace(match, parsedMatch)
                selector._setSelectorText(newText)

    return sheet.cssText.decode("utf-8")

def getRequiresRecursively(scriptCode):

    requires = re.findall("""require\(["|'](.*)["|']\)""", scriptCode)

    for require in requires:
        f = open("scripts/" + require + ".js")
        data = f.read()
        f.close()

        newReqs = getRequiresRecursively(data)
        for newReq in newReqs:
            if (newReq not in requires): requires.append(newReq)

    return requires

def parseJS(scriptTag):
    attrs = scriptTag.attrs
    lang = JSLang.VANILLA
    code = ""
    defer = ("defer" in attrs)
    bundle = True
    requires = []

    if ("bundle" in attrs):
        if (attrs["bundle"].lower() == "false" or attrs["bundle"].lower() == "f"):
            bundle = False

    if ("lang" in attrs):
        for key in JSLang:
            for name in key.value:
                if (name.lower() == attrs["lang"].lower()):
                    lang = key

    if (scriptTag.string != None):
        requires = getRequiresRecursively(scriptTag.string)
        code = scriptTag.string

    return Script(lang=lang, code=code, defer=defer, bundle=bundle, requires=requires)
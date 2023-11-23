import hypha.core.builder as builder
from css_html_js_minify import css_minify

class PageRenderer(object):
    def __init__(self, renderPath, pageBuilder):
        self.renderPath = renderPath
        self.pageBuilder = pageBuilder

        self.pagePath = self.renderPath + "/" + "pages" + "/"
        self.cssPath = self.renderPath + "/public/" + "hcss" + "/"
        self.jsPath = self.renderPath + "/public/" + "hjs" + "/"

    def makeHeader(self, page):
        pass

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
        finalHead = "<head>"
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
            finalBody += layoutHTML.replace("<slot/>", page.content).replace("<slot />", page.content)
            finalCss += layout.css

            for component in layout.requiredComponents:
                finalCss += self.pageBuilder.components[component].css

        else:
            finalBody += page.content

        # Css
        finalCss += page.css
        for component in page.requiredComponents:
                finalCss += self.pageBuilder.components[component].css

        finalCss = css_minify(finalCss)

        if (finalCss != ""):
            finalHead += '<link rel="stylesheet" href="/hcss/' + page.name + '.css">'
            builder.writeFile(self.cssPath + page.name + ".css", finalCss)

        finalHead += '<script src="/hjs/hypha.js" defer></script>'
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
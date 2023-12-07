import hypha.core.plugins as plugins
from hypha.core.pageBuilder import *
from hypha.core.pageRenderer import *
from hypha.core.routerBuilder import *
from hypha.core.logging import *

import os
import shutil

def walkPathFiles(path):
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]

def getLayoutPaths():
    return walkPathFiles("layouts")

def getPagePaths():
    return walkPathFiles("pages")

def getComponentPaths():
    return walkPathFiles("components")

def getDefaultComponentPaths():
    return walkPathFiles("hypha/components")

def dirName(path):
    path = path.replace(os.sep, '/')
    return os.path.splitext("/".join(path.strip("/").split('/')[1:]))[0].replace(os.sep, '/')

def getSoup(dir):
    f = open(dir, "r")
    content = f.read()
    f.close()

    return BeautifulSoup(content, "html.parser")

def makePath(path):
    os.makedirs(path, exist_ok=True)

def writeFile(path, data):
    if (not os.path.exists(os.path.dirname(path))): makePath(os.path.dirname(path))
    f = open(path, "w+")
    f.write(data)
    f.close()

def getInnerHTML(elem):
    return "".join(str(x) for x in elem.contents)

def buildInit():
    plugins.importPlugins()

def build():

    log("Building pages...")
    pageBuilder = PageBuilder()
    pageBuilder.build()

    try:
        shutil.rmtree("tmp")
    except:
        pass

    makePath("tmp")

    shutil.copytree("hypha/default", "tmp", dirs_exist_ok=True)
    shutil.copytree("public", "tmp/public", dirs_exist_ok=True)
    shutil.copytree("scripts", "tmp/public/hjs/scripts", dirs_exist_ok=True)

    log("Rendering pages...")
    pageRenderer = PageRenderer("tmp", pageBuilder)
    pageRenderer.render()

    log("Creating routes...")
    routerBuilder = RouterBuilder("tmp", pageBuilder)
    routerBuilder.build()

    try:
        shutil.rmtree("build")
    except:
        pass

    shutil.copytree("tmp", "build", dirs_exist_ok=True)

    try:
        shutil.rmtree("tmp")
    except:
        pass

    log("Done!")
import os
import shutil

class RouterBuilder(object):
    def __init__(self, tmpPath, pageBuilder):
        self.pageBuilder = pageBuilder
        self.tmpPath = tmpPath

        self.routes = {}

        self.routerPath = tmpPath + "/router.php"
        self.routesPath = tmpPath + "/routes.php"

    def addRoute(self, key, dir):
        self.routes[key] = dir

    def write(self):
        f = open(self.routesPath, "r")
        routesData = f.read() + "\n"
        f.close()

        for key in self.routes:
            routesData += '$router->get("' + key + '", "' + self.routes[key] + '");\n'

        routesData += "$router->run();\n"
        routesData += "?>\n"

        f = open(self.routesPath, "w+")
        f.write(routesData)
        f.close()

    def build(self):
        for page in self.pageBuilder.pages:
            baseName = os.path.basename(page)
            if (baseName == "index"):
                dirName = os.path.dirname(page)
                if (dirName == ""): dirName = "/"
                self.addRoute(dirName, "/pages/" + page + ".php")
            else:
                self.addRoute(page, "/pages/" + page + ".php")

        self.write()

import hypha.core.builder as builder
from hypha.core.logging import *
import hypha.core.utils as utils

import sys
import argparse
import zipfile
import requests
import io
import os
import subprocess
import time
from multiprocessing import Process, Pipe
import socket
import hashlib
import base64

PHP_URL_WIN = "https://windows.php.net/downloads/releases/php-8.0.30-nts-Win32-vs16-x64.zip"
OS_TYPE = None

PORT = 80
PHPSILENT = True

def downloadPHP():

    if (OS_TYPE == "lin"):
        try:
            subprocess.run(
                ["php", "-v"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return
        except FileNotFoundError:
            error("Please install PHP to use the development enviroment.")
            os._exit()

    elif (OS_TYPE == "win"):
        if (os.path.isfile("hypha/php/php.exe")):
            log("PHP has already been downloaded!")
            return

        log("Downloading PHP...")
        r = requests.get(PHP_URL_WIN)

        log("Unzipping...")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("hypha/php")

def phpServerCommand(osType, port, silent):
    cmdArgs = "-S 0.0.0.0:" + str(port) + " build/routes.php -t build"
    if (osType == "lin"):
        fullCmd = ["hypha/php/php.exe"] + cmdArgs.split()
    else:
        fullCmd = ["hypha/php/php.exe"] + cmdArgs.split()

    if (silent):
        subprocess.run(
            fullCmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        subprocess.run(fullCmd)
    
    error("Error while starting php server. Please use -v")

def startDevServer():
    log("Starting server...")

    phpThread = Process(target=phpServerCommand, args=(OS_TYPE, PORT, PHPSILENT))
    phpThread.start()

    time.sleep(2)
    log("Server started in port " + str(PORT))

    appDir = os.getcwd()
    lastHash = utils.md5_dir(appDir)

    try:
        while (True):
            time.sleep(1)
            hash = utils.md5_dir(appDir)
            if (hash != lastHash):
                log("Detected changes, rebuilding...")
                builder.build()
            lastHash = hash
    except KeyboardInterrupt:
        log("Closing server...")
        phpThread.terminate()
        log("Bye!")
        os._exit(1)

def build():
    builder.buildInit()
    builder.build()

def dev():
    downloadPHP()
    builder.buildInit()
    builder.build()
    startDevServer()

def main():
    global OS_TYPE, PORT, PHPSILENT

    parser = argparse.ArgumentParser(
        prog="Hypha",
        description="The Javascript Framework for PHP"
    )

    parser.add_argument("cmd", type=str, help="build / dev")
    parser.add_argument("-p", "--port", type=int, default=80, help="Port of the dev server")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show messages of the PHP server")

    args = parser.parse_args()

    PORT = args.port
    PHPSILENT = (not args.verbose)

    if (os.name == "nt"):
        OS_TYPE = "win"
    elif (os.name == "posix"):
        OS_TYPE = "lin"
    else:
        error("Unknown OS, please open a github issue with this stack trace.\nOS Name: " + str(os.name))
        os._exit(1)

    if (args.cmd == "build"):
        build()
    elif (args.cmd == "dev"):
        # Start dev server with automatic building and restarting
        dev()

if (__name__ == "__main__"):
    main()
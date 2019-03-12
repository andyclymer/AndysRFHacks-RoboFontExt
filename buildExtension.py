from __future__ import absolute_import
from __future__ import print_function
import os
from mojo.extensions import ExtensionBundle


basePath = os.path.dirname(__file__)
extensionPath = os.path.join(basePath, "AndysRFHacks.roboFontExt")
libPath = os.path.join(basePath, "lib")
htmlPath = os.path.join(basePath, "html")
resourcesPath = os.path.join(basePath, "resources")

B = ExtensionBundle()

B.name = "Andy's RF Hacks"
B.version = "1.1"
B.developer = "Andy Clymer"
B.developerURL = 'http://www.andyclymer.com/'

B.mainScript = "Setup.py"
B.launchAtStartUp = True
B.addToMenu = [
    {
        'path' : 'Manager.py',
        'preferredName': 'Preferences',
        'shortKey' : '',
    }]
    
B.requiresVersionMajor = '3'
B.requiresVersionMinor = '1'
B.infoDictionary["html"] = True

B.save(extensionPath, libPath=libPath, htmlPath=htmlPath, resourcesPath=resourcesPath, pycOnly=False)

print("Done")
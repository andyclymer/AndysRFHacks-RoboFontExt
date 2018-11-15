import os
import sys
import importlib
from mojo.extensions import getExtensionDefault, setExtensionDefault
from mojo.extensions import ExtensionBundle

KEYPREFIX = "com.andyclymer.andysHacks"


extBundle = ExtensionBundle("AndysRFHacks")
# Clear out any script metadata if it's a new version of the extension
if not extBundle.version == getExtensionDefault("%s.version" % KEYPREFIX, fallback="0.0"):
    setExtensionDefault("%s.version" % KEYPREFIX, extBundle.version)
    setExtensionDefault("%s.scriptMetadata" % KEYPREFIX, {})

from Scripts import *
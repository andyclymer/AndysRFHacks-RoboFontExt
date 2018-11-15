from mojo.extensions import getExtensionDefault, setExtensionDefault
from mojo.events import addObserver, removeObserver


# Script setup:
metadata = dict(
    shortName = "SampleHack",
    longName = "Sample Hack",
    description = "This is the description of a sample hack")
# Read the current scriptMetadata and add this one
fullMetadata = getExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fallback={})
fullMetadata[metadata["shortName"]] = metadata
setExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fullMetadata)
# Set the default on/off to False, or just keep the current state
scriptStateKey = "com.andyclymer.andysHacks.%s-state" % metadata["shortName"]
currentState = getExtensionDefault(scriptStateKey, fallback=False)
setExtensionDefault(scriptStateKey, currentState)



class SampleHack:
    
    def __init__(self):
        self.state = getExtensionDefault(scriptStateKey, fallback=False)
        if self.state:
            addObserver(self, "draw", "draw")
    
    def draw(self, scale):
        print("Drawing!")

SampleHack()
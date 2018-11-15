from mojo.UI import SetCurrentLayerByName
from mojo.extensions import getExtensionDefault, setExtensionDefault
from mojo.events import addObserver, removeObserver

""" Andy Clymer """

# Script setup:
metadata = dict(
    shortName = "HotkeyJumpToForeground",
    longName = "Hotkey – Jump to Foreground",
    description = "Assigns the “f” key to jump back to the “foreground” layer.")
    
# Read the current scriptMetadata and add this one
fullMetadata = getExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fallback={})
fullMetadata[metadata["shortName"]] = metadata
setExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fullMetadata)
# Set the default on/off to False, or just keep the current state
scriptStateKey = "com.andyclymer.andysHacks.%s-state" % metadata["shortName"]
currentState = getExtensionDefault(scriptStateKey, fallback=False)
setExtensionDefault(scriptStateKey, currentState)



class JumpToForeground():

    def __init__(self):
        if getExtensionDefault(scriptStateKey, fallback=False):
            addObserver(self, "keyDown", "keyDown")

    def keyDown(self, info):
        event = info["event"]
        characters = event.characters()
        modifierFlags = event.modifierFlags()
        if characters == "f":
            SetCurrentLayerByName("foreground")

JumpToForeground()

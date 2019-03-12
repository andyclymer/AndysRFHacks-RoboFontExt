from mojo.UI import SetCurrentLayerByName
from mojo.extensions import getExtensionDefault, setExtensionDefault
from mojo.events import addObserver, removeObserver

""" Andy Clymer """

# Script setup:
metadata = dict(
    shortName = "HotkeyShowHide",
    longName = "Hotkey – Show/Hide Layers",
    description = "Assigns the “h” key to show/hide layer outlines.")
    
# Read the current scriptMetadata and add this one
fullMetadata = getExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fallback={})
fullMetadata[metadata["shortName"]] = metadata
setExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fullMetadata)
# Set the default on/off to False, or just keep the current state
scriptStateKey = "com.andyclymer.andysHacks.%s-state" % metadata["shortName"]
currentState = getExtensionDefault(scriptStateKey, fallback=False)
setExtensionDefault(scriptStateKey, currentState)



class ShowHideLayers():

    def __init__(self):
        if getExtensionDefault(scriptStateKey, fallback=False):
            addObserver(self, "keyDown", "keyDown")

    def keyDown(self, info):
        event = info["event"]
        characters = event.characters()
        if characters == "h":
            modifierFlags = event.modifierFlags()
            glyph = info["glyph"]
            f = glyph.font
            if len(f.layerOrder) > 1:
                nextLayer = f.layerOrder[1]
                # Get the current display status for the first non-foreground layer
                currentDisplayOption = f.getLayer(nextLayer).getDisplayOption()["Stroke"]
                # Set the oppoosite display status on all other layers:
                for layerName in f.layerOrder:
                    if not layerName == "foreground":
                        f.getLayer(layerName).setDisplayOption("Stroke", not currentDisplayOption)

ShowHideLayers()




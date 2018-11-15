from lib.tools.defaults import getDefault, setDefault
from mojo.events import addObserver
from mojo.extensions import getExtensionDefault, setExtensionDefault
from mojo.events import addObserver, removeObserver

""" Andy Clymer """

# Script setup:
metadata = dict(
    shortName = "SnapOnlyWhileDragging",
    longName = "Snap Closed Only While Dragging",
    description = "Only “snap to close” open contours while the mouse clicked down and dragging. This prevents open ended contours from joining together when moving a point with the arrow keys.")
    
# Read the current scriptMetadata and add this one
fullMetadata = getExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fallback={})
fullMetadata[metadata["shortName"]] = metadata
setExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fullMetadata)
# Set the default on/off to False, or just keep the current state
scriptStateKey = "com.andyclymer.andysHacks.%s-state" % metadata["shortName"]
currentState = getExtensionDefault(scriptStateKey, fallback=False)
setExtensionDefault(scriptStateKey, currentState)




class SnapClosedOnlyWhileDragging(object):
    
    """
    Startup Script:
        Only "snap to close" open contours while the mouse clicked down and dragging.
        Prevents open ended contours from closing when nudging with the arrow keys.
        -- Andy Clymer, github.com/andyclymer
    """

    def __init__(self):
        
        self.snapToCloseDistance = 4
        
        if getExtensionDefault(scriptStateKey, fallback=False):
            addObserver(self, "mouseDownCallback", "mouseDown")
            addObserver(self, "mouseUpCallback", "mouseUp")

    def mouseDownCallback(self, info):
        setDefault("glyphViewCloseContourSnapDistance", self.snapToCloseDistance)

    def mouseUpCallback(self, info):
        setDefault("glyphViewCloseContourSnapDistance", 0)

SnapClosedOnlyWhileDragging()
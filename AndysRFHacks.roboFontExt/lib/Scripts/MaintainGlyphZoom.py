from AppKit import NSRect
from mojo.extensions import getExtensionDefault, setExtensionDefault
from mojo.events import addObserver, removeObserver

import sys
import importlib
importlib.reload(sys.modules[__name__])

""" Andy Clymer """

# Script setup:
metadata = dict(
    shortName = "MaintainGlyphZoom",
    longName = "Maintain Glyph Zoom",
    description = "RoboFont usually adjusts the glyph view to “resize to fit” when you switch between glyphs or layers, this option will maintain the same zoom settings as you switch to another layer or glyph in the same glyph window.")
    
# Read the current scriptMetadata and add this one
fullMetadata = getExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fallback={})
fullMetadata[metadata["shortName"]] = metadata
setExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fullMetadata)
# Set the default on/off to False, or just keep the current state
scriptStateKey = "com.andyclymer.andysHacks.%s-state" % metadata["shortName"]
currentState = getExtensionDefault(scriptStateKey, fallback=False)
setExtensionDefault(scriptStateKey, currentState)



# RF Version Check
from mojo.roboFont import version
RF3 = version[0] > "1"

class MaintainZoom(object):
    
    """
    Startup Script:
        Maintain the same zoom settings when switching between layers and glyphs
        -- Andy Clymer, github.com/andyclymer
    """

    def __init__(self):

        # Save zoom posSize and offset for each open font
        # font object as key, dict of "rectPos", "rectSize", "offset" and "glyph" as value
        self.prevZoom = {}
        
        if getExtensionDefault(scriptStateKey, fallback=False):
            addObserver(self, "getZoom", "viewWillChangeGlyph")
            addObserver(self, "setZoom", "viewDidChangeGlyph")

    def getZoom(self, info):
        view = info["view"]
        glyph = info["glyph"]
        if not None in [view, glyph]:
            font = glyph.getParent()
            # Get the zoom rect and offset for the view
            rect = view.visibleRect()
            offset = view._offset
            posSizeOffset = dict(
                rectPos = (rect.origin.x, rect.origin.y),
                rectSize = (rect.size.width, rect.size.height), 
                offset = (offset.x, offset.y),
                glyph = glyph)
            # Save the zoom info
            self.prevZoom[font] = posSizeOffset

    def setZoom(self, info):
        view = info["view"]
        glyph = info["glyph"]
        if not None in [view, glyph]:
            font = glyph.getParent()
            # Set the zoom info, if this is a new glyph or layer
            if font in self.prevZoom:
                posSizeOffset = self.prevZoom[font]
                if not posSizeOffset["glyph"]== glyph:
                    offset = view._offset
                    newRect = NSRect()
                    newRect.origin.x, newRect.origin.y = posSizeOffset["rectPos"]
                    newRect.size.width, newRect.size.height = posSizeOffset["rectSize"]
                    view.zoomViewToRect_(newRect)
                    view._offset.x, view._offset.y = posSizeOffset["offset"]
            else:
                # Zoom to 100% if nothing has been saved for this font
                view.zoomViewToAbsoluteScale_(1)

if RF3:
    MaintainZoom()


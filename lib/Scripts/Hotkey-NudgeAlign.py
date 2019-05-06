from mojo.UI import SetCurrentLayerByName
from mojo.extensions import getExtensionDefault, setExtensionDefault
from mojo.events import addObserver, removeObserver

""" Andy Clymer """

# Script setup:
metadata = dict(
    shortName = "HotkeyNudgeAlign",
    longName = "Hotkey – Nudge Align",
    description = "Hold the “Command” key while nudging with the arrow keys to align the selected points with other points or glyph metrics.")
    
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
        #if getExtensionDefault(scriptStateKey, fallback=False):
        addObserver(self, "keyDown", "keyDown")
        self.arrowKeyChars = {
            63232:"up",
            63233:"down",
            63234:"left",
            63235:"right"}
            
            
    def collectLocations(self, glyph, doPoints=True, doMetrics=True, doGuides=True):
        snapX = []
        snapY = []
        if doPoints == True:
            for c in glyph.contours:
                for bPt in c.bPoints:
                    if not bPt.selected:
                        if not bPt.anchor[0] in snapX: snapX += [bPt.anchor[0]]
                        if not bPt.anchor[1] in snapY: snapY += [bPt.anchor[1]]
        if doMetrics == True:
            f = glyph.font
            metricsY = [f.info.descender, 0, f.info.xHeight, f.info.ascender]
            metricsX = [0, glyph.width]
            for m in metricsY:
                if not m in snapY: snapY += [m]
            for m in metricsX:
                if not m in snapX: snapX += [m]
        if doGuides == True:
            for gd in glyph.guides:
                if gd.angle in [0, 180]:
                    if not gd.y in snapY: snapY += [gd.y]
                elif gd.angle in [90, 270]:
                    if not gd.x in snapX: snapX += [gd.x]
        snapX.sort()
        snapY.sort()
        return (snapX, snapY)
    
    
    def getSelectionBounds(self, g):
        # Get the selection bounds
        top = None
        bottom = None
        left = None
        right = None
        for c in g.contours:
            for bPt in c.bPoints:
                if bPt.selected:
                    x, y = bPt.anchor
                    if left == None:
                        left = x
                        right = x
                        top = y
                        bottom = y
                    if x < left: left = x
                    elif x > right: right = x
                    if y < bottom: bottom = y
                    elif y > top: top = y
        return dict(left=left, right=right, top=top, bottom=bottom)


    def findNeighbors(self, glyph, loc, axis):
        snapX, snapY = self.collectLocations(glyph)
        if axis == "x":
            snap = snapX
        else: snap = snapY
        n = [loc, loc]
        for i, l in enumerate(snap):
            if l > loc:
                if not i == 0:
                    n = [snap[i-1], snap[i]]
                else: n = [loc, snap[i]]
                break
        return n

            
    def keyDown(self, info):
        event = info["event"]
        modifierFlags = event.modifierFlags()
        if modifierFlags == 11534600: # command
            character = event.characters()
            if ord(character) in self.arrowKeyChars:
                glyph = info["glyph"]
                bounds = self.getSelectionBounds(glyph)
                direction = self.arrowKeyChars[ord(character)]
                diff = (0, 0)
                if direction == "up":
                    n = self.findNeighbors(glyph, bounds["top"], "y")
                    diff = (0, n[1] - bounds["top"])
                elif direction == "down":
                    n = self.findNeighbors(glyph, bounds["bottom"], "y")
                    diff = (0, n[0] - bounds["bottom"])
                if direction == "left":
                    n = self.findNeighbors(glyph, bounds["left"], "x")
                    diff = (n[0] - bounds["left"], 0)
                elif direction == "right":
                    n = self.findNeighbors(glyph, bounds["right"], "x")
                    diff = (n[1] - bounds["right"], 0)
                if not diff == (0, 0):
                    glyph.prepareUndo("Nudge")
                    for c in glyph.contours:
                        for bPt in c.bPoints:
                            if bPt.selected:
                                bPt.moveBy(diff)
                    glyph.performUndo()
                    
                

ShowHideLayers()




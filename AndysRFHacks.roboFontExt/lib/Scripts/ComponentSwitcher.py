import vanilla
import mojo.drawingTools as dt
from mojo.UI import CurrentGlyphWindow
from AppKit import NSColor
from mojo.extensions import getExtensionDefault, setExtensionDefault
from mojo.events import addObserver, removeObserver

""" Andy Clymer """

# Script setup:
metadata = dict(
    shortName = "ComponentSwitcher",
    longName = "Component Switcher",
    description = "Quickly jump to a component’s base glyph (and back).\n\nIn a glyph window, double-click a component to jump to its base glyph. While you’re editing the component you’ll see a preview of the composed glyph you just came from off to the right. Double-click this preview to jump back to the composed glyph.")
# Read the current scriptMetadata and add this one
fullMetadata = getExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fallback={})
fullMetadata[metadata["shortName"]] = metadata
setExtensionDefault("com.andyclymer.andysHacks.scriptMetadata", fullMetadata)
# Set the default on/off to False, or just keep the current state
scriptStateKey = "com.andyclymer.andysHacks.%s-state" % metadata["shortName"]
currentState = getExtensionDefault(scriptStateKey, fallback=False)
setExtensionDefault(scriptStateKey, currentState)





class CompoonentSwitcher:
    
    def __init__(self):
        self.currentGlyph = None
        self.previousGlyph = None
        self.didSwitch = False # When a glyph change happened because of this extension
        
        self.w = vanilla.Window((200, 200))
        self.w.bind("close", self.close)
        #self.w.open()
        
        if getExtensionDefault(scriptStateKey, fallback=False):
            addObserver(self, "draw", "draw")
            addObserver(self, "drawPreview", "drawPreview")
            addObserver(self, "drawInactive", "drawInactive")
            addObserver(self, "mouseDown", "mouseDown")
            addObserver(self, "viewDidChangeGlyph", "viewDidChangeGlyph")
        
    
    def close(self, sender):
        removeObserver(self, "draw")
        removeObserver(self, "drawPreview")
        removeObserver(self, "drawInactive")
        removeObserver(self, "mouseDown")
        removeObserver(self, "viewDidChangeGlyph")
        if not self.currentGlyph == None:
            self.currentGlyph.removeObserver(self, "Glyph.Changed")
        
    def viewDidChangeGlyph(self, info):
        glyph = info["glyph"]
        if not self.currentGlyph == None:
            self.currentGlyph.removeObserver(self, "Glyph.Changed")
        if self.didSwitch: # This tool did the switching, remember the previous glyph to draw it
            self.previousGlyph = self.currentGlyph
            self.didSwitch = False
        else:
            if not self.currentGlyph == glyph:
                self.previousGlyph = None
        self.currentGlyph = glyph
        if not self.currentGlyph == None:
            self.currentGlyph.addObserver(self, "glyphChanged", "Glyph.Changed")
            
    def glyphChanged(self, info):
        pass
        
    
    def drawGlyph(self):
        if not self.previousGlyph == None:
            path = self.previousGlyph.naked().getRepresentation("defconAppKit.NSBezierPath")
            dt.save()
            dt.translate(self.currentGlyph.width)
            path.fill()
            dt.restore()
    
    def draw(self, info):
        # scale = info["scale"]
        fillColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0, 0.5)
        fillColor.set()
        self.drawGlyph()
    
    def drawPreview(self, info):
        fillColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0, 1)
        fillColor.set()
        self.drawGlyph()
    
    def drawInactive(self, info):
        fillColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0, 0.25)
        fillColor.set()
        self.drawGlyph()
            
    def inBounds(self, loc, bounds, boundsOffset=0):
        if (bounds[0] + boundsOffset) <= loc[0] <= (bounds[2] + boundsOffset):
            if bounds[1] <= loc[1] <= bounds[3]:
                return True
        return False
        
    def mouseDown(self, info):
        if not self.currentGlyph == None:
            if info["clickCount"] == 2:
                mouseLoc = (info["point"].x, info["point"].y)
                if not self.previousGlyph == None:
                    # There's a previous glyph being drawn, check to see if the double click is in its bouds
                    if self.inBounds(mouseLoc, self.previousGlyph.bounds, self.currentGlyph.width):
                        cgw = CurrentGlyphWindow()
                        cgw.setGlyphByName(self.previousGlyph.name)
                else:
                    # Check the components
                    for c in self.currentGlyph.components:
                        if c.selected: # First click should select it
                            if self.inBounds(mouseLoc, c.bounds):
                                self.didSwitch = True
                                cgw = CurrentGlyphWindow()
                                cgw.setGlyphByName(c.baseGlyph)
                                
CompoonentSwitcher()

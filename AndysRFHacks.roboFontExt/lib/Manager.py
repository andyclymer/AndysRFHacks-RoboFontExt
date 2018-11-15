from AppKit import NSColor, NSFont, NSMiniControlSize, NSSmallControlSize, NSRegularControlSize, NSMutableAttributedString, NSForegroundColorAttributeName, NSFontAttributeName
import os
import sys
from mojo.extensions import getExtensionDefault, setExtensionDefault
import vanilla
from WebKit import WebView


KEYPREFIX = "com.andyclymer.andysHacks"


def text_SmallGray(text):
    size = NSSmallControlSize # NSMiniControlSize
    attrs = {}
    attrs[NSForegroundColorAttributeName] = NSColor.grayColor()
    string = NSMutableAttributedString.alloc().initWithString_attributes_(text, attrs)
    #attrs[NSFontAttributeName] = NSFont.boldSystemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
    attrs[NSFontAttributeName] = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
    attributedString = NSMutableAttributedString.alloc().initWithString_attributes_(text, attrs)
    return attributedString
    
    
def text_Gray(text):
    size = NSRegularControlSize
    attrs = {}
    attrs[NSForegroundColorAttributeName] = NSColor.grayColor()
    string = NSMutableAttributedString.alloc().initWithString_attributes_(text, attrs)
    #attrs[NSFontAttributeName] = NSFont.boldSystemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
    attrs[NSFontAttributeName] = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
    attributedString = NSMutableAttributedString.alloc().initWithString_attributes_(text, attrs)
    return attributedString
    
def text_Bold(text):
    size = NSRegularControlSize
    attrs = {}
    string = NSMutableAttributedString.alloc().initWithString_attributes_(text, attrs)
    attrs[NSFontAttributeName] = NSFont.boldSystemFontOfSize_(NSFont.systemFontSizeForControlSize_(size))
    attributedString = NSMutableAttributedString.alloc().initWithString_attributes_(text, attrs)
    return attributedString
    



class ScriptManagerWindow:
    
    def __init__(self):
        self.fullMetadata = getExtensionDefault("%s.scriptMetadata" % KEYPREFIX, fallback={})
        if not len(self.fullMetadata.keys()):
            # "Restart" window
            self.w = vanilla.Window((500, 160), "Andy’s RoboFont Hacks")
            self.w.hr = vanilla.HorizontalLine((10, -50, -10, 1))
            self.w.restartText = vanilla.TextBox((20, 20, -20, -45), text_Bold("Installed and updated.\nRestart RoboFont to refresh the list of my RoboFont hacks.\n\n    — Andy Clymer"))
            self.w.okButton = vanilla.Button((-120, -35, 100, 20), "OK", callback=self.cancelCallback)
            self.w.open()
        
        else:
            # Full window
            self.w = vanilla.Window((750, 300), "Andy’s RoboFont Hacks")
            columnDescriptions=[
                {"title": "state", "width":20, "cell": vanilla.CheckBoxListCell()}, 
                {"title": "longName"}]
            self.w.scriptList = vanilla.List((10, 10, 300, -60), 
                [], 
                allowsMultipleSelection=False,
                showColumnTitles=False,
                selectionCallback=self.listSelectionChanged,
                columnDescriptions=columnDescriptions)
        
            self.defaultTitle = "Andy’s RoboFont Hacks"
            self.defaultText = "A selection of extras that make RoboFont work the way I like it. \n\nEverything is optional, click on one of the names on the left for a description of what the add-on does. Select as many as you like by checking the box to the left of the name, and restart RoboFont to activate.\n\n    — Andy Clymer"
            self.w.descriptionBox = vanilla.Box((320, 10, -10, -60))
            self.w.descriptionBox.title = vanilla.TextBox((5, 5, -10, 25), self.defaultTitle)
            self.w.descriptionBox.text = vanilla.TextBox((5, 38, -10, -10), self.defaultText)
            #self.w.webView = WebView.alloc().initWithFrame_(((0, 0), (320, 1000)))
            #self.w.scroll = vanilla.ScrollView((320, 10, -10, -60), self.w.webView, hasHorizontalScroller=False, hasVerticalScroller=False)
            #self.w.webView.setMainFrameURL_(self.htmlPath)
        
            self.w.hr = vanilla.HorizontalLine((10, -50, -10, 1))
            self.w.changeNote = vanilla.TextBox((20, -32, -230, 25), text_SmallGray("Any change will require restarting RoboFont."), sizeStyle="small")
            self.w.cancelButton = vanilla.Button((-230, -35, 100, 20), "Cancel", callback=self.cancelCallback)
            self.w.applyButton = vanilla.Button((-120, -35, 100, 20), "Apply", callback=self.applyCallback)
            self.populateList()
            self.w.open()
        
    
    def populateList(self):
        scriptListData = []
        scriptNames = list(self.fullMetadata.keys())
        scriptNames.sort()
        for shortName in scriptNames:
            scriptMetadata = {}
            scriptMetadata["shortName"] = shortName
            scriptMetadata["longName"] = self.fullMetadata[shortName]["longName"]
            scriptMetadata["state"] = self.getState(shortName)
            scriptListData += [scriptMetadata]
        self.w.scriptList.set(scriptListData)
        
    def getState(self, scriptName):
        stateKey = "%s.%s-state" % (KEYPREFIX, scriptName)
        return(getExtensionDefault(stateKey, fallback=False))
    
    def setState(self, scriptName, state):
        stateKey = "%s.%s-state" % (KEYPREFIX, scriptName)
        return(setExtensionDefault(stateKey, state))
        
    def listSelectionChanged(self, sender):
        selection = sender.getSelection()
        if not len(selection):
            self.w.descriptionBox.title.set(text_Bold(self.defaultTitle))
            self.w.descriptionBox.text.set(self.defaultText)
        else:
            idx = selection[0]
            selectedName = sender.get()[idx]["shortName"]
            self.w.descriptionBox.title.set(text_Bold(self.fullMetadata[selectedName]["longName"]))
            self.w.descriptionBox.text.set(self.fullMetadata[selectedName]["description"])
        
    def cancelCallback(self, sender):
        self.w.close()
    
    def applyCallback(self, sender):
        optionList = self.w.scriptList.get()
        for scriptOption in optionList:
            self.setState(scriptOption["shortName"], scriptOption["state"])
        self.w.close()
    
    
ScriptManagerWindow()

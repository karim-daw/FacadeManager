# Give your component a unique name and nickname (portrayed on the canvas).
ghenv.Component.Name = "FM-CreatePanels"
ghenv.Component.NickName = "FM-CP"

# Keep it in the "Performing" tab
ghenv.Component.Category = "FM-Python"

# Define the subcategory
ghenv.Component.SubCategory = "2-Build"

# If you want to give the component a version number etc.
import time
import Rhino.Geometry as rg
import math
import scriptcontext as rs
import System.Collections.Generic.IEnumerable as IEnumerable

ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")

# Your code here

Utilities = rs.sticky["Fm-Utilities"]()
Panel = rs.sticky["Fm-Panel"]()

print(Utilities.message)
Panel.MakeMessage()

print(Panel.message)
print("hello")


c = []

class FmBuilding:

    def __init__(self,brep,gfHeight,fHeight):

        # properties
        self.brep = brep
        self.gfHeight = gfHeight
        self.fHeight = fHeight

        self.maxHeight = None
        self.minHeight = None
        self.floorHeights = []

    def CreateFloorHeights(self):
        """create series of numbers based on height of breps and inputed numbers"""

        # get max and min height
        self.minHeight = Utilities.GetMinHeight(self.brep)
        self.maxHeight = Utilities.GetMaxHeight(self.brep)

        maxCount = int(math.floor(self.maxHeight/self.fHeight))
        
        # add first floor height to list
        self.floorHeights = []
        
        counter = self.minHeight
        for i in range(0,maxCount):
            if i == 0:
                self.floorHeights.append(self.minHeight)
                counter = counter + self.gfHeight
                counter = round(counter,1)
                
            if i > 0 and i < maxCount:
                if counter < self.maxHeight - self.fHeight:
                    self.floorHeights.append(counter)
                    counter += self.fHeight
                    counter = round(counter,1)
        print("floor heights are:")
        print(self.floorHeights)


    def CreateWindowBays(self,facadeGridSize):
        """ creates surface representation of each facade per floor"""

        # Create Floor Heights
        self.CreateFloorHeights()

        # Countour Surface
        floorCurves = Utilities.ContourBrep(self.brep,self.floorHeights)

        # Split brep
        splitBreps = Utilities.SplitBrep(self.brep,floorCurves)

        windowPanels = []
        for i, sBrep in enumerate(splitBreps):
            print("helloooooo i am a type of...")
            print(type(sBrep))
            # Compute window curvers
            windowCurves = Utilities.ContourSurface(sBrep,facadeGridSize)
            splitSurfaces = Utilities.SplitBrep(sBrep,windowCurves)
            for splitSurface in splitSurfaces:
                windowPanels.append(splitSurface)
            #windowPanels.append(sBrep)

        return windowPanels

    
    def SplitBays(self):
        """ Split breps (window bays) by a gride size number using the tangent of brep """
        pass
    
    def GroupPanelsByOrientation(self):
        """ returns a direcionary where the key is the orientation, and the value is a list of panels """
        pass
    

a = []
b = []
for brep in Breps:

    fb = FmBuilding(brep,GroundFloorHeight,FloorHeight)

    windowBays = fb.CreateWindowBays(GridSize)
    for wBay in windowBays:
        b.append(wBay)


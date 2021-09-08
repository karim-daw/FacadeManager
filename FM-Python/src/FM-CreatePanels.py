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
import System
import System.Collections.Generic.IEnumerable as IEnumerable

ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")

# Your code here


class FmBuilding:

    def __init__(self,brep,gfHeight,fHeight):

        # properties
        self.brep = brep
        self.gfHeight = gfHeight
        self.fHeight = fHeight

        self.maxHeight = None
        self.minHeight = None
        self.floorHeights = []

    def GetMaxHeight(self):
        """get max height of brep"""

        # create bbox for brep
        bbox = self.brep.GetBoundingBox(True)
        
        # Get max z component
        self.maxHeight = round( (bbox.Max.Z) ,2)
        
    def GetMinHeight(self):
        """get min height of brep"""

        # create bbox for brep
        bbox = brep.GetBoundingBox(True)
        
        # Get max z component
        self.minHeight = round( (bbox.Min.Z) ,2)

    def CreateFloorHeights(self):
        """create series of numbers based on height of breps and inputed numbers"""

        # get rest count
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


    def ContourBrep(self):
        """contour brep and outputs curves"""

        fCurves = []
        for ht in self.floorHeights:

            # construct point from heights
            minPnt = rg.Point3d(0,0,ht)
            
            # create plane at Z = ht
            pln = rg.Plane(minPnt,rg.Vector3d(0,0,1))
            
            # get curves and join them
            crvs = rg.Intersect.Intersection.BrepPlane(brep,pln,0.01)[1]
            
            # NEED TO FIX THIS, have to write function that takes in varying sizes of inputs
            if crvs.Count == 1:
                fCurves.append(rg.Curve.JoinCurves(crvs)[0])
            else:
                for crv in crvs:
                    fCurves.append(crv)
            
        return fCurves
    
    def SplitBrep(self):
        """split brep by a set of curves"""

        crvs = self.ContourBrep()
        splitBreps = self.brep.Split.Overloads[IEnumerable[rg.Curve], System.Double](crvs,0.01)

        explodeBreps = []
        for i, splitBrep in enumerate(splitBreps):
            # Get faces from breps
            for j, face in enumerate(splitBrep.Faces):          
                # turn it into brep 
                dupFace = rg.BrepFace.DuplicateFace(face,False)
                explodeBreps.append(dupFace)

        return explodeBreps



a = []
b = []
for brep in Breps:

    fb = FmBuilding(brep,GroundFloorHeight,FloorHeight)
    fb.GetMaxHeight()
    fb.GetMinHeight()
    fb.CreateFloorHeights()
    curves = fb.ContourBrep()
    for curve in curves:
        a.append(curve)
    
    sBreps = fb.SplitBrep()
    for sBrep in sBreps:
        b.append(sBrep)

Panel = rs.sticky["Fm-Panel"]
PanelObject = Panel()
PanelObject.MakeMessage()

print(PanelObject.message)
print("hello")

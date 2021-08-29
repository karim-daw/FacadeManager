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

ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")

# Your code here

def GetMaxHeight(brep):
    """get max height of brep"""

    # create bbox for brep
    bbox = brep.GetBoundingBox(True)
    
    # Get max z component
    maxHeight = bbox.Max.Z
    
    return maxHeight

def GetMinHeight(brep):
    """get min height of brep"""

    # create bbox for brep
    bbox = brep.GetBoundingBox(True)
    
    # Get max z component
    minHeight = bbox.Min.Z
    
    return minHeight

def CreateFloorHeights(brep,gfHeight,fHeight):
    """create series of numbers based on height of breps and inputed numbers"""
    
    # compute max and min height
    maxHeight = round(GetMaxHeight(brep),2)
    minHeight = round(GetMinHeight(brep),2)

    # get rest count
    maxCount = int(math.floor(maxHeight/fHeight))
    
    # add first floor height to list
    floorHeights = []
    
    counter = minHeight
    for i in range(0,maxCount):
        if i == 0:
            floorHeights.append(minHeight)
            counter += gfHeight
            counter = round(counter,1)
            
        if i > 0 and i < maxCount:
            if counter < maxHeight - fHeight:
                floorHeights.append(counter)
                counter += fHeight
                counter = round(counter,1)

    return floorHeights

def ContourBrep(brep,fHeights):
    
    fCurves = []
    for ht in fHeights:

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


a = []
for brep in Breps:
    
    heights = CreateFloorHeights(brep,GroundFloorHeight,FloorHeight)
    #print(heights)
    curves = ContourBrep(brep,heights)
    for crv in curves:
        
        a.append(crv)

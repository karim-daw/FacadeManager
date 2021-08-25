"""
This function takes in a list of breps, and outputs a meshface grid on all facade surfaces of the breps
    Inputs:
        Breps: Breps massing representation of design {list:Brep}
        GridSize: Number indicated facade grid spacing {item:float}
    Outputs:
        MeshPanels: A nested list of mesh faces {list[list]:Mesh}
        
        Version: 260821001
        Author: Karim Daw
        License: Apache License 2.0
        Version: 290621000
    
"""

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

def CreateFloorHeights(brep,gfHeight,fHeight):
    
    """create series of numbers based on height of breps and inputed numbers"""
    
    # compute max height
    maxHeight = round(GetMaxHeight(brep),2)
    print(maxHeight)
    
    # get rest count
    maxCount = int(math.floor(maxHeight/fHeight))
    
    # add first floor height to list
    floorHeights = []
    
    counter = 0
    for i in range(0,maxCount):
        if i == 0:
            floorHeights.append(0)
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
        
        # getting minimum height
        minHeight = brep.GetBoundingBox(True).Min.Z
        minPnt = rg.Point3d(0,0,ht)
        
        # create plane at Z = ht
        pln = rg.Plane(minPnt,rg.Vector3d(0,0,1))
        
        # get curves and join them
        crvs = rg.Intersect.Intersection.BrepPlane(brep,pln,0.01)[1]
        jCrvs = rg.Curve.JoinCurves(crvs)[0]

        fCurves.append(jCrvs)
    return fCurves

a = []
for brep in Breps:
    
    heights = CreateFloorHeights(brep,GroundFloorHeight,FloorHeight)
    #print(heights)
    curves = ContourBrep(brep,heights)
    for crv in curves:
        
        a.append(crv)

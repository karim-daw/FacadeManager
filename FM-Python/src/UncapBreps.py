"""
Uncaps breps and return breps without top or bottom surfaces
-
    Args:
        CappedBreps: Breps to uncap {list,Breps}
        Tolerance: A number indicating the tolerance by which we cull the surfaces we dont want appearing {item,number}
    Returns:
        UnCappedBreps: List of uncapped Breps {list,Breps}
        TopSurface: Top surface as a Brep {item, Brep}
        BottomSurface: Bottom surface as a Brep {item, Brep}
    Remarks:
        Author: Karim Daw (BIG IDEAS)
        Project: EDUES
        License:
        Version: 250604001
"""

# Give your component a unique name and nickname (portrayed on the canvas).
ghenv.Component.Name = "UncapBreps"
ghenv.Component.NickName = "UB"

# Keep it in the "Performing" tab
ghenv.Component.Category = "FM-Python"

# Define the subcategory
ghenv.Component.SubCategory = "1-Utilities"

import time
import math
import Rhino
import Grasshopper as gh


# If you want to give the component a version number etc.
ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")



def unCapBreps(breps, tol):
    

    # Init empty list of unCappedBreps
    unCappedBreps = []
    bottomSurfaces = []
    topSurfaces = []
    
    # Loop through breps
    for i, brep in enumerate(breps):
        
        unCappedBrep = []
        
        # Init empty breps
        bottomSurface = Rhino.Geometry.Brep
        topSurface = Rhino.Geometry.Brep

        # Get faces from breps
        for j, face in enumerate(brep.Faces):
            
            # Evaluate surface
            vec = face.NormalAt(0.5, 0.5)
            
            # Check if normal is pointing up or down within tolerance
            if vec.Z <= 0 + tol and vec.Z >= 0 - tol:
                
                # Append to empty list
                unCappedBrep.append(face)
                
            elif vec.Z <= 0:
                bottomSurface = face
                
                # Append bottom master list of Top Brep(s)
                bottomSurfaces.append(bottomSurface)
                
            elif vec.Z >= 0:
                topSurface = face
                # Append top master list of Top Brep(s)
                topSurfaces.append(topSurface)
        
        # Append Uncapped Brep to master list of Uncapped Brep(s)
        unCappedBreps.append(unCappedBrep)

        
    # return tuple with all the stuff you want
    nestedGeo = [unCappedBreps,topSurfaces,bottomSurfaces]
    
    return nestedGeo

# check if user input anything
if not Tolerance:
    Tolerance = 0.01

if CappedBreps:
    nestedGeo = unCapBreps(CappedBreps,Tolerance)
    # Unnest objects
    unCappedBreps = []
    packedBreps = nestedGeo[0]
    
    for brepFaces in packedBreps:
        for brepFace in brepFaces:
            
            # Convert BrepFace into regulary brep for joining
            #brep = Rhino.Geometry.BrepFace.DuplicateFace(brepFace,False)
            
            brep = Rhino.Geometry.Brep.CreateFromOffsetFace(brepFace,OffsetDistance,0.0,False,False)
            
            # Add to unCappedBreps
            unCappedBreps.append(brep)
            
    TopSurface = nestedGeo[1]
    BottomSurface = nestedGeo[2]
    
    if OffsetDistance > 0.0:
        VerticalSurfaces = unCappedBreps
    else:
        VerticalSurfaces = Rhino.Geometry.Brep.JoinBreps(unCappedBreps,0.01)
else:
    VerticalSurfaces = []




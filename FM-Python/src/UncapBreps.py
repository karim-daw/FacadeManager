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

def unCapBrep(brep, offsetDis, tol):
    
    verticalSurfaces = []
    bottomSurface = Rhino.Geometry.Brep()
    topSurface = Rhino.Geometry.Brep()
    
    # Get faces from breps
    for i, face in enumerate(brep.Faces):
        
        # Evaluate Surface
        vec = face.NormalAt(0.5,0.5)
        
        # Check if normal is pointing up or down within tolerance
        if vec.Z <= 0 + tol and vec.Z >= 0 - tol:
            
            b = Rhino.Geometry.BrepFace.DuplicateFace(face,False)
            
            # Append to vertical
            verticalSurfaces.append(b)
        
        elif vec.Z <= 0:
            
            # Append top master list of top brep
            bottomSurface = face
  
        elif vec.Z >= 0:

            # Append top master list of top brep
            topSurface = face
    
    # Join vertical surface
    band = Rhino.Geometry.Brep.JoinBreps(verticalSurfaces,0.01)
    
    
    if offsetDis != 0.0:
        
        # Unpack band
        band = band[0]
        
        # offsetBand gives back 3 things, i just want the first one
        offsetBand = Rhino.Geometry.Brep.CreateOffsetBrep(band,offsetDis,False,False,False,0.01)
        offsetBand = offsetBand[0]
    
    else:
        offsetBand = band


    return offsetBand, bottomSurface, topSurface


# Run
# Default inputs


if not Tolerance:
    Tolerance = 0.01
if not OffsetDistance:
    OffsetDistance = 0.5

if CappedBreps:
    
    VerticalSurfaces = []
    TopSurface = []
    BottomSurface = []

    for b in CappedBreps:
        
        vS, tS, bS = unCapBrep(b,-1*OffsetDistance,0.01)
        
        # save surfaces
        VerticalSurfaces.append(*vS)
        TopSurface.append(tS)
        BottomSurface.append(bS)


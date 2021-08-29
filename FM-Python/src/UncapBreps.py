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

def unCapBrep(brep,tol):
    
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

    joinedVerticalSurfaces = []
    if len(band) == 1:
        joinedVerticalSurfaces.append(band)
    else:
        for ban in band:
            joinedVerticalSurfaces.append(ban)

    return joinedVerticalSurfaces, bottomSurface, topSurface


def OffsetJoinedBreps(brep,offsetDis):
    
    if offsetDis != 0.0:
        offsetBrep = Rhino.Geometry.Brep.CreateOffsetBrep(brep,offsetDis,False,True,False,0.01)
        return offsetBrep[0][0]
    else:
        return brep


if not Tolerance:
    Tolerance = 0.01
if not OffsetDistance:
    OffsetDistance = 0.0

if CappedBreps:
    
    VerticalSurfaces = []
    TopSurface = []
    BottomSurface = []

    for b in CappedBreps:
        
        vS, tS, bS = unCapBrep(b,Tolerance)
        print(len(vS))
        # save surfaces
        if len(vS) == 1:
            VerticalSurfaces.append(OffsetJoinedBreps(vS[0][0],-1*OffsetDistance))
        else:
            for v in vS:
                VerticalSurfaces.append(OffsetJoinedBreps(v,-1*OffsetDistance))
        TopSurface.append(tS)
        BottomSurface.append(bS)


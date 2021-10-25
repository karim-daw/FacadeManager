"""
Template for the creation of user objects for the Big Ideas tab. This text shows up as the component's description. In order to create an icon, drag+drop 24x24 pixel png onto component. Save them under L:\TOOLS\SOURCECODE\Icons
-
    Args:
        A: This is how to create a tool tip.
    Returns:
        B: This is how to create a tool tip.
        
        
        Version: 280621
"""

# Give your component a unique name and nickname (portrayed on the canvas).
ghenv.Component.Name = "FM-FacadeManager"
ghenv.Component.NickName = "FM-FM"

# Keep it in the "Performing" tab
ghenv.Component.Category = "FM-Python"

# Define the subcategory
ghenv.Component.SubCategory = "Facade-Manager"

# If you want to give the component a version number etc.
import time
import Rhino
import Rhino.Geometry as rg
import scriptcontext as rs
import System
import System.Collections.Generic.IEnumerable as IEnumerable

ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")




# Your code here
#THIS IS A TEST

class Panel:

    def __init__(self):

        self.message = "didnt work"

    def MakeMessage(self):

        self.message = "hello, i am a panel! Hooray!"




################################### Utilities functions ########################################


class Utilities:

    def __init__(self):

        self.message = "using utitlity class"
    

    def GetMinHeight(self,brep):

        """get min height of brep"""

        # create bbox for brep
        bbox = brep.GetBoundingBox(True)
        
        # Get max z component
        minHeight = round( (bbox.Min.Z) ,2)

        return minHeight
    

    def GetMaxHeight(self,brep):

        """get max height of brep"""

        # create bbox for brep
        bbox = brep.GetBoundingBox(True)
        
        # Get max z component
        maxHeight = round( (bbox.Max.Z) ,2)

        return maxHeight
    
    def ComputeSurfaceNormal(self,surface):

        """ computes surface normal and returns unit vector"""

        normal = surface.NormalAt(0.5,0.5)
        normal.Unitize

        return normal
    
    def ComputeSurfaceTangent(self,normalVector):

        """ computes vector perpendicular to input vector """

        # if vector is pointing up, use x or y axis as corss vector
        if normalVector.Z == 1:
            crossVector = rg.Vector3d(0, 1, 0)
        elif normalVector.Z == -1:
            crossVector = rg.Vector3d(0, 1, 0)
        else:
            crossVector = rg.Vector3d(0, 0, 1)

        # compute cross product
        tangent = rg.Vector3d.CrossProduct(normalVector, crossVector)
        tangent.Unitize

        return tangent
    

    def ContourBrep(self,brep,stepSizes):

        """ contour brep along upwards with a given set of step sizes and return list of curves"""
        
        cCurves = []
        for step in stepSizes:

            # contruct point from stepSizes
            pnt = rg.Point3d(0,0,step)

            # create plane
            pln = rg.Plane(pnt, rg.Vector3d(0,0,1))

            # get curves and join them
            crvs = rg.Intersect.Intersection.BrepPlane(brep,pln,0.01)[1]

            # NEED TO FIX THIS, have to write function that takes in varying sizes of inputs
            if crvs.Count == 1:
                cCurves.append(rg.Curve.JoinCurves(crvs)[0])
            else:
                for crv in crvs:
                    cCurves.append(crv)
            
        return cCurves

    
    def ContourSurface(self,surface,stepSizes,direction):

        """ contour a single surfac by given step sizes and direction and returns a list of curves"""

        # compute Normal
        nrml = self.ComputeSurfaceNormal(surface)

        # compute Tangent
        tngt = self.ComputeSurfaceTangent(nrml)

        # compute first point on surface
        fSurfacePnt = surface.PointAt(0.5,0.5)

        # loop through steps
        vCurves = []
        for i, step in enumerate(stepSizes):

            # create tangent move vector
            mVec = tngt * i

            # contruct point from stepSizes
            pnt = fSurfacePnt + mVec

            # contruct plane
            pln = rg.Plane(pnt,tngt)

            # get curves and join them
            crv = rg.Intersect.Intersection.BrepPlane(surface,pln,0.01)[1]

            # NEED TO FIX THIS, not sure if we need to join them
            vCurves.append(crv)
            
        return vCurves

    def SplitBrep(self,brep,curves):

        """split brep by a set of curves"""

        splitBreps = self.brep.Split.Overloads[IEnumerable[rg.Curve], System.Double](curves,0.01)

        explodeBreps = []
        for i, splitBrep in enumerate(splitBreps):
            # Get faces from breps
            for j, face in enumerate(splitBrep.Faces):          
                # turn it into brep 
                dupFace = rg.BrepFace.DuplicateFace(face,False)
                explodeBreps.append(dupFace)

        return explodeBreps


rs.sticky["Fm-Panel"] = Panel
rs.sticky["Fm-Utilities"] = Utilities 

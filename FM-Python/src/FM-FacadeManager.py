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

ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")

# Your code here
#THIS IS A TEST

class Panel:

    def __init__(self):

        self.message = "didnt work"

    def MakeMessage(self):

        self.message = "hello, i am a panel! Hooray!"


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
    
    def ComputeSurfaceTangent(self,surface):
        pass
    
    def ContourBrep(self,brep,stepSizes,direction):
        pass

    def SplitBrep(self,brep,crvs):
        pass
    


rs.sticky["Fm-Panel"] = Panel
rs.sticky["Fm-Utilities"] = Utilities 

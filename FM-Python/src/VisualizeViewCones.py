"""
Given a nested list of Rays, this function draws a percentage of the view cones as lines 
    Args:
        Rays: Nested Lists of Rays to use for raytrace {list[list]:ray3d}
        Amplitude: Length of the drawn ray line {item:int}
        Percentage: Percentage of cones you want to see {item:float}
        Run: Set to "True" to run calculation {item:bool}
    Returns:
        ViewLines: List of lines representating view cone rays {list:line3d}
        ViewVectors: List of vectors representating view cones rays {list:vector3d}
    Remarks:
        Author: Karim Daw 
        Project: Facade-Manager
        License:
        Version: 230621
"""

# Give your component a unique name and nickname (portrayed on the canvas).
ghenv.Component.Name = "VisualizeViewCones"
ghenv.Component.NickName = "VVC"

# Keep it in the "Performing" tab
ghenv.Component.Category = "FM-Python"

# Define the subcategory
ghenv.Component.SubCategory = "3-Performance"
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import random


def VisualizeRays(raysToVisualize,amplitude,percentage):

    # check if Percentange given, otherise set default to 0.1
    if percentage == None:
        percentage = 0.1
    
    if raysToVisualize == None:
        pass
    else:
        viewLines = []
        viewVectors = []
        
        raysToVisCount = len(raysToVisualize)
        
        # shuffle list 
        random.shuffle(raysToVisualize)
        
        # multiply list length by percentage to get reduced list length
        reduceListCount = raysToVisCount * Percentage
        
        #convert to int
        limit = int(reduceListCount)
        
        for i, raysList in enumerate(raysToVisualize):
            
            # set limit from percentage
            if i > limit:
                break
            
            vectors = []
            
            for j, ray in enumerate(raysList):
        
                # get position of ray
                pos = ray.Position
                
                # get vector of ray
                vector = ray.Direction
                vectors.append(vector)
                
                # move pos by vector by amplitutde provided
                movedPos = ( pos  + (vector * amplitude) )
                
                # create line
                line = rg.Line(pos,movedPos)
                
                # output vectors as lines
                viewLines.append(line)
            
            viewVectors.append(vectors)

    return viewLines, viewVectors


# Run function
if Run:
    ViewLines, ViewVectors = VisualizeRays(RaysToVisualize,Amplitude,Percentage)

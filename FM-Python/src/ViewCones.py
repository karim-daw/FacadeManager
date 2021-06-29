"""
Generates a nest list where each list, contains a list of rays equivalent the view cone at the given test points
-
    Args:
        AnalysisMesh: Mesh representing object you want to perform view analysis on for each mesh face {item:mesh}
        ViewAngle: Angle range. If None, 120 degrees is used {item,float,optional}
        Obstacles: Breps or Meshes to be used as viewing Obstacles, be sure to include the objects from which you are testing the views from {List,Mesh/Brep}
        ViewFromObject: Brep or Mesh where the points are viewed from {item,Mesh/Brep}
        DistanceLimit: A distance you would like to limit the view to, if None, 100meters is isued {item,float, optional}
    Returns:
        Rays: A nested list containing a list or ray3ds for each analysis point {list[list],ray3d}
        RayCountPerPoint: A list of numbers referring to amount of hits each ray of each analysis point receives of the target mesh {list,int}  
    Remarks:
        Author: Karim Daw , Guillaume Evain
        Project: 
        License:
        Version: 210629000
"""

# Give your component a unique name and nickname (portrayed on the canvas).
ghenv.Component.Name = "ViewCones"
ghenv.Component.NickName = "VC"

# Keep it in the "BigIdeas" tab
ghenv.Component.Category = "FM-Python"

# Define the subcategory
ghenv.Component.SubCategory = "3-Performance"

# If you want to give the component a version number etc.
import time
import math
import Rhino
import ghpythonlib.parallel
import ghpythonlib.treehelpers as th

ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")

# Compute Z vector
zVec = Rhino.Geometry.Vector3d(0,0,1)

def getAnalysisLocations(mesh):
    
    """ 
    Gets and offset mesh face centers by normal and return both
    """
    
    # Check and build facenormals
    if mesh.FaceNormals.Count == 0:
        mesh.FaceNormals.ComputeFaceNormals()
    
    faces = mesh.Faces
    normals = list(mesh.FaceNormals)
    centers = []
    
    for i in range(faces.Count):
        cPt = faces.GetFaceCenter(i)
        n = normals[i]
        centers.append(cPt)
        
    return centers,normals


def computeRays(points,vectors,angle,angleStepSize):
        
    """ 
    Computes the a cone of rays on eachm esh face centers
    """
    
    #init dictionary
    rayByPoint = []

    # Create number range
    min = int(math.floor(angle * -0.5))
    max = int(math.ceil(angle * 0.5)) + angleStepSize

    counter = 0
    for i, point in enumerate(points):

        # Get partnering vectors
        vector = vectors[i]
        
        # move point striaght forwards
        movedPoint = point + vector
        
        # init list of rays for each point
        rays = []
        
        # Rotate vector
        for j in range(min,max,angleStepSize):
            
            # Convert to Radians
            angle = math.radians(j)
            
            # disgard middle vector for now
            if angle == 0:
                continue 
            
            # make a copy of vector
            rotVector = Rhino.Geometry.Vector3d(vector)
            
            # Rotate Vector
            rotVector.Rotate(angle,zVec)
            
            # Rotate Horizontal Vector Fan by 179 degrees
            for k in range(0,180,angleStepSize):
                
                angle2 = math.radians(k)
                
                # make a copy of vector
                rotVector2 = Rhino.Geometry.Vector3d(rotVector)
                
                rotVector2.Rotate(angle2,vector)
                ray = Rhino.Geometry.Ray3d(point,rotVector2)
                rays.append(ray)
                counter = counter + 1


            # append last ray
            lastRay = Rhino.Geometry.Ray3d(point,vector)
            rays.append(lastRay)
            
            counter = counter +1
            
        rayByPoint.append(rays)
        
    rayTree = th.list_to_tree(rayByPoint, source=[0,0])

    return rayByPoint

# compute rays
if Run:
    
    analysisPoints, analysisVectors = getAnalysisLocations(AnalysisMesh)
    Rays = computeRays(analysisPoints,analysisVectors,ViewAngle,AngleStepSize)
    
    #output message
    RayCountPerPoint = len(Rays[0])
    message = "Rays shot per analysis point: " + str(RayCountPerPoint)
    message += "\nTotal Rays Shot = " + str( RayCountPerPoint * len(Rays) )
    ghenv.Component.Message = message
else:
    Rays = []
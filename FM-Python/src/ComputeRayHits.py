"""
Given a nested list of Rays, this function computes the amount of rays per view point that hits the target mesh
    Args:
        Rays: Nested Lists of Rays to use for raytrace {list[list]:ray3d}
        TargetMesh: Mesh to be used as a target for View Ray calculation {item:mesh}
        ObstaclesMesh: Mesh to be used as Obstacles occluding the view of the target (dont forget self occluding objects) {item:mesh}
        Run: Set to "True" to run calculation {item:bool}
    Returns:
        HitCounts: The amount of hits each view point recieved for each of its view rays {list:int}
    Remarks:
        Author: Karim Daw 
        Project: EDUES
        License:
        Version: 230621
"""

# Give your component a unique name and nickname (portrayed on the canvas).
ghenv.Component.Name = "ComputeRayHits"
ghenv.Component.NickName = "CRH"

# Keep it in the "Performing" tab
ghenv.Component.Category = "FM-Python"

# Define the subcategory
ghenv.Component.SubCategory = "3-Performance"



import time
import Rhino
import ghpythonlib.treehelpers as th

# If you want to give the component a version number etc.
ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")


# Compute hits for every ray shot by view points
def calculateHits(nestedRays,targetMesh,obstaclesMesh):
    
    hitGroups = []
    
    # loop through nested lists of lists of rays
    for i, rays in enumerate(nestedRays):
        
        # start counter for hits
        hitAmount = 0
        
        #loop through rays
        for j, ray in enumerate(rays):
            
            
            hitTarget = Rhino.Geometry.Intersect.Intersection.MeshRay(TargetMesh,ray) > 0
            hitObstacle = Rhino.Geometry.Intersect.Intersection.MeshRay(ObstaclesMesh,ray) > 0
            if hitTarget and not hitObstacle:
                
                # Accumulate hit points
                hitAmount = hitAmount + 1

            else:
                pass
        hitGroups.append(hitAmount)

    print(len(hitGroups))
    #hitsAsTree = th.list_to_tree(hitGroups, source=[0,0])
    
    return hitGroups

# Call function
if Run:
    HitCounts = calculateHits(Rays,TargetMesh,ObstaclesMesh)
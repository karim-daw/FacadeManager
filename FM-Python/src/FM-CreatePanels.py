"""
This function takes in a list of breps, and outputs a meshface grid on all facade surfaces of the breps
    Inputs:
        Breps: Breps massing representation of design {list:Brep}
        GridSize: Number indicated facade grid spacing {item:float}
    Outputs:
        MeshPanels: A nested list of mesh faces {list[list]:Mesh}
        
        Version: 290621000
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
ghenv.Component.Message = time.strftime("%d/%m/%Y") + "\n" + time.strftime("%H:%M:%S")

# Your code here
#THIS IS A TEST
print("Hello Facade Manager")


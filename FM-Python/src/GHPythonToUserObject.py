"""
Iterates the GHPython components in the document and makes user objects of them
if the their Category property matches the input Category parameter. Also grabs
all the code and writes this to .py files.

    Input:
        Toggle: Activate the component using a boolean toggle {item,bool}
        Folder: The folder/directory to save the user objects and source code to {item,str}
        Category: The name of the category for which to make user objects {item,str}
    Output:
        TLOC: Lines of code in user object {item,int}
    Remarks:
        Author: Anders Holden Deleuran
        Contributor: Karim Daw
        License: Apache License 2.0
        Version: 250621
"""
ghenv.Component.Name = "GHPythonToUserObject"
ghenv.Component.NickName = "PTUO"
ghenv.Component.Category = "FM-Python"
ghenv.Component.SubCategory = "0-Dev"

import os
import Grasshopper as gh
import getpass

def ghPythonToUserObject(ghPyComp,writeFolder):
    
    """ 
    Automates the creation of a GHPython user object. Based on this thread:
    http://www.grasshopper3d.com/forum/topics/change-the-default-values-for-userobject-popup-menu
    """
    
    # Make a user object
    uo = gh.Kernel.GH_UserObject()
    
    # Set its properties based on the GHPython component properties
    uo.Icon = ghPyComp.Icon_24x24    
    uo.BaseGuid = ghPyComp.ComponentGuid
    uo.Exposure = ghenv.Component.Exposure.primary
    uo.Description.Name = ghPyComp.Name
    uo.Description.Description = ghPyComp.Description
    uo.Description.Category = ghPyComp.Category
    uo.Description.SubCategory = ghPyComp.SubCategory
    
    # Set the user object data and save to file
    uo.SetDataFromObject(ghPyComp)
    uo.Path = os.path.join(writeFolder,ghPyComp.Name+".ghuser")
    uo.SaveToFile()
    
    # Update the grasshopper ribbon UI (doesn't seem to work)
    #gh.Kernel.GH_ComponentServer.UpdateRibbonUI()

def exportGHPythonSource(ghPyComp,writeFolder):
    
    """ Export the source code of a GHPython component """
    
    # Get code and lines of code
    code = ghPyComp.Code
    code = code.replace("\r","")
    lines = code.splitlines()
    loc = len(lines)
    
    # Check/make source file folder
    srcFolder = os.path.join(writeFolder,"src")
    if not os.path.isdir(srcFolder):
        os.makedirs(srcFolder)
        
    # Write code to .py file
    srcFile = os.path.join(srcFolder,ghPyComp.Name + ".py")
    f = open(srcFile,"w")
    f.write(code)
    f.close()
    
    return loc

if Toggle and LocalFolder and Category:
    
    # Make GH component warning handler
    wh = gh.Kernel.GH_RuntimeMessageLevel.Warning
    
    # Get user name
    username=getpass.getuser()

    # get local GH componenet folder
    localGhFolder = "C:\Users\karimd\AppData\Roaming\Grasshopper\UserObjects"
 
    Folders = [LocalFolder,localGhFolder]
    
    # Iterate the canvas and get to the GHPython components
    TLOC = 0
    for obj in ghenv.Component.OnPingDocument().Objects:
        if type(obj) is type(ghenv.Component):
            
            # Check that category matches and export to files
            if obj.Category == Category:
                
                #loop through folders you want to save to
                for f in Folders:
                    ghPythonToUserObject(obj,f)
                    loc = exportGHPythonSource(obj,f)
                    TLOC += loc
                    obj.AddRuntimeMessage(wh,"I was just saved as a user object, hooray!")
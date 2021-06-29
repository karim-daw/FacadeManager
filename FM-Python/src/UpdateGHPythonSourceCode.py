"""
Updates the source code of GHPython components on the canvas with the code
in the .py files in the Folder if the GHPython component Name property is 
the same as the name of one of the .py files.

    Inputs:
        Toggle: Activate the component {item,bool}
        Folder: The location of the .py source code files {item,str}
    Outputs:
        GUIDS: List of GHPython component that were updated {list,str}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 210621000
"""
ghenv.Component.Name = "UpdateGHPythonSourceCode"
ghenv.Component.NickName = "UPSC"
ghenv.Component.Category = "FM-Python"
ghenv.Component.SubCategory = "0-Dev"

import os
import Grasshopper as gh

def getSrcCodeVersion(srcCode):
    
    """
    Attempts to get the first instance of the word "version" (or, "Version")
    in a multi line string. Then attempts to extract an integer from this line 
    where the word "version" exists. So format version YYMMDD in the GHPython 
    docstring like so (or any other integer system):
        
        Version: 160121
    """
    
    # Get first line with version in it
    srcCodeLower = srcCode.lower()
    verStr = [l for l in srcCodeLower.split('\n') if "version" in l]
    if verStr:
        
        # Get the first substring integer and return it
        verInt = [int(s) for s in verStr[0].split() if s.isdigit()]
        if verInt:
            return int(verInt[0])
    else:
        return None

def updateGHPythonSrc(srcFolder,ghDocument):
    
    """ 
    Update the source code of GHPython components in ghDocument with the code
    in the .py files in the srcFolder if the GHPython component Name property is 
    the same as the name of one of the .py files.
    """
    
    # Get python source files in folder
    pyFiles = [f for f in os.listdir(srcFolder) if f.endswith(".py")]
    
    # Make dictionary with script name as key and source code as value
    srcCode = {}
    for f in pyFiles:
        fOpen = open(os.path.join(srcFolder,f))
        fRead = fOpen.read()
        fName,fExt = os.path.splitext(f)
        srcCode[fName] = fRead
        
    # Make GH component warning handler
    wh = gh.Kernel.GH_RuntimeMessageLevel.Warning
    
    # Iterate the gh canvas and update ghpython source code
    guids = []
    for obj in ghDocument.Objects:
        if type(obj) is type(ghenv.Component):
            if obj.Name in srcCode:
                
                # Check that srcCode file has higher version number than obj source code
                srcCodeVer = getSrcCodeVersion(srcCode[obj.Name])
                objSrcVer = getSrcCodeVersion(obj.Code)
                if objSrcVer and srcCodeVer > objSrcVer:
                    
                    # Update the obj source
                    obj.Code = srcCode[obj.Name]
                    obj.AddRuntimeMessage(wh,"GHPython code was automatically updated, input/output parameters might have changed")
                    guids.append(str(obj.InstanceGuid))
                    
    return guids

if Toggle and Folder:
    GUIDS = updateGHPythonSrc(Folder,ghenv.Component.OnPingDocument())
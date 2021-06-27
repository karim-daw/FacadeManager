using System;
using System.Collections.Generic;

using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;

namespace FacadeManager
{
    public class GhcCreateBuildings : GH_Component
    {

        public GhcCreateBuildings()
          : base("CreateBuildings", "CB",
            "Converts breps into FM 'Building Objects'",
            "FM", "Build")
        {
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {

            pManager.AddBrepParameter("Breps", "B", "Breps to make into Buildings", GH_ParamAccess.list);

        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {

            pManager.AddGenericParameter("FM-Building", "FM-B", "Facade Manager Building Object", GH_ParamAccess.list);
            pManager.AddTextParameter("log", "myLogList", "debugging log", GH_ParamAccess.item);

        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {

            List<Brep> iBreps = new List<Brep>();

            DA.GetDataList(0,iBreps);

            //importing utilities
            Utilities util = new Utilities();
            util.CreateMassings(iBreps);
            List<Massing> massings = util.Massings;


            Dictionary<int, List<Massing>> dict = util.GroupMassing(massings);

            // get list
            List<String> myStrings = util.MyLog;

            // creating instance of building
            List<Building> myBuildings = new List<Building>();
            foreach (KeyValuePair<int, List<Massing>> entry in dict)
            {
                Building building = new Building(entry.Key, entry.Value);
                myBuildings.Add(building);
            }
            // Setting data
            DA.SetDataList(0, myBuildings);
            DA.SetDataList(1, myStrings);
        }

   


        public override GH_Exposure Exposure => GH_Exposure.primary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => null;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("61DE5447-51FB-4EE1-935C-C7ACFDDE7571");
    }
}

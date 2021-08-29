using Grasshopper;
using Grasshopper.Kernel;
using System;
using System.Drawing;

namespace FacadeManager
{
    public class FacadeManagerInfo : GH_AssemblyInfo
    {
        public override string Name => "FacadeManager";

        //Return a 24x24 pixel bitmap to represent this GHA library.
        public override Bitmap Icon => null;

        //Return a short string describing the purpose of this GHA library.
        public override string Description => "";

        public override Guid Id => new Guid("1F192467-494D-46B1-84FB-B8A01D4E8AD5");

        //Return a string identifying you or your company.
        public override string AuthorName => "";

        //Return a string representing your preferred contact details.
        public override string AuthorContact => "";
    }
}
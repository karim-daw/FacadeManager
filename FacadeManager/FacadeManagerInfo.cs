using System;
using System.Drawing;
using Grasshopper;
using Grasshopper.Kernel;

namespace FacadeManager
{
    public class FacadeManagerInfo : GH_AssemblyInfo
    {
        public override string Name => "FacadeManager";

        //Return a 24x24 pixel bitmap to represent this GHA library.
        public override Bitmap Icon => null;

        //Return a short string describing the purpose of this GHA library.
        public override string Description => "";

        public override Guid Id => new Guid("B82B6471-D9F2-430C-B5F2-D6084F56AD33");

        //Return a string identifying you or your company.
        public override string AuthorName => "";

        //Return a string representing your preferred contact details.
        public override string AuthorContact => "";
    }
}

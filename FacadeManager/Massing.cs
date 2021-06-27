using System;
using Rhino.Geometry;
using Rhino.Geometry.Collections;
using System.Collections.Generic;

namespace FacadeManager
{
    public class Massing
    {
        public Brep Brep;
        public Point3d CPnt;

        public Massing(Brep brep)
        {
            Brep = brep;
            CPnt = brep.GetBoundingBox(false).PointAt(0.5, 0.5, 0.5);
        }

        
    }
}

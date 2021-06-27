using System;
using Rhino.Geometry;
using Rhino.Geometry.Collections;
using System.Collections.Generic;


namespace FacadeManager
{
    public class Building
    {

        public List<Massing> Massings;
        public int BuildingNum;

        // Constructor
        public Building(int buildingNum,List<Massing> massings)
        {
            Massings = massings;
            BuildingNum = buildingNum;
        }

    }
}

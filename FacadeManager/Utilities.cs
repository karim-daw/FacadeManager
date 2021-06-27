using System;
using Rhino.Geometry;
using Rhino.Geometry.Collections;
using System.Collections.Generic;
using System.Linq;

namespace FacadeManager
{
    public class Utilities
    {
        public List<String> MyLog = new List<string>();
        public List<Massing> Massings = new List<Massing>();

        public Utilities()
        {

        }

        public Dictionary<int, List<Massing>> GroupMassing(List<Massing> massings)
        {
            // create dictionary {key = id : value = List<Breps>}
            Dictionary<int, List<Massing>> buildingList = new Dictionary<int, List<Massing>>();

            // init counter to be used as key
            int counter = 1;

            for (int i = 0; i < massings.Count; i++)
            {
                // Get center points and x and y
                Massing myMassing = massings[i];
                Point3d cPnt = myMassing.CPnt;
                double xC = cPnt.X;
                double yC = cPnt.Y;

                // check if dic is empty
                if (buildingList.Count == 0)
                {
                    List<Massing> myMassings = new List<Massing>() { myMassing };
                    buildingList[counter] = myMassings;
                }

                // check the center point of current massing to all the center points of all the breps in the dictionary
                else
                {
                    foreach (KeyValuePair<int, List<Massing>> entry in buildingList)
                    {
                        List<Massing> list = entry.Value.ToList();
                        for (int j = 0; j < list.Count; j++)
                        {
                            Massing massing = list[j];
                            Point3d cPnt2 = massing.CPnt;
                            double xC2 = cPnt2.X;
                            double yC2 = cPnt2.Y;

                            if (xC2 == xC && yC2 == yC)
                            {
                                List<Massing> massingCopy = buildingList[counter];
                                massingCopy.Add(massing);
                            }
                            else
                            {
                                counter++;
                                List<Massing> myMassings2 = new List<Massing>() { myMassing };
                                buildingList[counter] = myMassings2;
                            }
                        }
                    }

                }

            }

            return buildingList;
        }


        public void CreateMassings(List<Brep> breps)
        {

            for (int i = 0; i < breps.Count; i++)
            {
                Brep brep = breps[i];
                Massing massing = new Massing(brep);
                Massings.Add(massing);
            }

        }



        // saves strings to MyLog for debugging
        // Inputs:
        // {item : String}
        // Outputs:
        // {void} but saves to global string list
        public void SaveToLog(String str)
        {
            MyLog.Add(str);

        }
    }

}

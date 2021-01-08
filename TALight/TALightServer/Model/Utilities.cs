using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using TALightObjects;

namespace TALightServer.Model
{
    public class Utilities
    {
        public static bool CheckArguments(ConnectInfo connectInfo, List<Tuple<string, string>> list)
        {
            Problem problem = GetData.GetMeta(connectInfo.Folder);

            Service s = problem.Service.Find((x) => x.Name == connectInfo.Services);

            foreach (Tuple<string, string> x in list)
            {
                Regex r = new Regex(x.Item2);

                foreach (Arguments j in s.List)
                {
                    if (j.Name == x.Item1)
                    {
                        if (!r.IsMatch(x.Item2))
                        {
                            return false;
                        }
                    }
                }
            }

            return true;
        }

        internal static bool CheckService(string folder, string service)
        {
            Problem p = GetData.GetMeta(folder);

            foreach (Service x in p.Service)
            {
                if (x.Name == service)
                {
                    return true;
                }
            }

            return false;
        }
    }
}

using System;
using System.Collections.Generic;

namespace TALightObjects
{
    public class Utilities
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="s">Example: "a=2 b=4"</param>
        /// <returns></returns>
        public static List<Tuple<string, string>> TakeArguments(string s)
        {
            List<Tuple<string, string>> tmp = new List<Tuple<string, string>>();

            if (string.IsNullOrWhiteSpace(s))
            {
                return tmp;
            }

            // Remove more spaces
            s = s.Trim();
            while (s.Contains("  "))
            {
                s = s.Replace("  ", " ");
            }
            string[] splitd = s.Split(" ");

            foreach (string x in splitd)
            {
                string[] splity = x.Split("=");

                Tuple<string, string> t = new Tuple<string, string>(splity[0], splity[1]);
                tmp.Add(t);
            }

            return tmp;
        }
    }
}

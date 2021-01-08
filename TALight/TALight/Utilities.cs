using System;
using TALightObjects;

namespace TALight
{
    internal class Utilities
    {
        internal static void PrintArray<T>(T[] array)
        {
            foreach (T x in array)
            {
                Console.WriteLine(x.ToString());
            }
        }

        internal static string PrintConnectInfo(ConnectInfo info)
        {
            string s = info.Folder.Replace("%2F", "\\") + " -> " + info.Services + Environment.NewLine +
                TALightObjects.Constant.banner;

            return s;
        }
    }
}
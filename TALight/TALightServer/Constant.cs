using System;

namespace TALightServer
{
    public class Constant
    {
        public const string Folder = @"Local";
        public const string MetaFile = "meta.yaml";

        public static string Separator
        {
            get
            {
                return Environment.OSVersion.Platform switch
                {
                    PlatformID.Win32NT => @"\",
                    PlatformID.Unix => @"/",
                    _ => @"/",
                };
            }
        }

        public const string ServerOK = "Server OK";
    }
}

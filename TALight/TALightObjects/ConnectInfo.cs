using System;

namespace TALightObjects
{
    public class ConnectInfo
    {
        public ConnectInfo(string folder, string services)
        {
            Folder = folder ?? throw new ArgumentNullException(nameof(folder));
            Services = services ?? throw new ArgumentNullException(nameof(services));

            Arguments = "";
            MyToken = new Token();
        }

        public ConnectInfo(string folder, string services, string arguments)
        {
            Folder = folder ?? throw new ArgumentNullException(nameof(folder));
            Services = services ?? throw new ArgumentNullException(nameof(services));
            Arguments = arguments ?? throw new ArgumentNullException(nameof(arguments));

            MyToken = new Token();
        }

        public string Folder { get; set; }
        public string Services { get; set; }
        public string Arguments { get; set; }

        public Token MyToken { get; set; }

        public override string ToString()
        {
            return Folder + " " + Services;
        }
    }
}

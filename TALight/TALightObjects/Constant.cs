namespace TALightObjects
{
    public class Constant
    {
        public const string Protocol = "https";
        public const string ProtocolWS = "wss";

        public static string Url(string Host, int Port)
        {
            return Protocol + "://" + Host + ":" + Port;
        }

        public static string UrlWS(string Host, int Port)
        {
            return ProtocolWS + "://" + Host + ":" + Port + "/ws";
        }

        public const string ProgramName = "TALight";
        public const string banner = "====================================";
        public const string WelcomeMessage = banner + "\n" + "TALight" + "\n" + banner + "\n";
        public const string WelcomeMessageCut = banner + "\n" + ProgramName;

        public const string Help = "help\n";

        public const int TokenDimension = 512;
        public const int Timeout = 3600;

        public const string Empty = "None";

        public const string EnviromentStart = "TAL_";
    }
}

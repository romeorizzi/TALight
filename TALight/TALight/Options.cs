using CommandLine;

namespace TALight
{
    public class Options
    {
        [Option('c', "command", Required = true, HelpText = "Principal command to execute")]
        public string Command { get; set; }

        [Option('h', "host", Required = false, Default = "", HelpText = "Host connection")]
        public string Host { get; set; }
        [Option('p', "port", Required = false, Default = -1, HelpText = "Host port")]
        public int Port { get; set; }

        [Option('f', "folder", Required = false, Default = "", HelpText = "Folder")]
        public string Folder { get; set; }

        [Option('d', "output", Required = false, Default = "", HelpText = "Name of the folder downloaded")]
        public string OutputPath { get; set; }

        [Option('s', "service", Required = false, Default = "", HelpText = "Service request")]
        public string Service { get; set; }
        [Option('r', "sargs", Required = false, Default = "", HelpText = "Service arguments")]
        public string ServiceArgs { get; set; }

        [Option('m', "program", Required = false, Default = "", HelpText = "My program to execute")]
        public string MyProgram { get; set; }
        [Option('g', "pargs", Required = false, Default = "", HelpText = "Args for my program")]
        public string MyProgramArgs { get; set; }

    }
}

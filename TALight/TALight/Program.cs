using CommandLine;
using System;
using System.IO;
using System.Threading;
using TALight.Calls;
using TALightObjects;

namespace TALight
{
    public class Program
    {
        public static void Main(string[] args)
        {
#if DEBUG
            Thread.Sleep(5000);
#endif

            ParserResult<Options> parser = Parser.Default.ParseArguments<Options>(args).WithParsed(o =>
            {
                Execute(o);
            });
        }

        public static void Execute(Options o)
        {
            // Load from local yaml
            LoadCache s = new LoadCache();
            s.Load(Constant.SettingFile);
            s.Into(o);

            if (o.Folder != null)
            {
                if (o.Folder.Contains(@"\") || o.Folder.Contains(@"/"))
                {
                    o.Folder = o.Folder.Replace(@"\", "%2F").Replace("/", "%2F");
                }
            }

            switch (o.Command.Trim().ToLower())
            {
                case Constant.Help:
                    Help();
                    break;
                case Constant.Test:
                    TestMethod(o);
                    break;
                case Constant.List:
                    List(o);
                    break;
                case Constant.ListP:
                    ListP(o);
                    break;
                case Constant.Info:
                    Info(o);
                    break;
                case Constant.Get:
                    Get(o);
                    break;
                case Constant.Connect:
                    Connect(o);
                    break;
            }

            s.Put(o);
            s.Save(Constant.SettingFile);
        }

        private static void Help()
        {
            Console.WriteLine(TALightObjects.Constant.WelcomeMessage);

            Console.WriteLine(TALightObjects.Constant.Help);
        }

        private static void TestMethod(Options o)
        {
            Console.WriteLine(TALightObjects.Constant.WelcomeMessage);

            Console.WriteLine(Test.GetTest(o.Host, o.Port).Result);
        }

        private static void List(Options o)
        {
            Console.WriteLine(TALightObjects.Constant.WelcomeMessage);

            TALightObjects.Folder[] folders = Calls.Folder.GetFolders(o.Host, o.Port, o.Folder).Result;
            Utilities.PrintArray(folders);
        }

        private static void ListP(Options o)
        {
            Console.WriteLine(TALightObjects.Constant.WelcomeMessage);

            Problem[] problems = Problems.GetProblems(o.Host, o.Port, o.Folder).Result;
            Utilities.PrintArray(problems);
        }

        private static void Info(Options o)
        {
            Console.WriteLine(TALightObjects.Constant.WelcomeMessage);

            Problem problem = Problems.GetInfoProblem(o.Host, o.Port, o.Folder).Result;
            Console.WriteLine(problem.ToConsole());
        }

        private static void Get(Options o)
        {
            Console.WriteLine(TALightObjects.Constant.WelcomeMessage);

            Console.WriteLine(Constant.FetchingData);
            File.WriteAllBytes(o.OutputPath, Problems.GetProblemAttachment(o.Host, o.Port, o.Folder).Result);
            Console.WriteLine(Constant.FileDownloaded);
        }

        private static void Connect(Options o)
        {
            Console.WriteLine(TALightObjects.Constant.WelcomeMessageCut);

            ConnectInfo info = new ConnectInfo(o.Folder, o.Service)
            {
                Arguments = o.ServiceArgs
            };

            Console.WriteLine(Utilities.PrintConnectInfo(info) + "\n");

            if (string.IsNullOrEmpty(o.MyProgram))
            {
                Engine.Connect(o.Host, o.Port, info);
            }
            else
            {
                Engine.Connect(o.Host, o.Port, info, o.MyProgram, o.MyProgramArgs);
            }
        }
    }
}

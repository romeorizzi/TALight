using System;
using System.Diagnostics;
using System.IO;
using System.Net.Security;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using TALight.Calls;
using TALightObjects;
using Websocket.Client;

namespace TALight
{
    class Engine
    {
        public Engine()
        {
        }

        public static void Connect(string host, int port, ConnectInfo info)
        {
            Token t = Connection.GetConnection(host, port, info).Result;

            if (t is not null)
            {
                ManualResetEvent exitEvent = new ManualResetEvent(false);
                Uri url = new Uri(TALightObjects.Constant.UrlWS(host, port));

                using WebsocketClient client = new WebsocketClient(url)
                {
                    ReconnectTimeout = TimeSpan.FromSeconds(TALightObjects.Constant.Timeout)
                };
                //client.ReconnectionHappened.Subscribe(info => Console.WriteLine(info));

                client.MessageReceived.Subscribe(msg => Console.Write(msg));
                client.Start();

                client.Send(t.ToSend());

                while (true)
                {
                    string s = Console.ReadLine();
                    if (!string.IsNullOrEmpty(s))
                    {
                        client.Send(s);
                    }
                }
            }
            else
            {
                Console.WriteLine(Constant.WrongArguments);
            }
        }

        public static void Connect(string host, int port, ConnectInfo info, string program, string programargs)
        {
            Process p = new Process();
            string exec = "python3";
            if (Environment.OSVersion.Platform == PlatformID.Win32NT)
            {
                exec = "python";
            }
            ProcessStartInfo startInfo = new ProcessStartInfo(exec)
            {
                UseShellExecute = false,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            };
            startInfo.Arguments = program;
            foreach (Tuple<string, string> x in TALightObjects.Utilities.TakeArguments(programargs))
            {
                startInfo.EnvironmentVariables.Add(TALightObjects.Constant.EnviromentStart + x.Item1, x.Item2);
            }
            p.StartInfo = startInfo;
            p.Start();

            StreamReader streamOutput = p.StandardOutput;
            StreamWriter streamInput = p.StandardInput;
            StreamReader streamErrore = p.StandardError;

#if DEBUG
            if (p.HasExited)
            {
                throw new NotImplementedException();
            }
#endif

            Token Servertoken = Connection.GetConnection(host, port, info).Result;

            CancellationTokenSource cancellationTokenSource = new CancellationTokenSource();
            CancellationToken t = cancellationTokenSource.Token;

            Uri uri = new Uri(TALightObjects.Constant.UrlWS(host, port));

            ClientWebSocket webSocket = new ClientWebSocket();
#if DEBUG
            webSocket.Options.RemoteCertificateValidationCallback += new RemoteCertificateValidationCallback((sender, certificate, chain, policyErrors) => { return true; });
#endif
            webSocket.ConnectAsync(uri, t).Wait();

            if (Servertoken is not null)
            {
                byte[] buffersend = Encoding.Default.GetBytes(Servertoken.ToSend());
                webSocket.SendAsync(new ArraySegment<byte>(buffersend, 0, buffersend.Length), WebSocketMessageType.Text, true, CancellationToken.None).Wait();

                cancellationTokenSource.CancelAfter(1000 * 3600); // 1 hour
                Task threadOutput = new Task(() => WebSocketHandler.FunOutput(webSocket, p, streamOutput, cancellationTokenSource, "CLIENTPROCESS_OUT:", t), t);
                Task threadInput = new Task(() => WebSocketHandler.FunInput(webSocket, p, streamInput, cancellationTokenSource, "CLIENTPROCESS_IN:", t), t);

                threadOutput.Start();
                threadInput.Start();

                try
                {
                    threadOutput.Wait(t);
                    threadInput.Wait(t);
                }
                catch (OperationCanceledException)
                {

                }

                string error = streamErrore.ReadToEnd();
                if (p.HasExited && error != "")
                {
                    Console.WriteLine(error);
                }

                int exitresult = p.ExitCode;

                try
                {
                    webSocket.CloseAsync(WebSocketCloseStatus.Empty, "", CancellationToken.None).Wait();
                }
                catch (AggregateException)
                {
                    return;
                }
            }
            else
            {
                Console.WriteLine(Constant.WrongArguments);
            }
        }
    }
}

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using TALightObjects;
using TALightServer.Model;

namespace TALightServer.WebSocketName
{
    public class WebSocketImplementation
    {
        public static async Task ProcessWebSocketHandler(WebSocket webSocket)
        {
            // First bytes are the token
            byte[] fortoken = new byte[TALightObjects.Constant.TokenDimension];
            WebSocketReceiveResult result = await webSocket.ReceiveAsync(new ArraySegment<byte>(fortoken), CancellationToken.None);

            ConnectInfo infotoken = TokensArchive.GetInstance().SearchToken(Token.Parse(fortoken));
            Problem probleminfo = GetData.GetMeta(infotoken.Folder);

            if (infotoken == null)
            {
                webSocket.Abort();
                return;
            }

            Process p = new Process();
            string exec = "python3";
            if (Environment.OSVersion.Platform == PlatformID.Win32NT)
            {
                exec = "python";
            }

            // TODO Generic program
            ProcessStartInfo info = new ProcessStartInfo(exec)
            {
                UseShellExecute = false,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            };
            info.Arguments = '\"' + GetData.GetExecutables(infotoken.Folder, infotoken.Services) + '\"';
            List<Tuple<string, string>> la = TALightObjects.Utilities.TakeArguments(infotoken.Arguments);
            foreach (Tuple<string, string> x in la)
            {
                info.EnvironmentVariables.Add(TALightObjects.Constant.EnviromentStart + x.Item1, x.Item2);
            }
            if (probleminfo.Debug)
            {
                info.EnvironmentVariables.Add(TALightObjects.Constant.EnviromentStart + "DEBUG", "TRUE");
            }
            p.StartInfo = info;
            p.Start();

            StreamReader serverError = p.StandardError;
            StreamReader serverOutput = p.StandardOutput;
            StreamWriter serverInput = p.StandardInput;

            CancellationTokenSource cancellationTokenSource = new CancellationTokenSource();
            cancellationTokenSource.CancelAfter(1000 * 3600); // 1 hour
            CancellationToken t = cancellationTokenSource.Token;
            Task threadOutput = new Task(() => WebSocketHandler.FunOutput(webSocket, p, serverOutput, cancellationTokenSource, "SERVERPROCESS_OUT:", t), t);
            Task threadInput = new Task(() => WebSocketHandler.FunInput(webSocket, p, serverInput, cancellationTokenSource, "SERVERPROCESS_IN:", t), t);

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

            string error = serverError.ReadToEnd();
            if (p.HasExited && error != "")
            {
                byte[] buffersend = Encoding.Default.GetBytes(error + "\n");
                await webSocket.SendAsync(new ArraySegment<byte>(buffersend, 0, buffersend.Length), WebSocketMessageType.Text, true, CancellationToken.None);
            }

            int exitresult = p.ExitCode;

            try
            {
                await webSocket.CloseAsync(result.CloseStatus.Value, result.CloseStatusDescription, CancellationToken.None);
            }
            catch (AggregateException)
            {
                return;
            }
            catch (InvalidOperationException)
            {
                return;
            }
            catch (NullReferenceException)
            {
                return;
            }
        }
    }
}

using System;
using System.Diagnostics;
using System.IO;
using System.Net.WebSockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace TALightObjects
{
    public class WebSocketHandler
    {
        public static void FunOutput(WebSocket webSocket, Process p, StreamReader serverOutput, CancellationTokenSource cancellationTokenSource, string ToPrint, CancellationToken t)
        {
            try
            {
                FunOutputAsync(webSocket, p, serverOutput, ToPrint).Wait(t);
                cancellationTokenSource.Cancel();
            }
            catch (WebSocketException)
            {
                return;
            }
            catch (OperationCanceledException)
            {
                return;
            }
            catch (AggregateException)
            {
                return;
            }
            catch (COMException)
            {
                return;
            }
        }

        public static void FunInput(WebSocket webSocket, Process p, StreamWriter streamInput, CancellationTokenSource cancellationTokenSource, string ToPrint, CancellationToken t)
        {
            try
            {
                FunInputAsync(webSocket, p, streamInput, ToPrint).Wait(t);
                cancellationTokenSource.Cancel();
            }
            catch (WebSocketException)
            {
                return;
            }
            catch (OperationCanceledException)
            {
                return;
            }
            catch (AggregateException)
            {
                return;
            }
            catch (COMException)
            {
                return;
            }
        }

        public static async Task FunInputAsync(WebSocket webSocket, Process p, StreamWriter serverInput, string s)
        {
            string mystring = "";

            while (!p.HasExited)
            {
                byte[] buffer = new byte[1024 * 4];
                _ = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);

                string ricevutaClient = Encoding.Default.GetString(buffer);
                ricevutaClient = ricevutaClient.Replace("\0", "");

                if (!string.IsNullOrEmpty(ricevutaClient))
                {
                    if (!string.IsNullOrEmpty(s))
                    {
                        mystring += "" + ricevutaClient;

                        if (mystring.EndsWith("\n") || mystring.EndsWith("\r"))
                        {
                            mystring = mystring.Replace("\n", "").Replace("\r", "");

                            if (!string.IsNullOrEmpty(mystring))
                            {
                                Console.Write(s + " " + mystring + Environment.NewLine);
                                Debug.Write(s + " " + mystring + Environment.NewLine);
                                mystring = "";
                            }
                        }
                    }

                    serverInput.Write(ricevutaClient);
                }
            }
        }

        public static async Task FunOutputAsync(WebSocket webSocket, Process p, StreamReader serverOutput, string s)
        {
            // TODO Handle big message

            string mystring = "";

            while (!p.HasExited || !serverOutput.EndOfStream)
            {
                char dainviarec = (char)serverOutput.Read();
                string dainviare = "" + dainviarec;

                if (dainviare != null && dainviare.Length != 0)
                {
                    if (!string.IsNullOrEmpty(s))
                    {
                        mystring += "" + dainviare;

                        if (mystring.EndsWith("\n") || mystring.EndsWith("\r"))
                        {
                            mystring = mystring.Replace("\n", "").Replace("\r", "");

                            if (!string.IsNullOrEmpty(mystring))
                            {
                                Console.Write(s + " " + mystring + Environment.NewLine);
                                Debug.Write(s + " " + mystring + Environment.NewLine);
                                mystring = "";
                            }
                        }
                    }

                    byte[] buffersend = Encoding.Default.GetBytes(dainviare);
                    await webSocket.SendAsync(new ArraySegment<byte>(buffersend, 0, buffersend.Length), WebSocketMessageType.Text, true, CancellationToken.None);
                }
            }
        }
    }
}

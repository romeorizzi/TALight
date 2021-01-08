using System.Collections.Generic;
using TALightObjects;

namespace TALightServer
{
    public sealed class TokensArchive
    {
        private readonly List<ConnectInfo> c = new List<ConnectInfo>();
        private static readonly TokensArchive instance = new TokensArchive();

        static TokensArchive()
        {
        }

        private TokensArchive()
        {
        }

        public static TokensArchive GetInstance()
        {
            return instance;
        }

        readonly object obj = new object();
        public ConnectInfo SearchToken(Token t)
        {
            lock (obj)
            {
                foreach (ConnectInfo x in c)
                {
                    if (x.MyToken.Check(t))
                    {
                        ConnectInfo info = x;
                        c.Remove(x);
                        return info;
                    }
                }
            }

            return null;
        }

        internal void AddConnection(ConnectInfo connectInfo)
        {
            c.Add(connectInfo);
        }
    }
}

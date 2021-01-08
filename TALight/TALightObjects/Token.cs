using System;
using System.Text;

namespace TALightObjects
{
    public class Token
    {

        public string Secret { get; set; }

        Random ran = new Random();

        public Token()
        {
            Generate();
        }

        public Token(string s)
        {
            this.Secret = s;
        }

        private readonly object obj = new object();

        public void Generate()
        {
            string tmp = "";

            for (int i = 0; i < Constant.TokenDimension; i++)
            {
                if (ran.Next(0, 10) > 7)
                {
                    lock (obj)
                    {
                        ran = new Random();
                    }
                }

                tmp += ran.Next(0, 9 + 1).ToString();
            }

            Secret = tmp;
        }

        public bool Check(Token t)
        {
            return t.Secret == this.Secret;
        }

        public string ToSend()
        {
            return Secret;
        }

        public static Token Parse(byte[] fortoken)
        {
            Token t = new Token(Encoding.Default.GetString(fortoken));
            return t;
        }

        public override string ToString()
        {
            return Secret;
        }
    }
}
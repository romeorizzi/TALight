using System.Collections.Generic;

namespace TALightObjects
{
    public class Problem
    {
        public Problem()
        {
            Service = new List<Service>();
        }

        public string Id { get; set; }

        public string Codename { get; set; }

        public string Description { get; set; }

        public string AttachmentFolder { get; set; }

        public List<Service> Service { get; set; }

        /// <summary>
        /// Unused
        /// </summary>
        public bool Debug { get; set; }
        /// <summary>
        /// Unused
        /// </summary>
        public bool Hide { get; set; }

        public override string ToString()
        {
            return Id + " " + Codename;
        }

        public string ToConsole()
        {
            string s;
            s = Codename;
            if (Description != "")
            {
                s += "\n" + Description;
            }

            s += "\nServices:";

            foreach (Service x in this.Service)
            {
                s += "\n - " + x.Name;
                if (x.List.Count != 0)
                {
                    s += "; ";

                    foreach (Arguments j in x.List)
                    {
                        s += j.Name + "=" + j.RegEx + " ,";
                    }

                    s = s.Remove(s.Length - 1, 1);
                }
            }

            return s;
        }
    }

    public class Service
    {
        public string Name { get; set; }

        public string Runnable { get; set; }

        public List<Arguments> List { get; set; }

        public Service()
        {
            List = new List<Arguments>();
        }
    }

    public class Arguments
    {
        public string Name { get; set; }
        public string RegEx { get; set; }
        public string Default { get; set; }
        public bool Request { get; set; }
    }
}

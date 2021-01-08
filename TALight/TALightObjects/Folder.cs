using System;

namespace TALightObjects
{
    public class Folder
    {
        public Folder()
        {
        }

        public Folder(string id, string name, bool isProblem)
        {
            Id = id ?? throw new ArgumentNullException(nameof(id));
            Name = name ?? throw new ArgumentNullException(nameof(name));
            IsProblem = isProblem;
        }

        public string Id { get; set; }

        public string Name { get; set; }

        public bool IsProblem { get; set; }

        public override string ToString()
        {
            return IsProblem ? Id + " " + "(Type: Problem)" : Id + " " + "(Type: Folder)";
        }
    }
}

using System;
using System.IO;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace TALight
{
    internal class LoadCache
    {
        Setting s;

        internal void Load(string filename)
        {
            string yml = File.ReadAllText(filename);

            IDeserializer deserializer = new DeserializerBuilder()
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .Build();

            s = deserializer.Deserialize<Setting>(yml);
        }

        internal void Save(string filename)
        {
            ISerializer serializer = new SerializerBuilder()
                .WithNamingConvention(UnderscoredNamingConvention.Instance)
                .Build();

            string tmp = serializer.Serialize(s);
            File.WriteAllText(filename, tmp);
        }

        internal void Into(Options o)
        {
            // TODO With Reflection

            if (string.IsNullOrEmpty(o.Command))
            {
                throw new NotImplementedException();
            }

            if (string.IsNullOrEmpty(o.Host))
            {
                o.Host = s.Host;
            }

            if (o.Port == -1)
            {
                o.Port = s.Port;
            }

            if (string.IsNullOrEmpty(o.OutputPath))
            {
                o.OutputPath = s.OutputPath;
            }

            if (string.IsNullOrEmpty(o.Folder))
            {
                o.Folder = s.Folder;
            }

            if (string.IsNullOrEmpty(o.Service))
            {
                o.Service = s.Service;
            }

            if (string.IsNullOrEmpty(o.ServiceArgs))
            {
                o.ServiceArgs = s.ServiceArgs;
            }

            if (string.IsNullOrEmpty(o.MyProgram))
            {
                o.MyProgram = s.MyProgram;
            }

            if (string.IsNullOrEmpty(o.MyProgramArgs))
            {
                o.MyProgramArgs = s.MyProgramArgs;
            }
        }

        internal void Put(Options o)
        {
            // TODO With Reflection

            if (string.IsNullOrEmpty(o.Command))
            {
                throw new NotImplementedException();
            }

            s.Host = o.Host;
            s.Port = o.Port;

            s.OutputPath = o.OutputPath;
            s.Folder = o.Folder;

            s.Service = o.Service;
            s.ServiceArgs = o.ServiceArgs;

            s.MyProgram = o.MyProgram;
            s.MyProgramArgs = o.MyProgramArgs;
        }
    }
}
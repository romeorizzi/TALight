using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using TALightObjects;
using YamlDotNet.RepresentationModel;

namespace TALightServer.Model
{
    public class GetData
    {
        internal static Folder[] GetFolder(string folder)
        {
            string[] ld = Directory.GetDirectories(GetPath.GetFolder(folder));

            List<Folder> l = new List<Folder>();

            foreach (string i in ld)
            {
                Folder f = new Folder
                {
                    Id = Path.GetFileName(i)
                };
                f.Name = f.Id;

                f.IsProblem = File.Exists(GetPath.GetMetaFile(i));

                l.Add(f);
            }

            return l.ToArray();
        }

        internal static byte[] GetProblemAttachment(string f)
        {
            // TODO Use cache

            Problem problemdata = GetMeta(f);
            string folder = GetPath.GetFolderAttach(f, problemdata.AttachmentFolder);

            using MemoryStream ms = new MemoryStream();
            using (ZipArchive zip = new ZipArchive(ms, ZipArchiveMode.Create, true))
            {
                foreach (string i in Directory.GetFiles(folder))
                {
                    string entryname = i.Remove(0, folder.Length + Constant.Separator.Length);

                    zip.CreateEntryFromFile(i, entryname);
                }
            }

            return ms.ToArray();
        }

        internal static Problem[] GetProblems(string folder)
        {
            string[] ld = Directory.GetDirectories(GetPath.GetFolder(folder));

            List<Problem> l = new List<Problem>();

            foreach (string i in ld)
            {
                if (File.Exists(GetPath.GetMetaFile(i)))
                {
                    Problem p = GetMeta(i);

                    p.Id = Path.GetFileName(i);

                    if (!p.Hide)
                        l.Add(p);
                }
            }

            return l.ToArray();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="idfolder">File path</param>
        /// <returns></returns>
        internal static Problem GetMeta(string idfolder)
        {
            Problem p = new Problem();

            string yml = File.ReadAllText(GetPath.GetMetaFile(idfolder));

            StringReader stringReader = new StringReader(yml);

            YamlStream yaml = new YamlStream();
            yaml.Load(stringReader);

            YamlMappingNode mapping = (YamlMappingNode)yaml.Documents[0].RootNode;

            // TODO Fix this

            foreach (var entry in mapping.Children)
            {
                if (entry.Value is YamlMappingNode mapping2)
                {
                    foreach (var entry2 in mapping2.Children)
                    {
                        if (entry2.Value is YamlMappingNode mapping3)
                        {
                            Service s = new Service
                            {
                                Name = entry2.Key.ToString()
                            };

                            foreach (var entry3 in mapping3.Children)
                            {
                                if (entry3.Key.ToString() == "evaluator")
                                {
                                    s.Runnable = entry3.Value.ToString();
                                }

                                if (entry3.Value is YamlMappingNode mapping4)
                                {
                                    Arguments arguments = new Arguments
                                    {
                                        Request = false
                                    };

                                    foreach (var entry4 in mapping4.Children)
                                    {
                                        arguments.Name = entry4.Key.ToString();

                                        YamlMappingNode mapping5 = (YamlMappingNode)entry4.Value;

                                        foreach (var entry5 in mapping5.Children)
                                        {
                                            if (entry5.Key.ToString() == "regex")
                                            {
                                                arguments.RegEx = entry5.Value.ToString();
                                            }
                                            else if (entry5.Key.ToString() == "default")
                                            {
                                                arguments.Default = entry5.Value.ToString();
                                                arguments.Request = false;
                                            }
                                        }
                                    }

                                    s.List.Add(arguments);
                                }
                            }

                            p.Service.Add(s);
                        }
                    }
                }

                switch (entry.Key.ToString())
                {
                    case "name":
                        p.Codename = entry.Value.ToString();
                        break;
                    case "codename":
                        p.Codename = entry.Value.ToString();
                        break;
                    case "description":
                        p.Description = entry.Value.ToString();
                        break;
                    case "attachments_folder":
                        p.AttachmentFolder = entry.Value.ToString();
                        break;
                    case "debug":
                        p.Debug = bool.Parse(entry.Value.ToString());
                        break;
                    case "hide":
                        p.Hide = bool.Parse(entry.Value.ToString());
                        break;
                }
            }

            return p;
        }

        internal static string GetExecutables(string folder, string services)
        {
            Problem p = GetMeta(folder);

            string program = "";

            foreach (Service x in p.Service)
            {
                if (x.Name == services)
                {
                    program = x.Runnable;
                }
            }

            return GetPath.GetProgram(folder, program);
        }
    }
}

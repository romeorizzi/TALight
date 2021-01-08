using System.IO;

namespace TALightServer.Model
{
    public class GetPath
    {
        public static string GetMetaFile(string idfolder)
        {
            string f = CleanFolder(idfolder);

            return idfolder.StartsWith(Constant.Folder)
                ? Path.Combine(f, Constant.MetaFile)
                : Path.Combine(Constant.Folder, f, Constant.MetaFile);
        }
        public static string GetFolderAttach(string idfolder, string attachmentfolder)
        {
            string f = CleanFolder(idfolder);
            return Path.Combine(Constant.Folder, f, attachmentfolder);
        }
        public static string GetProgram(string idfolder, string program)
        {
            string f = CleanFolder(idfolder);
            return Path.Combine(Constant.Folder, f, program);
        }
        public static string GetFolder(string folder)
        {
            string f = CleanFolder(folder);
            return Path.Combine(Constant.Folder, f);
        }

        public static string CleanFolder(string folder)
        {
            if (string.IsNullOrEmpty(folder) || folder == Constant.Folder)
            {
                return "";
            }
            else
            {
                return folder.Replace("%2F", Constant.Separator).Replace("%5C", Constant.Separator);
            }
        }
    }
}

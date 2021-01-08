using System.Threading.Tasks;

namespace TALight.Calls
{
    class Folder
    {
        public static async Task<TALightObjects.Folder[]> GetFolders(string host, int port, string folder)
        {
            return await GenericCall<TALightObjects.Folder[]>.Call("/Folder/" + folder, TALightObjects.Constant.Url(host, port));
        }
    }
}

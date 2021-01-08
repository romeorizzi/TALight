using System.Threading.Tasks;
using TALightObjects;

namespace TALight.Calls
{
    public class Connection
    {
        public static async Task<Token> GetConnection(string host, int port, ConnectInfo info)
        {
            return await GenericCall<Token>.Call("/Connect/" + info.Folder + "/" + info.Services + "/" + info.Arguments, TALightObjects.Constant.Url(host, port));
        }
    }
}

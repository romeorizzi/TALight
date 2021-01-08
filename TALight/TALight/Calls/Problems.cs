using System.Threading.Tasks;
using TALightObjects;

namespace TALight.Calls
{
    class Problems
    {
        public static async Task<Problem[]> GetProblems(string host, int port, string folder)
        {
            return await GenericCall<Problem[]>.Call("/Problem/" + folder, TALightObjects.Constant.Url(host, port));
        }

        public static async Task<byte[]> GetProblemAttachment(string host, int port, string folder)
        {
            return await GenericCall<byte[]>.Call("/Problem/" + folder + "/att", TALightObjects.Constant.Url(host, port));
        }

        public static async Task<Problem> GetInfoProblem(string host, int port, string course)
        {
            return await GenericCall<Problem>.Call("/Problem/" + course + "/info", TALightObjects.Constant.Url(host, port));
        }
    }
}

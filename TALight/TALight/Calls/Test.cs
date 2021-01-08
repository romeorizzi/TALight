using System.Threading.Tasks;

namespace TALight.Calls
{
    class Test
    {
        public static async Task<string> GetTest(string host, int port)
        {
            return await GenericCall<string>.Call("/Test", TALightObjects.Constant.Url(host, port));
        }
    }
}

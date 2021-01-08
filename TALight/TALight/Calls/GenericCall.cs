using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;

namespace TALight.Calls
{
    public class GenericCall<T>
    {
        public static async Task<T> Call(string request, string url)
        {
            HttpClientHandler httpClientHandler = new HttpClientHandler
            {
#if DEBUG
                ServerCertificateCustomValidationCallback = (message, cert, chain, errors) => { return true; }
#endif
            };

            using HttpClient client = new HttpClient(httpClientHandler)
            {
                BaseAddress = new Uri(url)
            };
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // HTTP GET
            HttpResponseMessage response = client.GetAsync(request).Result;
            if (response.IsSuccessStatusCode)
            {
                JsonSerializerOptions options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };

                string result = await response.Content.ReadAsStringAsync();
                T myInstance = JsonSerializer.Deserialize<T>(result, options);
                return myInstance;
            }
            else
            {
                throw new NotImplementedException();
            }
        }
    }
}

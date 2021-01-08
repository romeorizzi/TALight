using Microsoft.AspNetCore.Mvc;

namespace TALightServer.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class TestController : ControllerBase
    {
        [HttpGet]
        public string Get() => Constant.ServerOK;
    }
}

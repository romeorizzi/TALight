using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using TALightObjects;
using TALightServer.Model;

namespace TALightServer.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class FolderController : ControllerBase
    {
        [HttpGet("{idfolder?}")]
        public IEnumerable<Folder> Get(string idfolder = "") => GetData.GetFolder(idfolder);
    }
}

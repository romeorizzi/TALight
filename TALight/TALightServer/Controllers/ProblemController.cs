using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.IO;
using TALightObjects;
using TALightServer.Model;

namespace TALightServer.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ProblemController : ControllerBase
    {
        [HttpGet("{idfolder?}")]
        public IEnumerable<Problem> Get(string idfolder = "") => GetData.GetProblems(idfolder);

        [HttpGet("{idfolder}/info")]
        public Problem GetInfoProblem(string idfolder = "")
        {
            Problem p = GetData.GetMeta(idfolder);
            p.Id = Path.GetExtension(idfolder);
            return p;
        }

        [HttpGet("{idfolder}/att")]
        public byte[] GetProblemAttachment(string idfolder = "") => GetData.GetProblemAttachment(idfolder);
    }
}

using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using TALightObjects;

namespace TALightServer.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ConnectController : ControllerBase
    {
        [HttpGet("{idfolder}/{service}/{arguments?}")]
        public Token Get(string idfolder, string service, string arguments = "")
        {
            if (string.IsNullOrEmpty(arguments))
            {
                arguments = "";
            }

            if (Model.Utilities.CheckService(idfolder, service))
            {
                ConnectInfo connectInfo = new ConnectInfo(idfolder, service, arguments);

                List<Tuple<string, string>> l = TALightObjects.Utilities.TakeArguments(arguments);

                if (Model.Utilities.CheckArguments(connectInfo, l))
                {
                    TokensArchive.GetInstance().AddConnection(connectInfo);
                    return connectInfo.MyToken;
                }
                else
                {
                    return null;
                }
            }
            else
            {
                return null;
            }
        }
    }
}

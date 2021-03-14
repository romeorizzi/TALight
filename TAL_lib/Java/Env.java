/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication17;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;

/**
 *
 * @author UTENTE
 */
public class Env {
    private String service_server_fullname="";
    private String exe_path="";
    private Map<String,String> environment_variables=System.getenv();
    private String meta_data=System.getenv("TAL_META_DIR");
    private String problem="";
    private String service="";
    private Object [] arg = {};

    public Env(String exe_path,String problem,String service,Object []argv){
        this.service_server_fullname=argv[0].toString();
        this.exe_path=exe_path.split(service_server_fullname)[0];
        this.problem=problem;
        this.service=service;
        Object [] arg = {};
        for(int i =0;i<argv.length;i++) {
            if(argv[i] instanceof String)
                arg[i]=System.getenv("TAL_"+i);
            else if(argv[i] instanceof Boolean) {
                argv[i]="1";
                environment_variables.put("TAL_"+i,"1");
            }
            else if(argv[i] instanceof Integer) {
                for (Map.Entry <String, String> entry: environment_variables.entrySet()) {
                     if(entry.getKey().equals("TAL_"+i))
                             arg[i]=Integer.parseInt(entry.getValue());
                }
            }
            else if(argv[i] instanceof Float) {
                for (Map.Entry <String, String> entry: environment_variables.entrySet()) {
                     if(entry.getKey().equals("TAL_"+i))
                             arg[i]=Float.parseFloat(entry.getValue());
                }
            }
            else {
               System.out.println("# Unrecoverable Error: TypeVariable not yet supported in args list. Used to interpret arg {name}.");
               System.err.println("# Unrecoverable Error: TypeVariable not yet supported in args list. Used to interpret arg {name}.");
               System.exit(0);
            }
        }
    }
    public Object[] getitem() {
        return arg;
    }
}

/*
class Env:
    
    def __init__(self, problem, service, args_list):
        self.service_server_fullname = argv[0]
        self.exe_path = split(argv[0])[0]
        self.meta_dir = environ["TAL_META_DIR"]
        self.problem = problem
        self.service = service
        self.args_list = args_list
        self.arg = {}
        for name, val_type in args_list:
            if val_type == str:
                self.arg[name] = environ[f"TAL_{name}"]
            elif val_type == bool:
                self.arg[name] = (environ[f"TAL_{name}"] == "1")
            elif val_type == int:
                self.arg[name] = int(environ[f"TAL_{name}"])
            elif val_type == float:
                self.arg[name] = float(environ[f"TAL_{name}"])
            else:
                for out in [stdout, stderr]:
                    print(f"# Unrecoverable Error: type {val_type} not yet supported in args list. Used to interpret arg {name}.", file=out)
                exit(1)
    def __getitem__(self, key):
        return self.arg.get(key)
*/
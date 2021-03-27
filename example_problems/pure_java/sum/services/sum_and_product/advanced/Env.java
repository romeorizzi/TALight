/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


import java.io.IOException;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;

/**
 *
 * @author UTENTE
 */
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 *
 * @author UTENTE
 */
public class Env {
    private Map<String, Object> item = new HashMap<>();
    private Map<String, String> environment_variables = System.getenv();
    public String META_DIR = System.getenv("TAL_META_DIR");
    public String exe_path = "";
    public String problem = "";
    public String service = "";
    private Object[] arg = {};
    public Env() {

    }
    public Env(String problem, String service, Map<String, String> args) {
        this.problem = problem;
        this.service = service;
        this.environment_variables = args;
        this.item = ENV_overide(environment_variables);
        try {
            this.exe_path= new java.io.File( "." ).getCanonicalPath();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    private Map<String, Object> ENV_overide(Map<String, String> args) {

        for (Map.Entry<String, String> entry : args.entrySet()) {
            switch (entry.getValue()) {
                case "int":
                    item.put(entry.getKey(), Integer.parseInt(System.getenv("TAL_" + entry.getKey())));
                    break;

                case "String":
                    item.put(entry.getKey(), System.getenv("TAL_" + entry.getKey()));

                    break;
                case "Float":
                    item.put(entry.getKey(), Float.parseFloat(System.getenv("TAL_" + entry.getKey())));
                    break;
                default:
                    System.out.println("# Unrecoverable Error: type " + entry.getValue() + "not yet supported in args list. Used to interpret arg " + entry.getKey() + ".");
            }
        }
        return item;
    }

    public Object ENV(String var) {
        for (Map.Entry<String, Object> entry : item.entrySet()) {
            if (entry.getKey().equalsIgnoreCase(var)) {
                return entry.getValue();
            }
        }
        return null;

    }
}


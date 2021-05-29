import java.io.*;
import java.util.*;
import java.util.regex.Pattern;

public class Lang {
    public String message_book_file = "";
    public Env env = new Env();
    public TALcolors TAc = new TALcolors();
    public String service_server_eval = "";
    public String exe_path ="";
    public String opening_msg="";
    public Lang(Env env,TALcolors TAc,String service_server_eval,boolean book_required) {

        this.env = env;
        this.TAc=TAc;
        this.service_server_eval=service_server_eval;

         this.exe_path=""+env.exe_path;
        this.message_book_file=exe_path.substring(0,exe_path.length()-3)+service_server_eval+"_feedbackBook."+ env.ENV("Lang")+".yaml";
        List<String> characterType=new ArrayList<>();
        characterType.add("bold");
        if (!book_required) {
                TAc.print("# Recoverable Error: ", "red", characterType,null);
                System.out.println("# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue (as long as you can understand the little needed English).\n# (To enjoy a feedback in a supported language install the python package 'ruamel'. The languages supported by a problem service appear as the options for the lang parameter listed by the command `rtal list`)");
        }
        else {
            List<Object> vars = new ArrayList<>();
            vars.add(env.problem);
            vars.add(env.service);
            vars.add(0);
            vars.add(0);
         opening_msg=render_feedback("open-channel","# I will serve: problem="+env.problem+", service="+env.service+".",vars);
        }


    }
    public String render_feedback(String msg_code,String redition_of_the_hardcoded_MSG,List<Object>vars) {
        File initialFile = new File(message_book_file);
        Map<String,String>yamlKey=new HashMap<>();
        try {
            BufferedReader objReader = new BufferedReader(new FileReader(message_book_file));
            String strCurrentLine = "";
            String key,value ="";
            Pattern pattern =Pattern.compile("\\{.*}");

            while ((strCurrentLine = objReader.readLine()) != null) {
                if (strCurrentLine.contains(":")&&strCurrentLine.split(":")[0].equals(msg_code)) {
                    key = strCurrentLine.split(":")[0];
                    for(int i = 1;i<strCurrentLine.split(":").length;i++)
                        value+=strCurrentLine.split(":")[i];
                    yamlKey.put(key,value);

                    for (Map.Entry<String, String> entry : yamlKey.entrySet()) {
                        if (entry.getKey().equals(msg_code)) {
                            if(msg_code.equals("open-channel")) {
                                value = entry.getValue().replace("{problem}", (String) vars.get(0));
                                value = value.replace("{service}", (String) (vars.get(1)));
                                return value;
                            }
                            int a= (int)vars.get(0);
                            int b= (int)vars.get(1);
                            int x= (int)vars.get(2);
                            int y= (int)vars.get(2);


                            value = value.replace("{a}", "" + a);
                        value = value.replace("{b}", "" +b);
                        value = value.replace("{x}", "" +x);
                        value = value.replace("{y}", "" + y);
                        int sumAB = a +b;
                        int prodAB = a * b;
                        int sumXY = x + y;
                        int prodXY = x *y;
                        value = value.replace("{a+b}", "" + sumAB);
                        value = value.replace("{a*b}", "" + prodAB);
                        value = value.replace("{x+y}", "" + sumXY);
                        value = value.replace("{x*y}", "" + prodXY);
                        return value;
                    }




                    }
                }
            }
        }catch (IOException e) {
            e.printStackTrace();
        }
        return redition_of_the_hardcoded_MSG;
    }

}

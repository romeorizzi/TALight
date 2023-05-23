import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;

public class sum_and_product_server {
    public static void main(String[] args) {
        TALinputs TALinput = new TALinputs();
        String problem = "sum";
        String service= "sum_and_product";
        Map<String,String>args_list=new HashMap<>();
        args_list.put("num_questions","int");
        args_list.put("numbers","String");
        args_list.put("lang","String");
        args_list.put("META_TTY","String");
        System.out.println(args.length);
        Env env= new Env(problem,service,args_list);
        TALcolors TAc = new TALcolors();
        Lang lang = new Lang(env,TAc,service,true);
        TAc.print(lang.opening_msg,"green",null,null);
        System.out.println("");
        int x = 0;
        int y = 0;
        Random randrange = new Random();
        boolean gen_new_pair = true;

        for(int i=0;i <(int)env.ENV("NUM_QUESTIONS");i++) {
            if (env.ENV("NUMBERS").equals("onedigit")) {
                x = randrange.nextInt(10);
                y = randrange.nextInt(10);
            } else if (env.ENV("NUMBERS").equals("twodigits")) {
                x = randrange.nextInt(100);
                y = randrange.nextInt(100);
            } else {
                x = randrange.nextInt(2 * 32);
                y = randrange.nextInt(2 * 32);
            }
            int sum = x + y;
            int prod = x * y;
            List<String> carFormat = new ArrayList<>();
            carFormat.add("bold");
            TAc.print(sum + " " + prod, "yellow", carFormat, null);

            List<Object> vars = new ArrayList<>();
            vars = TALinput.TALinput("int", 2, TAc);
            int a = (int) vars.get(0);
            int b = (int) vars.get(1);
            vars.add(x);
            vars.add(y);
            if (a + b > x + y) {
                TAc.NO();
                TAc.print(lang.render_feedback("over-sum", "No! indeed,%d+%d=%d>%d.", vars), "yellow", null, null);
            } else if (a + b < x + y) {
                TAc.NO();
                TAc.print(lang.render_feedback("under-sum", "No! indeed,%d+%d=%d>%d.", vars), "yellow", null, null);
            } else if (a * b > x * y) {
                TAc.NO();
                TAc.print(lang.render_feedback("over-product", "No! indeed,%d+%d=%d>%d.", vars), "yellow", null, null);
            } else if (a * b < x * y) {
                TAc.NO();
                TAc.print(lang.render_feedback("under-product", "No! indeed,%d+%d=%d>%d.", vars), "yellow", null, null);
            } else {
                TAc.OK();
                TAc.print(lang.render_feedback("ok", "No! indeed,%d+%d=%d>%d.", vars), "yellow", null, null);
                gen_new_pair = false;
            }
        }
        TAc.Finished();
        System.exit(0);
    }
}

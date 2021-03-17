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
        args_list.put("NUM_QUESTIONS","int");
        args_list.put("NUMBERS","String");
        args_list.put("LANG","String");
        args_list.put("ISATTY","String");

        Env env= new Env(problem,service,args_list);
        TALcolors TAc = new TALcolors();

        Scanner scan = new Scanner(System.in);
        String spoon = "";
        String numbers = "";
        int num_question=0;
        int x = 0;
        int y = 0;
        Random randrange = new Random();
        boolean gen_new_pair = true;

        for(int i=0;i <(int)env.ENV("NUM_QUESTIONS");i++) {
            if(env.ENV("NUMBERS").equals("onedigit")) {
                x= randrange.nextInt(10);
                y=randrange.nextInt(10);
            }
            else if(env.ENV("NUMBERS").equals("twodigits")) {
                x=randrange.nextInt(100);
                y=randrange.nextInt(100);
            }
            else {
                x=randrange.nextInt(2*32);
                y=randrange.nextInt(2*32);
            }
            int sum = x+y;
            int prod=x*y;
            List<String> carFormat = new ArrayList<>();
            carFormat.add("bold");
            TAc.print("? "+sum +" "+ prod,"yellow",carFormat,null);
            spoon = scan.nextLine();
            while(spoon.charAt(0)=='#') {
                spoon=scan.nextLine();
            }
            List<Object> vars=new ArrayList<>();
            vars=TALinput.TALinput("int",2,TAc);
            int a=(int)vars.get(0);
            int b= (int)vars.get(1);
            gen_new_pair = false;
            if (a+b > x+y)
                System.out.println("No! indeed,"+a+ "+"+b+"="+(a+b)+">"+(x+y)+".");
            else if (a+b < x+y)
                System.out.println("No! indeed,"+a+ "+"+b+"="+(a+b)+"<"+(x+y)+".");
            else if (a*b > x*y)
                System.out.println("No! indeed,"+a+ "*"+b+"="+(a*b)+">"+(x*y)+".");
            else if (a*b < x*y)
                System.out.println("No! indeed,"+a+ "*"+b+"="+(a*b)+">"+(x*y)+".");
            else {
                System.out.println("Ok! indeed,"+a+ "+"+b+"="+(a+b)+" and"+a+"*"+b+"="+(a*b)+".");
                gen_new_pair = false;
            }

        }
        System.exit(0);
    }
}
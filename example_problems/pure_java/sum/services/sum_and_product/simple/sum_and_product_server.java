import java.util.Scanner;
import java.util.Map;
import java.util.Random;

public class sum_and_product_server {

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String spoon = "";
        String numbers = "";
        int num_question=0;
        int x = 0;
        int y = 0;
        Random randrange = new Random();

        Map <String, String> map = System.getenv();
        for (Map.Entry <String, String> entry: map.entrySet()) {

            if(entry.getKey().equals("TAL_NUMBERS"))
                numbers= entry.getValue();
            if(entry.getKey().equals("TAL_NUM_QUESTIONS"))
                num_question= Integer.parseInt(entry.getValue());

        }
        System.out.println(numbers);
        System.out.println(num_question);
        boolean gen_new_pair = true;
        for (int i=0;i<num_question;i++) {
            if(numbers.equals("onedigit")) {
                x= randrange.nextInt(10);
                y=randrange.nextInt(10);
            }
            else if(numbers.equals("twodigits")) {
                x=randrange.nextInt(100);
                y=randrange.nextInt(100);
            }
            else {
                x=randrange.nextInt(2*32);
                y=randrange.nextInt(2*32);
            }
            int sum = x+y;
            int prod=x*y;
            System.out.println("? "+sum + " "+prod);
            spoon = scan.nextLine();
            while(spoon.charAt(0)=='#') {
                spoon=scan.nextLine();
            }
            int a = Integer.parseInt(spoon.split(" ")[0]);
            int b = Integer.parseInt(spoon.split(" ")[1]);
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
    /*
    if gen_new_pair:
        if ENV['numbers'] == "onedigit":
            x = randrange(10)
            y = randrange(10)
        elif ENV['numbers'] == "twodigits":
            x = randrange(100)
            y = randrange(100)
        else:
            x = randrange(2**32)
            y = randrange(2**32)
    print(f"? {x+y} {x*y}")
        System.exit(0);

    }
}

/*


        while (true) {
            spoon = scan.nextLine();
            while (!(spoon.charAt(0) == '?')) {
                spoon = scan.nextLine();
            }
            int s = Integer.parseInt(spoon.split(" ")[1]);
            int p = Integer.parseInt(spoon.split(" ")[2]);
	    int delta = (int) Math.sqrt(s * s - 4 * p);
	    int x1 = (s - delta) / 2;
	    int x2 = s - x1;
	    System.out.println(x1 + " " + x2);
        }
    }
}

ENV={}
ENV['numbers'] = environ["TAL_numbers"]
ENV['num_questions'] = int(environ["TAL_num_questions"])

print(f"# I will serve: problem=sum, service=sum_and_product, numbers={ENV['numbers']}, num_questions={ENV['num_questions']}.")

gen_new_pair = True
for _ in range(ENV['num_questions']):
    if gen_new_pair:
        if ENV['numbers'] == "onedigit":
            x = randrange(10)
            y = randrange(10)
        elif ENV['numbers'] == "twodigits":
            x = randrange(100)
            y = randrange(100)
        else:
            x = randrange(2**32)
            y = randrange(2**32)
    print(f"? {x+y} {x*y}")
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_pair = False
    if a+b > x+y:
        print(f"No! indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:
        print(f"No! indeed, {a}+{b}={a+b} < {x+y}.")
    elif a*b > x*y:
        print(f"No! indeed, {a}*{b}={a*b} > {x*y}.")
    elif a*b < x*y:
        print(f"No! indeed, {a}*{b}={a*b} < {x*y}.")
    else:
        assert (a + b == x+y) and (a * b == x*y)
        print(f"Ok! indeed, {a}+{b}={x+y} and {a}*{b}={x*y}.")
        gen_new_pair = True

exit(0)
*/

/*


        while (true) {
            spoon = scan.nextLine();
            while (!(spoon.charAt(0) == '?')) {
                spoon = scan.nextLine();
            }
            int s = Integer.parseInt(spoon.split(" ")[1]);
            int p = Integer.parseInt(spoon.split(" ")[2]);
	    int delta = (int) Math.sqrt(s * s - 4 * p);
	    int x1 = (s - delta) / 2;
	    int x2 = s - x1;
	    System.out.println(x1 + " " + x2);
        }
    }
}

ENV={}
ENV['numbers'] = environ["TAL_numbers"]
ENV['num_questions'] = int(environ["TAL_num_questions"])

print(f"# I will serve: problem=sum, service=sum_and_product, numbers={ENV['numbers']}, num_questions={ENV['num_questions']}.")

gen_new_pair = True    
for _ in range(ENV['num_questions']):
    if gen_new_pair:
        if ENV['numbers'] == "onedigit":
            x = randrange(10)
            y = randrange(10)
        elif ENV['numbers'] == "twodigits":
            x = randrange(100)
            y = randrange(100)
        else:
            x = randrange(2**32)
            y = randrange(2**32)
    print(f"? {x+y} {x*y}")
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_pair = False
    if a+b > x+y:
        print(f"No! indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:    
        print(f"No! indeed, {a}+{b}={a+b} < {x+y}.")
    elif a*b > x*y:    
        print(f"No! indeed, {a}*{b}={a*b} > {x*y}.")
    elif a*b < x*y:    
        print(f"No! indeed, {a}*{b}={a*b} < {x*y}.")
    else:
        assert (a + b == x+y) and (a * b == x*y)
        print(f"Ok! indeed, {a}+{b}={x+y} and {a}*{b}={x*y}.")
        gen_new_pair = True

exit(0)
*/

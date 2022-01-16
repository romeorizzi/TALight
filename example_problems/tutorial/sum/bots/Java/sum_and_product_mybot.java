import java.util.Scanner;
import static java.lang.Math.sqrt;

public class sum_and_product_mybot {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String line = "";
        while (true) {
            line = scan.nextLine();
	    if(line.charAt(0) == '#') {   // line contains a commented line from the service server
		if(line.equals("# WE HAVE FINISHED")) {
		    System.exit(0);   // exit upon termination of the service server
		}
	    }
	    else {
		int s = Integer.parseInt(line.split(" ")[0]);
		int d = Integer.parseInt(line.split(" ")[1]);
		int rad = (int) sqrt(s * Integer.parseInt(s) - 4 * p);
		int x1 = (s - rad) / 2;
		int x2 = s - x1;
		System.out.println(x1 + " " + x2);
            }
        }
    }
}

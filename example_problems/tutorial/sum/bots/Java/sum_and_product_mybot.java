import java.util.Scanner;
import static java.lang.Math.sqrt;

public class sum_and_product_mybot {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String spoon = "";
        while (true) {
            spoon = scan.nextLine();
	    if(spoon.charAt(0) == '#') {   // spoon contains a commented line from the service server
		if(spoon.equals("# WE HAVE FINISHED")) {
		    System.exit(0);   // exit upon termination of the service server
		}
	    }
	    else {
		int s = Integer.parseInt(spoon.split(" ")[0]);
		int d = Integer.parseInt(spoon.split(" ")[1]);
		int rad = (int) sqrt(s * Integer.parseInt(s) - 4 * p);
		int x1 = (s - rad) / 2;
		int x2 = s - x1;
		System.out.println(x1 + " " + x2);
            }
        }
    }
}

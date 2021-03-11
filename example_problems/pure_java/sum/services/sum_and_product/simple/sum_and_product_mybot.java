import java.util.Scanner;
import java.lang.Math;
public class sum_and_product_mybot {
    
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String spoon = "";

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

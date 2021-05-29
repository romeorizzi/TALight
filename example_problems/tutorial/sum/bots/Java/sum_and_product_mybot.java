import static java.lang.Math.sqrt;

import java.util.Scanner;

public class sum_and_product_mybot {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String spoon = "";
        String s, p = "";
        int x1, x2;

        while (true) {
            spoon = scan.nextLine();
	    if(!spoon[0].equals("#")) {
		s = spoon.split(" ")[0];
		p = spoon.split(" ")[1];
		int rad = (int) sqrt(Integer.parseInt(s) * Integer.parseInt(s) - 4 * Integer.parseInt(p));
		x1 = (Integer.parseInt(s) - rad) / 2;
		x2 = Integer.parseInt(s) - x1;
		System.out.println(x1 + " " + x2);
            }
        }
    }
}

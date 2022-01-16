import java.util.Scanner;

public class free_sum_mymaxproductbot {
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
		int n = Integer.parseInt(spoon);
		System.out.println(n / 2 + " " + (n + 1) / 2);
            }
        }
    }
}

import java.util.Scanner;

public class free_sum_mysimplebot {
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
		int n = Integer.parseInt(line);
		System.out.println(n + " 0");
	    }
        }
    }
}

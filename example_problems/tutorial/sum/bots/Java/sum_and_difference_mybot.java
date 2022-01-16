import java.util.Scanner;

public class sum_and_difference_mybot {
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
		int x1 = (s + d) / 2;
		int x2 = (s - d) / 2;
		System.out.println(x1 + " " + x2);
            }
        }

    }
}

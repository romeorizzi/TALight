import java.util.Scanner;
class saluta {
    public static void main(String[] args) {
	Scanner scan = new Scanner(System.in);
	String name = "";
	System.out.println("What's your name?\nPlease, insert your name: ");
	name = scan.nextLine();
        System.out.println("Hello, " + name); 
    }
}

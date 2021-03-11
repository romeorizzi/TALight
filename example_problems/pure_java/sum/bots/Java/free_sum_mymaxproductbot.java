import java.util.Scanner;
public class free_sum_mymaxproductbot {
    
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String spoon = "";
        int n;

        while (true) {
            spoon = scan.nextLine();
            while (!(spoon.charAt(0) == '?')) {
                spoon = scan.nextLine();
            }
            n = Integer.parseInt(spoon.split(" ")[1]);

            System.out.println(n / 2 + " " + (n + 1) / 2);
        }
    }
}

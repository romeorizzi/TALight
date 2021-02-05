

import java.util.Scanner;

public class sum_and_difference_mybot {

    public static void main(String[] args) {
      Scanner scan = new Scanner(System.in);
      String spoon ="";
      do {
       spoon = scan.nextLine();
       if(spoon.split(" ").length!=3) {
           System.out.println("Devi inserire due numeri separati da spazio dopo il ?");
           return;
       }
      }while(!"?".equals(spoon.split(" ")[0]));
      int s = Integer.parseInt(spoon.split(" ")[1]);
      int d = Integer.parseInt(spoon.split(" ")[2]); 
      int x1 = (s + d) / 2;
      int x2 = (s - d) / 2;
      System.out.println(x1 + " "+x2);
    }
    
}

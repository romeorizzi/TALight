public class sum_mymaxproductbot {


    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String spoon ="";
        String s,p ="";
        int x1,x2;
        int n;

        while(true) {
            spoon=scan.nextLine();
            while(!spoon.split(" ")[0].equals("?")) {
                spoon=scan.nextLine();
            }
            n=Integer.parseInt(spoon.split(" ") [1]);

            System.out.println(n/2 + " "+(n+1)/2);
        }
    }
}

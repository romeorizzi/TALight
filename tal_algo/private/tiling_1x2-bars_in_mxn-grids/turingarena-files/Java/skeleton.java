import java.util.Scanner;

abstract class Skeleton {
    private static final Scanner in = new Scanner(System.in);

    static final int H = 0;
    static final int V = 1;

    abstract int is_tilable(int m, int n);

    interface Compose_tilingCallbacks {
        void place_tile(int row, int col, int dir);
    }
    abstract void compose_tiling(int m, int n, Compose_tilingCallbacks callbacks);

    public static void main(String[] args) {
        Solution __solution = new Solution();

        // checkpoint
        System.out.printf("%d\n", 0);
        // read m, n
        int n;
        int m;
        System.out.flush();
        m = in.nextInt();
        n = in.nextInt();
        // call res = is_tilable(m, n)
        int res;
        res = __solution.is_tilable(m, n);
        // write res
        System.out.printf("%d\n", res);
        // if res {...}
        if (res != 0) {
            // read choice
            int choice;
            System.out.flush();
            choice = in.nextInt();
            // if choice {...}
            if (choice != 0) {
                // read m1, n1
                int m1;
                int n1;
                System.out.flush();
                m1 = in.nextInt();
                n1 = in.nextInt();
                // call compose_tiling(m1, n1) callbacks {...}
                Compose_tilingCallbacks compose_tilingCallbacks = new Compose_tilingCallbacks() {
                    public void place_tile(int row, int col, int dir) {
                        // callback place_tile
                        System.out.printf("%d %d\n", 1, 0);
                        // write row, col, dir
                        System.out.printf("%d %d %d\n", row, col, dir);
                    }
                };
                __solution.compose_tiling(m1, n1,  compose_tilingCallbacks);
                // no more callbacks
                System.out.printf("%d %d\n", 0, 0);
            }
        }
        // exit
        System.exit(0);
    }
}

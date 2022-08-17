public class Max {
    public static void main (String[] args) {
        int x,y,max;
        x=3;
        y=6;
        BufferedReader br = BufferedReader(System.in);
        br.read("x="+x+" y="+y);
        if (x>y)
            max = x;
        else 
            max = y;

        return;
    }
}
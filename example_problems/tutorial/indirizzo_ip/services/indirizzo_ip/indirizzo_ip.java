import java.util.*;
class Indirizzo_ip{
    public static void main(String[] args) {
            int n1,n2,n3,n4,punteggio=0;
            
        while(punteggio<10){
            int numeroSubNet=(int)(Math.random()*4)+1;
            if(numeroSubNet==1){
                n1=(int)(Math.random()*256)+1;
                n2=(int)(Math.random()*256)+1;
                n3=(int)(Math.random()*256)+1;
                n4=0;
                System.out.print("255.255.255.0     SUBNET MASK\n");
                System.out.print(n1+"."+n2+"."+n3+"."+n4+"      INDIRIZZO DI RETE\n");
            }
            else if(numeroSubNet==2){
                n1=(int)(Math.random()*256)+1;
                n2=(int)(Math.random()*256)+1;
                n3=0;
                n4=0;
                System.out.print("255.255.0.0     SUBNET MASK\n");
                System.out.print(n1+"."+n2+"."+n3+"."+n4+"      INDIRIZZO DI RETE\n");
            }
            else{
                n1=(int)(Math.random()*256)+1;
                n2=0;
                n3=0;
                n4=0;
                System.out.print("255.0.0.0     SUBNET MASK\n");
                System.out.print(n1+"."+n2+"."+n3+"."+n4+"      INDIRIZZO DI RETE\n");
            }
            
            System.out.println("Inserire un indirizzo ip appartenente all'indirizzo di rete qui sopra\n");
            
            //input da parte dell'utente
            Scanner sc=new Scanner(System.in);
            String input;
            
            input=sc.nextLine();
            int numeri []=new int[4];
    
             String[] separatedStrings = input.split("[.]");
            
                
             for (int i = 0; i <separatedStrings.length; i++) {
                
                    numeri[i] = Integer.parseInt(separatedStrings[i]);
                    
                }
          
            
            if(numeroSubNet==1){
                while((numeri[0]!=n1)||(numeri[1]!=n2)||(numeri[2]!=n3)||(numeri[3]>256)){
                    System.out.println("SBAGLIATO\nRIPROVA\n");
                    
                    input=sc.nextLine();
                    separatedStrings = input.split("[.]");
                    for (int i = 0; i <separatedStrings.length; i++) {
                         numeri[i] = Integer.parseInt(separatedStrings[i]);
                    }
                }   
                System.out.println("GIUSTO\n\n");
                punteggio++;
            }
            else if(numeroSubNet==2){
                while((numeri[0]!=n1)||(numeri[1]!=n2)||(numeri[2]>256)||(numeri[3]>256)){
                    System.out.println("SBAGLIATO\nRIPROVA\n");
                
                    input=sc.nextLine();
                    separatedStrings = input.split("[.]");
                    for (int i = 0; i <separatedStrings.length; i++) {
                         numeri[i] = Integer.parseInt(separatedStrings[i]);
                    }
                    
                }    
                System.out.println("GIUSTO\n\n");
                punteggio++;
            }
            else{
                while(numeri[0]!=n1 || (numeri[1]>256 || numeri[2]>256 || numeri[3]>256)){
                   System.out.println("SBAGLIATO\nRIPROVA\n");
                
                    input=sc.nextLine();
                    separatedStrings = input.split("[.]");
                    for (int i = 0; i <separatedStrings.length; i++) {
                         numeri[i] = Integer.parseInt(separatedStrings[i]);
                    }
                }   
                System.out.println("GIUSTO\n\n");
                punteggio++;
            }
        }
        System.out.println("Complimenti hai completato il problema, hai totalizzato 10/10 punti");
    }
}
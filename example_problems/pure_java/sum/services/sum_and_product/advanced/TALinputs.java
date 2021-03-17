/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


/**
 *
 * @author UTENTE
 */
import java.util.Scanner;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.Random;

public class TALinputs {

    Scanner scan = new Scanner(System.in);
    private char ignore_lines_starting_with='#';

    public List<Object> TALinput(String type,int num,TALcolors TAc) {
        List<Object> input = new ArrayList<>();
        String spoon =scan.nextLine();
        while(spoon.charAt(0)==ignore_lines_starting_with)
            spoon = scan.nextLine();


        if(spoon.length()==0) {
            System.out.println("You have entered an unexpected empty line. I assume you want to drop this TALight service call. See you next time ;))");
            System.exit(0);
        }

        if(spoon.charAt(0)!=ignore_lines_starting_with) {
            String [] vals = spoon.split(" ");
            if(num==vals.length) {
                if(type.equals("int")) {
                    for(int i=0;i<num;i++) {
                        input.add(Integer.parseInt(vals[i]));
                    }
                }

                if(type.equals("string")) {
                    for(int i=0;i<num;i++) {
                        input.add(vals[i]);
                    }
                }
                if(type.equals("float")) {
                    for (int i = 0; i < num; i++) {
                        input.add(Float.parseFloat(vals[i]));
                    }
                }
                else {
                    TAc.print(type + "is not supported","red",null,null);
                }
            }
            else {
                TAc.print("the number of parameter that I expected is not equal to your number of parameters","red",null,null);
            }
        }
        return input;
    }
}
    /*
   

def TALinput(tokens_type, regex="^((\S)+)$", regex_explained=None, ignore_lines_starting_with='#'):
    while True:
        spoon = input()
        if len(spoon) == 0:
            print(f"You have entered an unexpected empty line. I assume you want to drop this TALight service call. See you next time ;))")
            exit(0)
        if spoon[0] not in ignore_lines_starting_with:
            break
    tokens = spoon.split() 
    if len(tokens) != len(tokens_type):
        for out in [stdout, stderr]:
            print(f"Input error from the problem-solver: the server was expecting a line with {len(tokens_type)} tokens but the line you entered:\n{spoon}\ncontains {len(tokens)} != {len(tokens_type)} tokens.\n\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
        exit(0)
    vals = []
    for tk, tk_type, i in zip(tokens,tokens_type,range(1,1+len(tokens))):
        vals.append(try_to_convert(tk, tk_type,regex))
        if vals[-1] == None:
            if tk_type == str:
                for out in [stdout, stderr]:
                    print(f"Input error from the problem-solver:  when parsing the {i}-th token of your input line, namely the string:\n{tk}\nthe server was actually expecting a string matching the regex:\n{regex}\nbut the string you entered does not comply the regex.\n", file=out)
                    if regex_explained != None:
                        print(f"In practice, the expected string should be either 'end' (to close the input) or {regex_explained}", file=out)
                    print(f"\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
            else:
                for out in [stdout, stderr]:
                    print(f"Input error from the problem-solver: the server was expecting a token of type {tk_type} when it got the token '{tk}'.\n\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
            exit(1) 
    return (val for val in vals)

*/

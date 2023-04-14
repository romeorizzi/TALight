/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication17;

/**
 *
 * @author UTENTE
 */
import java.util.Scanner;
import java.util.Map;
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class sum_and_product_server {
    Scanner scan = new Scanner(System.in);
    public Object try_to_convert(Object tk,Object tk_type,String regex) {
       
        
        if (tk_type instanceof Integer)
          return (Integer)tk;
            
        else  if (tk_type instanceof Float)
                return (Float)tk;
        else  if (tk_type instanceof String) {
            if((tk.toString().toUpperCase().equals("END")))
                return "end";
            Matcher matcher = Pattern.compile(regex).matcher(regex);
            boolean matched=matcher.matches();
            if(matched)
                return true;
            else
                return null;
        }
        else {
           System.out.println("Internal error (please, report it to the problem maker): the TALinputs library does not support the " +tk_type +"token type. The problem maker should either extend the library or adapt to it.");     
        }  System.exit(1);
        return null;   
    }
    public void TALinput() {
        while(true) {
            char ignore_lines_starting_with='#';
            String spoon = scan.nextLine();
            if(spoon.length()==0) {
               System.out.println("You have entered an unexpected empty line. I assume you want to drop this TALight service call. See you next time ;))");
               System.exit(0);
            }
            if(spoon.charAt(0)!=ignore_lines_starting_with)
        }
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

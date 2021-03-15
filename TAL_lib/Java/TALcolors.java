/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


/**
 *
 * @author UTENTE
 */
import java.util.Map;

public class TALcolors {
    public int num_NO=0;
    public int num_OK=0;
    private String msg_style ="";
    private String colors="";
    colorOption co=new colorOption();
    boolean colored_print = Boolean.parseBoolean(System.getenv("TAL_ISATTY"));

    public void print(String msg_text,String color,Object characterFormats,String end){
        if(characterFormats!=null)
            this.msg_style=characterFormats.toString();
        if(color !=null) {
            if(color.equals("red")) {
                System.out.println(co.color16(colorOption.Color16.FG_RED,msg_text));
            }
            if(color.equals("green")){
                System.out.println(co.color16(colorOption.Color16.FG_GREEN,msg_text));
            }
            if(color.equals("white")) {
                System.out.println(co.color16(colorOption.Color16.FG_WHITE,msg_text));
            }

        }


    }
    public void NO(){
        num_NO+=1;
        this.print("No!","red",null,"");
    }
    public void OK(){
        num_OK+=1;
        this.print("OK", "green", null,"");
    }
    public void GoBored(){
        this.print("!(I got bored", "white",null, null);
    }
    public void Finished() {
        this.print("!(We have finished)Correct answers:"+this.num_OK+"/"+(this.num_OK+this.num_NO),"white",null,null);
    }



}


/*
from sys import stdout, stderr, exit, argv
from os import environ
from os.path import join, split

termcolor_is_installed = True
try:
    from termcolor import colored, cprint
except Exception as e:
    termcolor_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package termcolor.)", file=stderr)

err_ruamel = None
yaml_is_installed = True
try:
    import ruamel.yaml
except Exception as e:
    yaml_is_installed = False
    err_ruamel = e
class TALcolors:
    def __init__(self, ENV):
        self.numNO = 0
        self.numOK = 0
        self.colored_print = ENV["ISATTY"] and termcolor_is_installed

    def print(self, msg_text, *msg_rendering, **kwargs):
      if type(msg_rendering[-1]) == list:
          msg_style = msg_rendering[-1]
          msg_colors = msg_rendering[:-1]
      else:
          msg_style = []
          msg_colors = msg_rendering
      if self.colored_print:
          print(colored(msg_text, *msg_colors, attrs=msg_style), **kwargs)
      else:
          print(msg_text, **kwargs)

    def NO(self):
        self.numNO += 1
        self.print("No! ", "red", ["blink", "bold"], end="")

    def OK(self):
        self.numOK += 1
        self.print("OK! ", "green", ["bold"], end="")

    def GotBored(self):
        self.print("! (I got bored)", "white")

    def Finished(self):
        self.print(f"! (We have finished) Correct answers: {self.numOK}/{self.numOK+self.numNO}", "white")

*/
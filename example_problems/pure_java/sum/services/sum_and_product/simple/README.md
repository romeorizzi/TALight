## How to make the bytecode of a java source:

javac hello_world.java

How to call for the execution of the bytecode from the JVM:

java hello_world

Other examples:

javac saluta.java
java saluta

javac free_sum_mysimplebot.java
java free_sum_mysimplebot

javac free_sum_mymaxproductbot.java
java free_sum_mymaxproductbot

## How to make the .jar file from a java source:

1. compile the java source.
   example:
      javac sum_and_product_server.java 

2. create the file:
      myfile.mf
   with the following minimal content (the name of the starting class for the bundle):
romeo-prompt$ cat myfile.mf
Main-Class: sum_and_product_server
romeo-prompt$

3. launch the jar archiving command:
      jar -cvmf myfile.mf sum_and_product_server.jar sum_and_product_server.class 


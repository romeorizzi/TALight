# What is TAlight

Are you a teacher or passionate about transmitting some problem solving competences/technique/methods or proposing an interesting and instructive challenge?
TAlight offers you the perfect tool for you to make up your favorite problem into a full fledged didactic inclusive Montessori toy, allowing to organize and offer smooth interactive didactic paths around it and automatic feedback services to promote autonomous exploration and learning.
Also the social dimension is empowered:

Do you want to become a problem maker but know only one programming language?

TAlight is a minimal but powerful system for the design, the sharing, the experimentation and the use of interactive didactic problems which offer rich ongoing instant feedback services to the problem solver (the student or trainee).

Most problems in TAlight are of an algorithmic nature.
This repository offers TAlight plus some example problems working under TAlight.
These problems prompt and stimulate the student and are meant also to show how making new interesting problem under TAlight is in their and in your reach.
TAlight is meant to be simple to work with.
Among its commitments in our vision come:

1. no one left behind: the feedback provided to the students should be rich and stimulating
2. brake on through to the other side: when solving problems and interacting with the system, problem solvers should grow autonomous and get the desire and competence to become a problem maker
3. to be a problem maker the knowledge f one single programming language of your choice (and just the basics of it) should be enough
4. possible to design didactic projects articulated on problems meant as Montessori games
5. possible for teachers to share and collaborate on these didactic projects
6. no installation required, neither for the problem solvers nor for the problem makers.

## DOWNLOAD

Open a shell, go to your home directory, and enter:

```bash
git checkout git@github.com:romeorizzi/TAlight.git
```
to download the content of this repo. Of course, you can achieve the sam result by any other means if you prefer. 

## OBTAIN THE BINARIES

TAlight consists of two programs, the `rtal` client, and the `rtald` server.
After downloading this TAlight project public repo, you can either choose to use the binaries made available for your platform (not yet made available at present) or compile them from the source code.
How to make these two binaries and the basic on how to use them is explained in the file `rtal/README.md` of this repo.

In the following we assume that the files `~/TAlight/rtal/target/debug/rtal` and `~/TAlight/rtal/target/debug/rtald` exist on your machine and have excution permission.
You can check this with

```bash
~/TAlight/rtal/target/debug/rtal --help
```
and

```bash
~/TAlight/rtal/target/debug/rtald --help
```

which should also list out the parameters and subcommands of these `TAlight` commands.

## SETUP OF THE PATH ENVIRONMENT VARIABLE

Having to remember and digit the whole path `~/TAlight/rtal/target/debug/` in order to use the `TAlight` commands will soon appear too lengthy.
There are many ways to solve this nuisance, like copying the binaries into a directory listed into the `PATH` environment variable on your system, or adding the path `~/TAlight/rtal/target/debug/` to your `PATH` environment variable.
Here we suggest a convenint way to make the `TAlight` commands directly accessible, it can be applied on any platform that allows for simlinks (or hardlinks). We word it out step by step for Unix/Linux/Mac: 


From the terminal,
lounch the following commands
```bash
mkdir ~/.bin
cd ~/.bin
ln -s ~/TAlight/rtal/target/debug/rtald ~/.bin/
ln -s ~/TAlight/rtal/target/debug/rtal ~/.bin/
```

Then, add the following line at the end of your `~/.bashrc` file.

```bash
export PATH="$PATH:$HOME/.bin"
```

Remember that this update will be effective only for terminals you open after having modifyied the `~/.bashrc` file.
If you want older terminals to get the update then you can issue from them the command
```bash
source .bashrc
```

Again, you can check that the `TAlight` commands are now directly accessible with

```bash
rtal --help
```
and

```bash
rtald --help
```


## TUTORIAL (How to use TAlight)

In the examples we offer in this tutorial we assume the use of a POSIX-like shell. 

#### PREAMBLE

Once the two executable `rtal` and `rtald` are built and conveniently available then you can already use `TAlight` both in local and in connection to an external server exposing TAlight problems and other material for a course, a didactic path or project, a competition, a scouting selection, a challenge, or a game.
Whether you are a problem solver (usually a student) or a problem maker (usually a teacher, or a senior student), a general truth and assumption in `TAlight` is that working first in local, whenever possibile, is the best way to experiment, learn and develop. You go out in the wide when ready. Active learning is better organized as a multistage process.

After downloading this repo you already have on your machine 
a set of working test problems to experiment with, and this section offers you a tutorial on them.
The first thing to understand is the way the server and the client interact. This can be confusing at first but every mistery will soon be dispelled. Though the `rtald` command might not be necessary (at least in principle) to the student in certain settings, for experimenting with the problems in our tutorial you need to launch both the server and the client and let them interact. The server `rtald` is the deamond and you need to activate it first, then you can issue many requests to it through the client `rtal`. The server offers two main modalities of activation:

1. `rtald` activated to serve requests concerning problems sitting on your local machine and coming from the local client.

2. `rtald` activated to serve requests concerning problems sitting on your local machine and coming from clients on other machines but reaching it through the internet. In this case your `rtald` daemon will need the bind address and the port from where to listen from the outside world and on which to establish connection with other `rtald` deamons.

In this tutorial we start with examples concerning modality 1 since all main features appear there.
In particular, this is certainly true with the problems of this tutorial that are entirely public and already downloaded with this repo.
Moreover, working in local prompts you to action, makes for a more concrete understanding, and fosters your experimental attitudes and skills which is one of the goals of `TAlight`.
As a problem solver, the time to connect to the internet comes only when you want to work on problems that (in full or in part) are not openly published (competitions, exams, didactic reasons, privacy reasons, copyright reasons, ...) or to multiplayer problems or games.
As a problem maker, you should consider offering the services for a problem from an internet server when your aim is to manage a competition, scouting selection, exam, or you want to offer a challenge through the internet with some control on the flow of information (for example when with your problems you want to instruct and fideize clients to a product). Or possibly when you want to offer a very user friendly and attractive service.
When creating a problem and designing, implementing and experimenting its services within `TAlight` you do not need to offer these services online through an internet server. You can experiment them in local and share them by other means with other problem solvers or makers and collaborators to that project. Each of these recipients will have the possibility to make them alive in local with the open source `TAlight` platform.
In good conclusion, you need modality 2 almost only to offer a service on the web for problems where some services to the problem solver require pieces that for some reason you do not want to make public. Though the example problems are fully public (you download them as a whole with this repo), still their directory structure is organized as they were not. In the public directory of a problem it is customary to place links to all the materials of the problem that can be made public without spoilering in any way the problem (as for its intended use). 

## STARTING THE TAlight DAEMON

To operate with problems you have on your local machine, you first activate the `TAlight` daemon `rtald` on your machine to serve requests coming from your machine itself (modality 1).
When starting the daemon, it is a good idea to also turn on logging, by setting the environment variable `RUST_LOG=info`.
Both in modality 1 and in modality 2, you must specify to the deamon the directory containing the `TAlight` problems it should take care of. It is assumed that this directory is located on your local file system and each problem is a direct subdirectory of it.
In the case of the problems comprising this tutorial they are placed in the `~/TAlight/problems` directory. Therefore, you activate (in modality 1) the `TAlight` daemon with the following command from a terminal:

```bash
RUST_LOG=info rtald -d ~/TAlight/problems
```
The `rtald` daemon is now active and ready to serve requests concerning the problems present in the directory `~/TAlight/problems`.
The terminal where you issued its activation will now be the place where the server `rtald` updates you about the requests of service it receives and what is going on with them.
The help page of the `rtald` command lists its optional parameters that allow you to expose the service in the wide rather than just in local (modality 2).
Still, when creating and experimenting, you will launch `rtald` as above and operate with no need for an internet connection. Only at deploy time (and if the intended use asks for it) you will expose services for your problems to requests coming from the outside (modality 2).

Since the previous terminal is now the downstream channel of the daemon you have activated, in order to enjoy and explore the services it offers you need to open another terminal (I prefer vertically splitting my terminator so that I quickly perceive what is going on while experimenting) to send requests with your client `rtal` to the running daemon.
First, to list the problems available, and thus check that both the client and the server are working, try the following command:
```bash
rtal list
```
In the list of available problems at least the example problem `sum` should appear.

If you want to know more about the `list` subcommand of `rtal` you can, as for any other subcommand, try

```bash
rtal list --help
```

## Exploring the services available for a problem

To explore the services available for the example problem `sum` try issuing
```bash
rtal list sum -v
```
For this first `rtal` problem-set specific request, and for all the others that will follow, be told that if you want to address them to another server made available online (and serving the same problems) you simply need to use the `-s` option that is mentioned when you run `rtal --help`.

Either way, you should get something like
```bash
- sum
  * sum_and_product
    # numbers [onedigit] { ^(onedigit|twodigits|big)$ }
    # num_questions [10] { ^([1-9]|[1-2][0-9]|30)$ }
    # lang [it] { ^(en|it)$ }
  * sum_and_difference
    # lang [it] { ^(en|it)$ }
    # numbers [onedigit] { ^(onedigit|twodigits|big)$ }
    # num_questions [10] { ^([1-9]|[1-2][0-9]|30)$ }
  * sum
    # num_questions [10] { ^([1-9]|[1-2][0-9]|30)$ }
    # obj [any] { ^(any|max_product)$ }
    # numbers [twodigits] { ^(onedigit|twodigits|big)$ }
    # lang [it] { ^(en|it)$ }
```
From this you understand that three services (`sum`, `sum_and_difference`, and `sum_and_product`) are up for this problem on your local machine. All three services will conduct a dialogue where you (or a bot you designed to act in your place) will be asked 10 questions (all instances of a problem defined by the service). Indeed, 10 is the default value for the parameter `num_questions`. You can set a different value for this parameter as shown in the next `TAlight` request which sets it to 13.
However, you can set it only to integrs in the intrval $[1,30]$ as specified by the regexp `^([1-9]|[1-2][0-9]|30)$` reported above.
To know how to interpret (if a problem solver) or write (if a problem maker) these regexps, we refer you to [regexp syntax](https://docs.rs/regex/1.4.3/regex/#syntax). 

Combining the problem specific information you got above by issuing `rtal list sum -v` with the TAlight core instructions you get with `rtal connect --help` you could decide to try one of the following two services:

```bash
rtal connect -a num_questions=13 -a numbers=big sum sum_and_product
```

```bash
rtal connect -a numbers=big sum sum -- sum_mysolution.py
```

In the first case you will enjoy a direct interaction with the server through the terminal (this can be enough or anyhow play helpful to find out about the service and the protocol of the interaction).
In the second case you connect your local solution program or bot `sum_mysolution.py` to the server to check out how your method you have therein encoded performs.
Clearly the file `sum_mysolution.py` must have the correct permissions in order to be executed on your local system. In other words the file must be an excutable, but otherwise any programming language could have been used to produced it. 
If you want to observe the interaction between your bot and the server you can issue:

```bash
rtal connect -e -a numbers=small sum sum -- sum_mysolution.py
```

Problem `sum` also exemplifies how to interact with a service through a browser rather than through the terminal.
In this way and by resorting on HTML/CCS/JavaScript technology, nice applets running on the problem solver site can be designed for more user friendly interactions.
Just look in the `applets` directory of the project and run

```bash
~/TAlight/applets$ google-chrome sum-protoapplet.html
```
In this file, it is easy to spot out and substitute the hardcoded problem-specific parts and get an analogous page for a first browser mediated interaction also for other problems. One can start from here in order to develop ad-hoc applets specific to other problems and offer fun active learnig opportunities also to kids that do not yet know how to code.




## Vision (pezzi in Italiano)

Miriamo al promuovere lo sviluppo distribuito e condiviso di percorsi didattici funzionali alle proprie esigenze e finalità. Se diverrà facile per i docenti (e loro studenti) contribuire con problemi, ciò consentirà la realizzazione di un repository di percorsi didattici per problemi che possa venire costituito e popolato di problemi in modo distribuito e condiviso, in vari contesti e discipline.
TAlight non richiede alcuna installazione.
TAlight consente di affrontare in locale sia la soluzione che il design, la realizzazione, e testing in locale di un problema.
Al momento del deployment di servizi sul problema al docente basterà disporre di un web server modesto che potrà facilmente approntare senza spese. 
In futuro potremmo mirare a fornire noi stessi dei servizi di hosting gratuiti che forniranno ambienti per percorsi didattici spendibili in esercitazioni, lezioni, gare, o allenamento aperto. I problemi potranno così essere condivisi e percorsi didattici basati su problemi potranno essere realizzati in una rete collaborativa, come specifici a particolari esigenze e percorsi svolti in scuole lontane ed altrimenti isolate.

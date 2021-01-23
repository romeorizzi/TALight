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

## SETUP OF THE PATH ENVIRONMENT VARIABLE

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

## GENERAL USAGE

Once the two executable `rtal` (the rust implemntation of the TA-light client) and `rtald` (the rust implementation of the TA-light daemon) are placed in their directory (`~/TAlight/rtal/target/debug`) then you can already use `TAlight` both in local and in connection to an external server exposing TAlight problems and other material for a course or didactic path.
Whether you are a problem solver (usually a student) or a problem maker (usually a teacher, or a senior student), a general truth and assumption in `TAlight` is that working first in local, whenever possibile, is the best way to experiment, learn and develop. You go out in the wide when ready. Active learning is better organized as a multistage process.

After downloading this repo you already have on your machine 
a set of working test problems to experiment with, and this section offers you a tutorial on them.
To operate with problems in local, and in this case placed in the   
`~/TAlight/problems` directory, then you first lounch the `TAlight` daemond with the following command from a terminal:

```bash
RUST_LOG=info rtald -d ~/TAlight/problems
```
We refer to the file `rtal/README.md` of this repo to know more on this and for a more detailed tutorial. Also, both `rtal` and `rtald` have detailed `--help` sections.
Either way, if you are a problem maker or just interested in offering trough the internet the services for a collection of problems, you can find out how to use the needed option parameters of `rtald` that allow you to expose the service in the wide rather than just in local.
Still, when creating and experimenting, you will launch `rtald` as above and operate with no need for an internet connection. Only at deploy time you will publish your problems and services on some server where `rtald` is up and running to serve requests coming from the outside.

Now that `rtald` is activated and serving the services associated with the problems in the directory `~/TAlight/problems`, to enjoy and explore these services you need to open another terminal (I prefer vertically splitting my terminator so that I quickly perceive what is going on while experimenting) to send requests with your client `rtal`.
To list the problems available, and thus check that both the client and the server are working, try the following command:
```bash
rtal list
```
In the list of available problems at least the example problem `sum` should appear. 

To explore the services available for the example problem `sum` try issuing
```bash
rtal list sum -v
```
From the lines of explanation obtained from this command you understand that three services (`sum`, `sum_and_difference`, and `sum_and_product`) are up for this problem on your local machine. If you want to talk with another server made available online use the `-s` option that is mentioned when you run `rtal --help`.

Not only: Combining the problem specific information you got above by issuing `rtal list sum -v` with the TAlight core instructions you get with `rtal connect --help` you could decide to try the following service:

```bash
rtal connect -a numbers=big sum sum_and_product
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

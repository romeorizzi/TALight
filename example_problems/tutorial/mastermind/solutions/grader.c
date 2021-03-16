#include <stdio.h>
#include <stdlib.h>
 
using namespace std;

int maxAttempts;
int guesses;
FILE *file;

int secretCode[4] = {0}; //Codice da scoprire

extern void solve(); 

void checkCode(int attempt[], int result[]){
 
    result[0] = 0;
    result[1] = 0;
    int blacks[4] = {0};
    int whites[4] = {0};
 
 
    for(int i=0; i<4; i++)
    {
        if(attempt[i] == secretCode[i])
            blacks[i]=1;
        else
            blacks[i]=0;
    }
 
    for(int i=0; i<4; i++)
    {
        if(blacks[i]!=1)
        {
            for(int f=0; f<4; f++)
            {
                if(f==i) continue;
                if((attempt[i] == secretCode[f] && blacks[f] != 1))
                    if(whites[f] == 0)
                    {
                        whites[f]=1;
                        break;
                    }
            }
        }
    }
 
    for(int i=0; i<4; i++){
        result[0] += blacks[i];
        result[1] += whites[i];
    }

	if(result[0] != 4){
		guesses++;	
	}
 
}
 
void pensoCheCodiceSia(int risposta[]){
	fprintf(file, "%d %d\n", maxAttempts, guesses);
 
	for (int j = 0; j < 4; j++) {
			fprintf(file, "%d ", risposta[j]);
	}
	fprintf(file, "\n");
	fclose(file);

	exit(0);	
}
 
int main(){

	#ifdef EVAL
    file = fopen("input.txt", "r");
	#else
  	file = stdin;
	#endif

    int subtask, seed;

	fscanf(file, "%d", &subtask);
	fscanf(file, "%d", &seed);
    
	fclose(file);

	#ifdef EVAL
    file = fopen("output.txt", "w");
	#else 
    file = stdout;
	#endif

    srand(seed);

 	if(subtask == 0) maxAttempts = 1000000;
	if(subtask == 1) maxAttempts = 10;
	if(subtask == 2) maxAttempts = 6; // soluzione ottima (6 errate)

	for(int i = 0; i < 4; i++){
		secretCode[i] = rand()%6; 
	} 

    guesses = 0;
    
	solve();
	
    return 0;
}

/*      

Specchio (selezioni nazionali 2002)

Copyright (C) 2002 Paolo Boldi

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2, or (at your option) any
later version.
	
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
	
You should have received a copy of the GNU General Public License along
with this program; see the file COPYING.  If not, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.  

*/


#include <stdio.h>

/* Un nodo dell'albero contiene il numero N di figli, il puntatore (ult)
   all'ultimo figlio più a destra, e il puntatore (prec) al fratello di
   sinistra */
typedef struct nodo {
	int N;
	struct nodo *ult;
	struct nodo *prec;
} albero;

/* Legge un intero albero dal file f e restituisce il puntatore alla radice */
albero *leggialb( FILE *f ) {
	albero *a, *prev, *figlio;
	int i;

	a = (albero *)malloc( sizeof( albero ) );

	fscanf( f, "%d", &(a->N) );
	prev = NULL;
	for ( i = 0; i < a->N; i++ ) {
		figlio = leggialb( f );
		figlio->prec = prev;
		prev = figlio;
	}
	a->ult = prev;
	a->prec = NULL;
	return a;
}

/* Stampa sul file f l'albero puntato da a */
void stampaalb( FILE *f, albero *a ) {
	albero *figlio;

	fprintf( f, "%d ", a->N );
	figlio = a->ult;
	while ( figlio != NULL ) {
		stampaalb( f, figlio );
		figlio = figlio->prec;
	}
}

int main() {
	FILE *in, *out;
	albero *a;

	in = fopen( "input.txt", "r" );
	out = fopen( "output.txt", "w" );

	a = leggialb( in );
	fclose( in );
	
	stampaalb( out, a );
	fprintf( out, "\n" );
	fclose( out );
	return 0;
}

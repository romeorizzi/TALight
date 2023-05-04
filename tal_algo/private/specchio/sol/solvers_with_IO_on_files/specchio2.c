/*      

Specchio (selezioni nazionali 2002)

Copyright (C) 2002 Flavio Chierichetti

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
#include <stdlib.h>

typedef struct n {
  struct n **S;
  short N;
} node;

void get(node *n);
void print(node *n);

int main() {
  node Tree;

  get(&Tree);

  print(&Tree);

  return 0;
}

void get(node *n) {
  short i;

  scanf(" %d", &n->N);

  n->S = (node**) calloc (n->N, sizeof(node*));

  for ( i = 0 ; i < n->N ; i++ )
    get( n->S[i] = (node*) malloc (sizeof(node)) );
}

void print(node *n) {
  short i;

  printf(" %d", n->N);

  for ( i = n->N - 1 ; i >= 0 ; i-- )
    print( n->S[i] );
}

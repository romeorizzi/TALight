#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include <string.h>

#ifdef EVAL
#define NDEBUG
#endif

#define MAXF 1000
#define MAXN 1000000
#define MAXC 256
#define HASHSIZE 53
#define CACHESIZE 503

typedef struct colore_nodo_t {
  int colore;
  int val;
  struct colore_nodo_t *next;
} colore_nodo, *colore_lista;

typedef struct cache_nodo_t {
  int endpos;
  colore_lista val[HASHSIZE];
  struct cache_nodo_t *next;
} cache_nodo, *cache_lista;

typedef struct int_nodo_t {
  int val;
  struct int_nodo_t *next;
} int_nodo, *int_lista;

int strisce[MAXF];
int N;
cache_lista cache[MAXF][CACHESIZE];
int_lista pos[MAXC];

#define colore_hash(x) ( ( abs(x) ) % HASHSIZE )
#define cache_hash(x) ( ( abs(x) ) % CACHESIZE )

void leggi( void );
void risolvi( void );
int ottimizza( int start, int end, int segcol );
cache_nodo *cache_find( int start, int end  );
colore_nodo *colore_find( cache_lista lista, int segcol );
void cache_add( cache_nodo *cache_curr, int start, int end,
		int segcol, int val );

int main() {
#ifdef EVAL
  stdin = fopen("input.txt", "r");
  stdout = fopen("output.txt", "w");
#endif
  leggi();
  risolvi();
  return 0;
}

void leggi( void ) {
  int last = 0, prev = -1;
  int i;
  
  scanf( "%d", &N );
  assert( ( N > 0 ) && ( N <= MAXN ) );

  for( i = 0; i < N; ++i ) {
    int num;
    int_nodo *nodo;
    scanf( "%d", &num );
    if( num != prev ) {
      prev = num;
      strisce[last] = num;
      nodo = ( int_nodo * )malloc( sizeof( int_nodo ) );
      assert( nodo );
      nodo->next = pos[num];
      nodo->val = last;
      pos[num] = nodo;
      ++last;
    }
  }
  N = last;
}

void risolvi( void ) {
#ifndef NDEBUG
  //fprintf( stderr, "Risoluzione...\n" );
#endif
  printf( "%d\n", ottimizza( 0, N, -1 ) );
}

int ottimizza( int start, int end, int segcol ) {
  int col1;
  int ott, res;
  cache_nodo *cache_curr;
  colore_nodo *colore_curr;
  int_nodo *pos_curr;
  
  assert( ( start >= 0 ) && ( start <= N ) );
  assert( ( end >= 0 ) && ( end <= N ) );
  assert( start <= end );
  assert( ( segcol >= -1 ) && ( segcol < MAXC ) );

#ifndef NDEBUG
  //fprintf( stderr, "start = %d, end = %d, segcol = %d\n", 
	//   start, end, segcol );
#endif

  if( start == end )
    return 0;

  col1 = strisce[start];

  if( start == ( end-1 ) ) {
    if( col1 != segcol )
      return 1;
    else
      return 0;
  }

  cache_curr = cache_find( start, end );
  colore_curr = colore_find( cache_curr, segcol );
  if( colore_curr ) {
#ifndef NDEBUG
    //fprintf( stderr, "CACHE!\n" );
#endif
    return colore_curr->val;
  }

  if( col1 == segcol ) {
    ott = ottimizza( start + 1, end, segcol );
    cache_add( cache_curr, start, end, segcol, ott );
    return ott;
  }

#ifndef NDEBUG
  //fprintf( stderr, "Le prova tutte.\n" );
#endif
  ott = N;
  for( pos_curr = pos[col1]; ( pos_curr ) && ( pos_curr->val >= start );
       pos_curr = pos_curr->next ) {
    if( pos_curr->val >= end )
      continue;
    assert( ( pos_curr->val >= start ) && ( pos_curr->val < end ) );
    res = ottimizza( start, pos_curr->val + 1, col1 )
      + ottimizza( pos_curr->val + 1, end, segcol ) + 1;
    if( res < ott )
      ott = res;
  }

  cache_add( cache_curr, start, end, segcol, ott );
  return ott;
}

cache_nodo *cache_find( int start, int end  ) {
  cache_nodo *curr = cache[start][cache_hash(end)];
#ifndef NDEBUG
  //fprintf( stderr, "cache_find( %d, %d )\n", start, end );
#endif

  while( curr ) {
    if( curr->endpos == end )
      break;
    curr = curr->next;
  }
  return curr;
}

colore_nodo *colore_find( cache_lista lista, int segcol ) {
  colore_nodo *curr;
#ifndef NDEBUG
  //fprintf( stderr, "colore_find( %p, %d )\n", lista, segcol );
#endif
  if( !lista )
    return NULL;
  curr = lista->val[colore_hash(segcol)];
#ifndef NDEBUG
  //fprintf( stderr, "ricerca...\n" );
#endif
  while( curr ) {
    if( curr->colore == segcol )
      break;
    curr = curr->next;
  }
  return curr;
}

void cache_add( cache_nodo *cache_curr, int start, int end,
		int segcol, int val ) {
  colore_nodo *colore_new;
  int hash_val;
#ifndef NDEBUG
  //fprintf( stderr, "cache_add( %p, %d, %d, %d, %d )\n",
  //         cache_curr, start, end, segcol, val );
#endif
  if( !cache_curr ) {
#ifndef NDEBUG
    //fprintf( stderr, "cache_add(): [%d][%d] non esiste, creo.\n", start, end );
#endif
    cache_curr = ( cache_nodo * )malloc( sizeof( cache_nodo ) );
    assert( cache_curr );
    cache_curr->endpos = end;
    memset( cache_curr->val, 0, HASHSIZE * sizeof( colore_lista ) );

    hash_val = cache_hash(end);
    cache_curr->next = cache[start][hash_val];
    cache[start][hash_val] = cache_curr;
  }
  colore_new = ( colore_nodo * )malloc( sizeof( colore_nodo ) );
  assert( colore_new );
  colore_new->colore = segcol;
  colore_new->val = val;
  hash_val = colore_hash( segcol );
  colore_new->next = cache_curr->val[hash_val];
  cache_curr->val[hash_val] = colore_new;
}

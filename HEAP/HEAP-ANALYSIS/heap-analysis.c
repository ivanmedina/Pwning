#include <stdio.h>
#include <stdlib.h>

int main(){

	int *a =malloc(8); //fast chunk
	int *b = malloc (1020); //small chunk
	int *c = malloc(8); //fast chunk
	int *d = malloc(2046); //large chunk
	int *e = malloc(1020); //small chunk

	free (d); // small chunk 'd' will be inserted into unsorted bin
	free(c); //fast chunk 'c' will be inserterd in fast bin
	free(b); // large chunk 'b' will be inserted in unsorted bin 
	free(a); // fast bin 'a' will be inserted in fast bin
	malloc(8); //allocated one 32 bytes sized fast chunk
	malloc(8); // allocated one 32 bytes sizes fast chunk
	malloc(3000); //large chunk

	return 0;
} 
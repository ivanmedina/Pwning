#include <stdio.h>
 
int main(){
	unsigned int random;
	srand(time(NULL));
	random = rand();	// random value!
	printf("%x\n",random);
}

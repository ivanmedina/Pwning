#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char shellcode[] = "\xbb\x00\x00\x00\x00"
		   "\xb8\x01\x00\x00\x00"
		   "\xcd\x80";

/*char shellcode[] = "\xbb\x00\x00\x00\x00\xb8\x01\x00\x00\x00\xcd\x80";
*/

int main()
{   //printf("*********** SHELLCODE ***********\n");
    //printf("SHELLCODE S: %s \n",shellcode);
    //printf("SHELLCODE D: %d \n",(int)shellcode);
    //printf("SHELLCODE P: %p \n",shellcode);
    //printf("LEN: %d \n",strlen(shellcode));
    //printf("****************************\n\n");
    //printf("*********** *RET ***********\n");	
    int *ret;
    //printf("P: %p \n",ret);
    //printf("I: %d \n",*ret);
    //printf("****************************\n\n");
    //printf("***ret = (int *) &ret +2;***\n");
    ret = (int *) &ret +2;
    //printf("P: %p \n",ret);
    //printf("I: %d \n",*ret);

    //printf("****************************\n\n");
    //printf("***(*ret) = (int)shellcode;***\n");
    (*ret) = (int)shellcode;
    //printf("P: %p \n",ret);
    //printf("I: %d \n",*ret);
    //printf("****************************\n\n");
    //printf("SHELLCODE S: %s \n",shellcode);
    //printf("SHELLCODE D: %d \n",(int)shellcode);
    //printf("SHELLCODE P: %p \n",shellcode);
    //printf("LEN: %d n",strlen(shellcode));   
}

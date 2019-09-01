#include <stdio.h>

char shellcode[] = "\xbb\x00\x00\x00\x00"
		   "\xb8\x01\x00\x00\x00"
		   "\xcd\x80";

int main(int argc, char **argv)
{
    int (*funct)();
    funct = (int (*)()) shellcode;
    
    (int)(*funct)();
   
}


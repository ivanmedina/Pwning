#include <stdio.h>
#include <unistd.h>
int main()
{
char *happy[2];
happy[0]= "/bin/sh";
happy[1]=NULL;
execve(happy[0],happy,NULL);

}

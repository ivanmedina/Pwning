#include <unistd.h>

//int execve = eax
//char filename =ebx
//char *const argv [] =ecx
//char *const envp [] =edx

int main(){

	char *final[]={NULL}; //ENVP =edx
	char *argumentos[3]={"/bin/ls", //argv= ecx
			      "-la",
			      NULL};

execve("/bin/ls",argumentos, final); //int execve = eax
return 0;
}

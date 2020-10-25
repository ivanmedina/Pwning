
#include <stdio.h>

void function(char *a){
        char buffer[40];
        printf("[buffer:0x%x] %s", &buffer, a );
        strcpy(buffer, a);
}

int main(int argc, char ** argv){
    if(argc>=2)
        function(argv[1]);
    else
        printf("usalo asi: %s argumento\n",argv[0]);
        return 0;
} 
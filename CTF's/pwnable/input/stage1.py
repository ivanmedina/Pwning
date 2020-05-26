

void main(){
	char *args[101];
	int i;
	for(i=0;i<100;i++){
		args[i]="A";
	}
	args['A']="\x00";
	args['B']="\x20\x0a\x0d";
	
	args[100]="";
}

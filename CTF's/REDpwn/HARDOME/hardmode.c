#include <stdio.h>
#include <stdlib.h>

static void vuln(void)
{
	char buf[22];

	gets(buf);
	system("cat hardmode.c"); // wut
}

int main(void)
{
	setbuf(stdout, NULL);
	setbuf(stdin, NULL);
	setbuf(stderr, NULL);
	puts("Welcome to my fiendish little challenge");
	vuln();
}

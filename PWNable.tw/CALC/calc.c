
void calc(void)

{
  int myVariable;
  int in_GS_OFFSET;
  int pool;
  undefined4 stack100 [100];
  undefined buffer1024 [1024];
  int canary;
  
  canary = *(int *)(in_GS_OFFSET + 0x14);
  while( true ) {
    bzero(buffer1024,0x400);                        // fill zeros in buffer1024
    myVariable = get_expr((int)buffer1024,0x400);   // get expresion and save on myVariable 
    if (myVariable == 0) break;                     // break
    init_pool(&pool);                               // init_pool with pool address
    myVariable = parse_expr(buffer1024,&pool);      // afer get expresion, partse it
    if (myVariable != 0) {                          // only if myvar is != 0 ...   
      printf("%d\n",stack100[pool + -1]);           // printf from stack100 which appears be an stack of results
      fflush((FILE *)stdout);                       // only fflush
    }
  }
  if (canary == *(int *)(in_GS_OFFSET + 0x14)) {
    return;
  }
    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


undefined4 parse_expr(void *paramBF1024,int *param_2)                           //(buffer1024,&pool)
{
  int iterator;                                                                
  char *mCpChr;
  int myChar;
  undefined4 returnedVar;
  size_t nBytes;
  int in_GS_OFFSET;
  void *buffer1024;
  int contador;
  int pointerArray;
  char arrayExpr [100];
  int canary;
  
  canary = *(int *)(in_GS_OFFSET + 0x14);
  buffer1024 = paramBF1024;
  pointerArray = 0;
  bzero(arrayExpr,100);
  contador = 0;

  do {
    if (9 < (int)*(char *)((int)paramBF1024 + contador) - 0x30U) {              // if ( (int(actualChar) - 48) > 9 ) check char is allowed

      nBytes = (int)paramBF1024 + (contador - (int)buffer1024);                 
      mCpChr = (char *)malloc(nBytes + 1);
      memcpy(mCpChr,buffer1024,nBytes);
      mCpChr[nBytes] = '\0';
      myChar = strcmp(mCpChr,"0");                                              // copy byte by byte to use it
                                                                                
      if (myChar == 0) {                                                       
        puts("prevent division by zero");                                       
        fflush((FILE *)stdout);
        returnedVar = 0;
        goto LAB_0804935f;
      }                                                                        // no zeros and jumpt to check canary

      myChar = atoi(mCpChr);
      if (0 < myChar) {
        iterator = *param_2;
        *param_2 = iterator + 1;
        param_2[iterator + 1] = myChar;                                         
      }                                                                         // change element to asci code 

      if ((*(char *)((int)paramBF1024 + contador) != '\0') &&
         (9 < (int)*(char *)((int)paramBF1024 + contador + 1) - 0x30U)) {       
        puts("expression error!");
        fflush((FILE *)stdout);
        returnedVar = 0;
        goto LAB_0804935f;
      }                                                                         // review if is allowed char of not zero

      buffer1024 = (void *)((int)paramBF1024 + contador + 1);                   // save next char to the actual

      if (arrayExpr[pointerArray] == '\0') {                                    // if actual char is 0:
        arrayExpr[pointerArray] = *(char *)((int)paramBF1024 + contador);       //      expr = char in buffer
      }                 


      else {
        switch(*(undefined *)((int)paramBF1024 + contador)) { // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        case 0x25:                                                                      // %
        case 0x2a:                                                                      // *
        case 0x2f:                                                                      // /

          if ((arrayExpr[pointerArray] == '+') || (arrayExpr[pointerArray] == '-')) {   // if expr = + or expre = -:
            arrayExpr[pointerArray + 1] = *(char *)((int)paramBF1024 + contador);       //      nextExpr = actual char
            pointerArray = pointerArray + 1;                                            //      pointerArray ++
          }                                                                             //

          else {                                                                        //
            eval(param_2,arrayExpr[pointerArray]);                                      //  eval(param2, actualChar)
            arrayExpr[pointerArray] = *(char *)((int)paramBF1024 + contador);           //  current expr = current char
          }                                                                             //

          break;

        default:
          eval(param_2,arrayExpr[pointerArray]);                                        //  eval(param2, actualChar)
          pointerArray = pointerArray + -1;                                             //  pointerArray --
          break; 

        case 0x2b:                                                                      //  +
        case 0x2d:                                                                      //  -

          eval(param_2,arrayExpr[pointerArray]);                                        //  eval(param2, actualChar)
          arrayExpr[pointerArray] = *(char *)((int)paramBF1024 + contador);             //  
        } // switch <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      }

      if (*(char *)((int)paramBF1024 + contador) == '\0') {     // <<<<<<<<<<<<<< ya llegamos a un cero
        while (-1 < pointerArray) {                             // if char == 0:                  
          eval(param_2,arrayExpr[pointerArray]);                //      while (pointer > -1)    
          pointerArray = pointerArray + -1;                     //          eval(expr, current arrayExp[state])
        }                                                       //          pointerArray --
        returnedVar = 1;                                        // <<<<<<<<<<<<<<


        LAB_0804935f:                                           // canary check
        if (canary != *(int *)(in_GS_OFFSET + 0x14)) {          //
            /* WARNING: Subroutine does not return */           //  canary broken
          __stack_chk_fail();                                   //
        }


        return returnedVar;
      }
    } // main if
    contador = contador + 1;
  } while( true );
}


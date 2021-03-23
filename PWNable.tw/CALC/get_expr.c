
int get_expr(int param_1,int param_2)                          // (buffer1024, 1024)

{
  ssize_t sizeExpr;
  char myExpresion;
  int contador;
  
  contador = 0;
  while (contador < param_2) {
    sizeExpr = read(0,&myExpresion,1);                          // read my expresion and save in myExpresion and return size in sizeExpr
    if ((sizeExpr == -1) || (myExpresion == '\n')) break;       // if sizeExpr equals -1 oe myExpresion to '\n': break
        if ((((myExpresion == '+') || (((myExpresion == '-' ||  // if my Expresion is + or -
            myExpresion == '*')) || (myExpresion == '/')))) ||  // or * or /
            (myExpresion == '%')) ||                            // or %
            (('/' < myExpresion && (myExpresion < ':')))) {     // or an number 
                *(char *)(contador + param_1) = myExpresion;    // asign to myExpresion next char 
                contador = contador + 1;                        // increment contador in 1
        }
  } //end while
  *(undefined *)(param_1 + contador) = 0;                       // set 0 to end of param1 to end
  return contador;
}
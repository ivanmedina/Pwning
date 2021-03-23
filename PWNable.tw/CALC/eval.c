void eval(int *param_1,char param_2)                                            //param2, arrayexpr
{
  if (param_2 == '+') {                                                         
    param_1[*param_1 + -1] = param_1[*param_1 + -1] + param_1[*param_1];
  }
  else {
    if (param_2 < ',') {
      if (param_2 == '*') {
        param_1[*param_1 + -1] = param_1[*param_1 + -1] * param_1[*param_1];
      }
    }
    else {
      if (param_2 == '-') {
        param_1[*param_1 + -1] = param_1[*param_1 + -1] - param_1[*param_1];
      }
      else {
        if (param_2 == '/') {
          param_1[*param_1 + -1] = param_1[*param_1 + -1] / param_1[*param_1];
        }
      }
    }
  }
  *param_1 = *param_1 + -1;
  return;
}


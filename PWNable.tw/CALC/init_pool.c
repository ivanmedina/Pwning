void init_pool(undefined4 *param_1)

{
  int local_8;
  
  *param_1 = 0;
  local_8 = 0;          
  while (local_8 < 100) {
    param_1[local_8 + 1] = 0;           // only made 0's in our address, from it starts to 100 bytes foreward
    local_8 = local_8 + 1;
  }
  return;
}

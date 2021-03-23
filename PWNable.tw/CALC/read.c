
ssize_t read(int __fd,void *__buf,size_t __nbytes)

{
  uint aPointer;
  int in_GS_OFFSET;
  
  if (*(int *)(in_GS_OFFSET + 0xc) == 0) {          // if my pointed int + 12 == 0
    aPointer = (*(code *)_dl_sysinfo)();            // aPOinter = dl_sysinfo() and returned as code
    if (aPointer < 0xfffff001) {                    // aPointer is less that 0xfffff001?
      return aPointer;                              // ok, return the pointer
    }
  }
  else {                                            // no? ...
    __libc_enable_asynccancel();
    aPointer = (*(code *)_dl_sysinfo)();            // okey, one more time
    __libc_disable_asynccancel();               
    if (aPointer < 0xfffff001) {                    // now, is less?
      return aPointer;                              // okey, return it
    }
  }
  *(int *)(in_GS_OFFSET + -0x18) = -aPointer;       // error
  return -1;                                        // error
}

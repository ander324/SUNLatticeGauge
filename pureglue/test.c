#include "clcomplex.h"
#include <CL/cl.h>
#include <stdio.h>


int main(){
  
  clcomplex x = Clcomplex(2.0,3.5);

  clcomplex y = Conjg(x);
  
  printf("x = %f + i%f\n", x.v2[0], x.v2[1]);
  printf("y = %f + i%f\n", y.v2[0], y.v2[1]);


  return 0;
}

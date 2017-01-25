#include "openclcomplex.h"
#include "clsun.h"
#include <clRNG/mrg31k3p.clh>



// Creates a bunch of random matrices along with their inverses
__kernel void CreateRandomSUN( __global clrngMrg31k3pHostStream* streams,
			       __global matrix* RandSUN)
{

  int gid = get_global_id(0);
  clrngMrg31k3pStream private_stream_d;   // This is not a pointer!	
  clrngMrg31k3pCopyOverStreamsFromGlobal(1, &private_stream_d, &streams[gid]);

  matrix A;
  double tmp;
  for(int i=0; i<3; i++){
    tmp = clrngMrg31k3pRandomU01(&private_stream_d)*eps*2.0 - eps;
    A.a[i][i] = cdouble_new(1.0,  tmp);
  }

  for(int i=0; i<Nc; i++)
    for(int j=i+1; j<Nc; j++){
      tmp = clrngMrg31k3pRandomU01(&private_stream_d)*eps*2.0 - eps;
      A.a[i][j] = cdouble_new(0.0, tmp);
      A.a[j][i] = cdouble_new(0.0, tmp);
    }

  A = reunitarize(A);

  RandSUN[gid] = A;
  RandSUN[gid+numRandSUN/2] = adjoint(A);

  /* printf("(%f %f) (%f %f)\n", determinant(A).x, determinant(A).y, determinant(adjoint(A)).x, determinant(adjoint(A)).y); */
  /* m_print(m_mul_na(A,A)); //check if it producing SUN(mats) */

  /* if(gid == 0){ */
  /*   printf("(%f %f) (%f %f)\n", determinant(A).x, determinant(A).y, determinant(adjoint(A)).x, determinant(adjoint(A)).y); */
  /*   m_print(m_mul_na(A,A)); //check if it producing SUN(mats) */
  /* } */

}



//Start the lattice from a cold start
__kernel void LatticeColdStart(__global matrix* gauge)
{
  int gid = get_global_id(0);

  gauge[gid] = m_ident();
}


//Update the gauge fields using the metropolis algorithm
// and the Wilson Action

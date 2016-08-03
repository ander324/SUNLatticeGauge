/**
Author: Peter Anderson
Date: 8-3-2016

**/

#ifndef CLSUN_H
#define CLSUN_H

#include "clcomplex.h"

const int Nc = 3;

typedef struct {
  clcomplex a[Nc*Nc];
} _matrixsun;

//returns 0 matrix
_matrixsun m_zero(){
  _matrixsun A;
  memset(A, 0, sizeof(_matrixsun));

  return A;
}

// returns identity
_matrixsun m_ident(){
  _matrixsun A;
  memset(A, 0, sizeof(_matrixsun));
  for(int i=0; i<Nc; i++){
    A.a[i + Nc*i] = Clcomplex(1.0,0.0);
  }
  return A;
}

//A+B -> C
_matrixsun m_add( _matrixsun A, _matrixsun B){
  _matrixsun C;

  for(int r=0; r<Nc; r++)
    for(int c=0; c<Nc; c++)
      C.a[r*Nc + c] = A.a[r*Nc + c] + B.a[r*Nc + c];

  return C;
}

//A-B -> C
_matrixsun m_sub( _matrixsun A, _matrixsun B){
  _matrixsun C;

  for(int r=0; r<Nc; r++)
    for(int c=0; c<Nc; c++)
      C.a[r*Nc + c] = A.a[r*Nc + c] - B.a[r*Nc + c];

  return C;
}



// A*B -> C
_matrixsun m_mul_nn( _matrixsun A, _matrixsun B){
  _matrixsun C;
  
  for(int row=0; row<Nc; row++)
    for(int col=0; col<Nc; col++)
      for(int k=0; k<Nc; k++)
	C.a[row*Nc + col] = A.a[row*Nc + k]*B.a[k*Nc + col];

  return C;
}


// returns A^dagger
_matrixsun adjoint( _matrixsun A){
  _matrixsun B;
  
  for(int i=0; i<Nc; i++)
    for(int j=0; j<Nc; j++)
      B.a[j*Nc+i] = Conj(A[i*Nc+j]);

  return B;
}

//returns trace
clcomplex trace(_matrixsun A){
  clcomplex tr = Clcomplex(0.0, 0.0);

  for(int i=0; i<Nc; i++)
    tr = Cadd(tr, A.a[i*Nc + i]);

  return tr;
}

#endif

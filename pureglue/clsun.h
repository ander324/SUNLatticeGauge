/**
Author: Peter Anderson
Date: 8-3-2016

**/

#ifndef CLSUN_H
#define CLSUN_H

#include "openclcomplex.h"
#define _matrixsun matrix

#define Nc 3

typedef struct {
  cdouble_t a[Nc][Nc];
} _matrixsun;

//returns 0 matrix
_matrixsun m_zero(){
  _matrixsun A;
  for(int i=0; i<Nc; i++){
    for(int j=0; j<Nc; j++){
      A.a[i][j] = cdouble_new(0.0,0.0);
    }
  }


  return A;
}

// returns identity
_matrixsun m_ident(){
  _matrixsun A;
  A = m_zero();
  for(int i=0; i<Nc; i++){
    A.a[i][i] = cdouble_new(1.0,0.0);
  }
  return A;
}

//A+B -> C
_matrixsun m_add( _matrixsun A, _matrixsun B){
  _matrixsun C;

  for(int r=0; r<Nc; r++)
    for(int c=0; c<Nc; c++)
      C.a[r][c] = cdouble_add(A.a[r][c] , B.a[r][c]);

  return C;
}

//A-B -> C
_matrixsun m_sub( _matrixsun A, _matrixsun B){
  _matrixsun C;

  for(int r=0; r<Nc; r++)
    for(int c=0; c<Nc; c++)
      C.a[r][c] = cdouble_sub(A.a[r][c] ,B.a[r][c]);

  return C;
}



// A*B -> C
_matrixsun m_mul_nn( _matrixsun A, _matrixsun B){
  _matrixsun C;
  cdouble_t tmp;
  for(int row=0; row<Nc; row++)
    for(int col=0; col<Nc; col++){
      tmp = cdouble_new(0.0,0.0);
      for(int k=0; k<Nc; k++)
	tmp = cdouble_add(tmp,cdouble_mul(A.a[row][k],B.a[k][col]));
      C.a[row][col] = tmp;
    }
  return C;
}

// a*A -> B
_matrixsun m_mul_real( double a, _matrixsun A){
  _matrixsun B;
  
  for(int row=0; row<Nc; row++)
    for(int col=0; col<Nc; col++)
      B.a[row][col] = cdouble_rmul(a, A.a[row][col]);

  return B;
}




// returns A^dagger
_matrixsun adjoint( _matrixsun A){
  _matrixsun B;
  
  for(int i=0; i<Nc; i++)
    for(int j=0; j<Nc; j++)
      B.a[j][i] = cdouble_conj(A.a[i][j]);

  return B;
}

//returns trace
cdouble_t trace(_matrixsun A){
  cdouble_t tr = cdouble_new(0.0, 0.0);

  for(int i=0; i<Nc; i++)
    tr = cdouble_add(tr, A.a[i][i]);

  return tr;
}

//returns real{trace(A*B)}
/* double realtrace(_matrixsun A, _matrixsun B){ */
/*   double sum = 0.0; */

/*   //not yet implemented */
/*   printf("Error, realtrace is not implemented as of yet\n"); */
/*   exit(-1); */

/*   return sum; */
/* } */

//print sun matrices
void m_print(_matrixsun A){
  printf("%s","\n");
  for(int r=0; r<Nc; r++){
    for( int c=0; c<Nc; c++){
      printf("(%f, %f)\t",A.a[r][c].x, A.a[r][c].y);
    }
      printf("%s","\n");
    printf("\n");
  }
    printf("%s","\n");
  printf("\n");
}

//should be equal to 1, but need to calculate for
cdouble_t determinant(_matrixsun A){
  _matrixsun B;
  cdouble_t res = cdouble_new(0.0,0.0);

  //copy matrix into B
  for(int i=0; i<Nc; i++)
    for(int j=0; j<Nc; j++)
      B.a[i][j] = A.a[i][j];

  for(int j = 0; j < Nc; j++){
    for(int i = 0; i <= j; i++){
      res = B.a[i][j];
      for(int c = 0; c < i; c++)
	res = cdouble_sub(res , cdouble_mul(B.a[i][c], B.a[c][j]));
			    
      B.a[i][j] = res;
    }
		
    for(int i = (j+1); i < Nc; i++){
      res = B.a[i][j];
      for(int c = 0; c < j; c++)
	res =cdouble_sub(res ,cdouble_mul( B.a[i][c] , B.a[c][j]));
      B.a[i][j] = cdouble_divide(res,B.a[j][j]);
    }
  }

  res = cdouble_mul(B.a[0][0],B.a[1][1]);
  for(int c = 2; c < Nc; c++)
    res =cdouble_mul(res , B.a[c][c]);

  return res;
}

//reunitarize the matrices using the Gram-Schmidt Process

_matrixsun reunitarize(_matrixsun A){
  cdouble_t tmp, dot_uv;
  double dot_uu;
  _matrixsun B = A;

  for(int i=0; i<Nc; i++){
    //normalize vector_i
    tmp = cdouble_new(0.0,0.0);
    for(int k=0; k<Nc; k++)
      tmp = cdouble_add(tmp ,cdouble_mul(cdouble_conj(B.a[i][k]),B.a[i][k]));
    dot_uu = sqrt(tmp.real);
    for(int k=0; k<Nc; k++)
      B.a[i][k] = cdouble_divider(B.a[i][k], dot_uu);

    //subtract the project of vec_i onto vec_j from vec_j
    for(int j=i+1; j<Nc; j++){
      //calculate dot product
      dot_uv = cdouble_new(0.0,0.0);
      for(int k=0; k<Nc; k++)
	dot_uv = cdouble_add(dot_uv, cdouble_mul(cdouble_conj(B.a[i][k]),B.a[j][k]));

      //subtrace off projection
      for(int k=0; k<Nc; k++)
	B.a[j][k] = cdouble_sub(B.a[j][k], cdouble_mul(B.a[i][k], dot_uv));
    }
  }

  //Inorder to have det A = 1 we need to divide out the phase
  cdouble_t t2 = determinant(B);
  double th = atan2( t2.x, t2.y);
  t2 = cdouble_new(cos(th), -sin(th));

  for(int c=0; c<Nc; c++)
    B.a[Nc-1][c] = cdouble_mul(B.a[Nc-1][c],t2);

  return B;
}




#endif

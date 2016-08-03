/*
  Author: Peter Anderson
  Date: 7-28-2016
  
  
*/


#ifndef CLCOMPLEX_H
#define CLCOMPLEX_H


typedef struct {double x; double y;} _clzcomplex;

#define clcomplex _clzcomplex

_clzcomplex Clcomplex(double re, double im){
  _clzcomplex c;
  c.x = re;
  c.y = im;
  return c;
}

double Real(_clzcomplex a){
  return a.x;
}

double Imag(_clzcomplex a){
  return a.y;
}

//a+b -> c
_clzcomplex Cadd(_clzcomplex a, _clzcomplex b){
  _clzcomplex c;
  c.x = a.x + b.x;
  c.y = a.y + b.y;

  return c;
}

//a-b -> c
_clzcomplex Csub(_clzcomplex a, _clzcomplex b){
  _clzcomplex c;
  c.x = a.x - b.x;
  c.y = a.y - b.y;

  return c;
}

//a*b -> c
 _clzcomplex Cmul( _clzcomplex a, _clzcomplex b){
  _clzcomplex c;
  c.x = a.x*b.x - a.y*b.y;
  c.y = a.x*b.y + a.y*b.x;
  
  return c;
}

//alpha*b -> c
_clzcomplex RCmul( double alpha, _clzcomplex b){
  _clzcomplex c;
  c.x = alpha*b.x;
  c.y = alpha*b.y;

  return c;
}

// a/b -> c
_clzcomplex Cdiv(_clzcomplex a, _clzcomplex b){
  _clzcomplex c;
  double r,den;
  
  if (fabs(b.x) >= fabs(b.y)) {
    r=b.y/b.x;
    den=b.x+r*b.y;
    c.x=(a.x+r*a.y)/den;
    c.y=(a.y-r*a.x)/den;
  } else {
    r=b.x/b.y;
    den=b.y+r*b.x;
    c.x=(a.x*r+a.y)/den;
    c.y=(a.y*r-a.x)/den;
  }
  return c;
}

double Cabs(_clzcomplex z){
  double x,y,ans,temp;
  x=fabs(z.x);
  y=fabs(z.y);
  if (x == 0.0)
    ans=y;
  else if (y == 0.0)
    ans=x;
  else if (x > y) {
    temp=y/x;
    ans=x*sqrt(1.0+temp*temp);
  } else {
    temp=x/y;
    ans=y*sqrt(1.0+temp*temp);
  }
  return ans;
}

// a-> |a|^2
double Cmod(_clzcomplex a){
  return a.x*a.x + a.y*a.y;
}


_clzcomplex Csqrt(_clzcomplex z){
  _clzcomplex c;
  double x,y,w,r;
  if ((z.x == 0.0) && (z.y == 0.0)) {
    c.x=0.0;
    c.y=0.0;
    return c;
  } else {
    x=fabs(z.x);
    y=fabs(z.y);
  } if (x >= y) {
    r=y/x;
    w=sqrt(x)*sqrt(0.5*(1.0+sqrt(1.0+r*r) )) ;
  } else {
    r=x/y;
    w=sqrt(y)*sqrt(0.5*(r+sqrt(1.0+r*r)));
  }
  if (z.x >= 0.0) {
    c.x=w;
    c.y=z.y/(2.0*w);
  } else {
    c.y=(z.y >= 0) ? w : -w;
    c.x=z.y/(2.0*c.y) ;
  }
  return c;
}




// a -> b^*
_clzcomplex Conj(_clzcomplex a){
  _clzcomplex c;
  c.x = a.x;
  c.y = -a.y; 
  return c;
}


#endif

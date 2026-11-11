/* Minimal scalar BLAS/platform support for the pinned LAPACK routines.
   Generated test harness, not a substitute for the complete upstream library. */
#include <float.h>
#include <math.h>
#include <stdlib.h>
void xerbla_(char *s,int *n,int len){(void)s;(void)n;(void)len;abort();}
double dlamch_(char *s){(void)s;return DBL_MIN;}
int idamax_(int *n,double *x,int *inc){int k=0;for(int i=1;i<*n;i++)if(fabs(x[i*(*inc)])>fabs(x[k*(*inc)]))k=i;return k+1;}
void dscal_(int *n,double *a,double *x,int *inc){for(int i=0;i<*n;i++)x[i*(*inc)]*=*a;}
void dswap_(int *n,double *x,int *ix,double *y,int *iy){for(int i=0;i<*n;i++){double t=x[i*(*ix)];x[i*(*ix)]=y[i*(*iy)];y[i*(*iy)]=t;}}
void dger_(int *m,int *n,double *alpha,double *x,int *ix,double *y,int *iy,double *a,int *lda){for(int j=0;j<*n;j++){double t=*alpha*y[j*(*iy)];for(int i=0;i<*m;i++)a[i+j*(*lda)]+=x[i*(*ix)]*t;}}

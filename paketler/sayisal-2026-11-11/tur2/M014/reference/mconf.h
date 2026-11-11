/* Portable platform shim; the upstream C algorithm bodies are unchanged. */
#include <math.h>
#define NPY_NAN NAN
#define DOMAIN 1
#define UNDERFLOW 4
double igam(double,double);
double igamc(double,double);
double lgam(double);
double beta(double,double);
double lbeta(double,double);
int mtherr(char *,int);

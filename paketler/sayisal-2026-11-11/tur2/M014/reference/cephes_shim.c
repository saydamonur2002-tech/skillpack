#include <math.h>
double MACHEP=1.11022302462515654042E-16,MAXLOG=7.09782712893383996732E2,MINLOG=-7.451332191019412076235E2;
double lgam(double a){return lgamma(a);}
double lbeta(double a,double b){return lgamma(a)+lgamma(b)-lgamma(a+b);}
double beta(double a,double b){return exp(lbeta(a,b));}
int mtherr(char *s,int code){(void)s;(void)code;return 0;}

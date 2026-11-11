static void t_cal2jd(int *status)
/*
**  - - - - - - - - -
**   t _ c a l 2 j d
**  - - - - - - - - -
**
**  Test eraCal2jd function.
**
**  Returned:
**     status    int         FALSE = success, TRUE = fail
**
**  Called:  eraCal2jd, vvd, viv
**
**  This revision:  2013 August 7
*/
{
   int j;
   double djm0, djm;


   j = eraCal2jd(2003, 06, 01, &djm0, &djm);

   vvd(djm0, 2400000.5, 0.0, "eraCal2jd", "djm0", status);
   vvd(djm,    52791.0, 0.0, "eraCal2jd", "djm", status);

   viv(j, 0, "eraCal2jd", "j", status);

}
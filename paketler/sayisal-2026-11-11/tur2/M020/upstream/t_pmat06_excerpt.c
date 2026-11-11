static void t_pmat06(int *status)
/*
**  - - - - - - - - -
**   t _ p m a t 0 6
**  - - - - - - - - -
**
**  Test eraPmat06 function.
**
**  Returned:
**     status    int         FALSE = success, TRUE = fail
**
**  Called:  eraPmat06, vvd
**
**  This revision:  2013 August 7
*/
{
   double rbp[3][3];


   eraPmat06(2400000.5, 50123.9999, rbp);

   vvd(rbp[0][0], 0.9999995505176007047, 1e-12,
       "eraPmat06", "11", status);
   vvd(rbp[0][1], 0.8695404617348208406e-3, 1e-14,
       "eraPmat06", "12", status);
   vvd(rbp[0][2], 0.3779735201865589104e-3, 1e-14,
       "eraPmat06", "13", status);

   vvd(rbp[1][0], -0.8695404723772031414e-3, 1e-14,
       "eraPmat06", "21", status);
   vvd(rbp[1][1], 0.9999996219496027161, 1e-12,
       "eraPmat06", "22", status);
   vvd(rbp[1][2], -0.1361752497080270143e-6, 1e-14,
       "eraPmat06", "23", status);

   vvd(rbp[2][0], -0.3779734957034089490e-3, 1e-14,
       "eraPmat06", "31", status);
   vvd(rbp[2][1], -0.1924880847894457113e-6, 1e-14,
       "eraPmat06", "32", status);
   vvd(rbp[2][2], 0.9999999285679971958, 1e-12,
       "eraPmat06", "33", status);

}
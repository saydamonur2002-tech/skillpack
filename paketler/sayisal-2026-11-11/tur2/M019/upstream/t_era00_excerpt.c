static void t_era00(int *status)
/*
**  - - - - - - - -
**   t _ e r a 0 0
**  - - - - - - - -
**
**  Test eraEra00 function.
**
**  Returned:
**     status    int         FALSE = success, TRUE = fail
**
**  Called:  eraEra00, vvd
**
**  This revision:  2013 August 7
*/
{
   double era00;


   era00 = eraEra00(2400000.5, 54388.0);

   vvd(era00, 0.4022837240028158102, 1e-12, "eraEra00", "", status);

}
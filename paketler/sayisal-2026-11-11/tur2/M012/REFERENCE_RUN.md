# Reference verification scope

The upstream quadpack test asserts sin integral=2 and the n=2,z=1.8 Bessel integral=0.30614353532540296487. Those are driver-level published fixtures, applied here to a smooth single panel with declared tolerances. Supplemental polynomial expectations are analytically integrated, not upstream literal gold.

The original Fortran routine was not compiled: no Fortran compiler was available and the system package-network attempt failed. No alternative authentication, network bypass or binary claim was used. Read the original source excerpt, then run the declared published/analytic references with `python -m pytest tests`. These are not a claim to have run the complete upstream test suite.

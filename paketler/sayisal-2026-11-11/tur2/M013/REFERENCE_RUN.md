# Reference verification scope

Primary upstream embedded test prints orbital examples but supplies no asserted golden trajectory. State fixtures instead come from the explicitly pinned BSD SciPy test_ivp.py fun_linear/sol_linear analytic solution, a different upstream validation source. Scalar exponential, zero and constant-derivative cases are supplementary analytic checks. Neither RKF78 raw terr nor a full adaptive controller has an independent native-Fortran reference here.

The original Fortran routine was not compiled: no Fortran compiler was available and the system package-network attempt failed. No alternative authentication, network bypass or binary claim was used. Read the original source excerpt, then run the declared published/analytic references with `python -m pytest tests`. These are not a claim to have run the complete upstream test suite.

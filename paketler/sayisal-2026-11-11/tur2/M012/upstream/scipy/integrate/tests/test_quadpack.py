        legacy_sigs = [sin_2, sin_4]
        legacy_only_sigs = [sin_4]

        # LowLevelCallables work for new signatures
        for j, func in enumerate(all_sigs):
            callback = LowLevelCallable(func)
            if func in legacy_only_sigs:
                pytest.raises(ValueError, quad, callback, 0, pi)
            else:
                assert_allclose(quad(callback, 0, pi)[0], 2.0)

        # Plain ctypes items work only for legacy signatures
        for j, func in enumerate(legacy_sigs):
            if func in legacy_sigs:
                assert_allclose(quad(func, 0, pi)[0], 2.0)
            else:
                pytest.raises(ValueError, quad, func, 0, pi)


class TestMultivariateCtypesQuad:
    def setup_method(self):
        restype = ctypes.c_double
        argtypes = (ctypes.c_int, ctypes.c_double)
        for name in ['_multivariate_typical', '_multivariate_indefinite',
                     '_multivariate_sin']:
            func = get_clib_test_routine(name, restype, *argtypes)
            setattr(self, name, func)

    def test_typical(self):
        # 1) Typical function with two extra arguments:
        assert_quad(quad(self._multivariate_typical, 0, pi, (2, 1.8)),
                    0.30614353532540296487)

    def test_indefinite(self):
        # 2) Infinite integration limits --- Euler's constant
        assert_quad(quad(self._multivariate_indefinite, 0, np.inf),
                    0.577215664901532860606512)

    def test_threadsafety(self):
        # Ensure multivariate ctypes are threadsafe
        def threadsafety(y):
            return y + quad(self._multivariate_sin, 0, 1)[0]
        assert_quad(quad(threadsafety, 0, 1), 0.9596976941318602)


class TestQuad:
    def test_typical(self):
        # 1) Typical function with two extra arguments:
        def myfunc(x, n, z):       # Bessel function integrand
            return cos(n*x-z*sin(x))/pi
        assert_quad(quad(myfunc, 0, pi, (2, 1.8)), 0.30614353532540296487)

    def test_indefinite(self):
        # 2) Infinite integration limits --- Euler's constant
        def myfunc(x):           # Euler's constant integrand
            return -exp(-x)*log(x)
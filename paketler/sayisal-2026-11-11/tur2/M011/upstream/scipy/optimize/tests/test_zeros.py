class TestBracketMethods(TestScalarRootFinders):
    @pytest.mark.parametrize('method', bracket_methods)
    @pytest.mark.parametrize('function', tstutils_functions)
    def test_basic_root_scalar(self, method, function):
        # Tests bracketing root finders called via `root_scalar` on a small
        # set of simple problems, each of which has a root at `x=1`. Checks for
        # converged status and that the root was found.
        a, b = .5, sqrt(3)

        r = root_scalar(function, method=method.__name__, bracket=[a, b], x0=a,
                        xtol=self.xtol, rtol=self.rtol)
        assert r.converged
        assert_allclose(r.root, 1.0, atol=self.xtol, rtol=self.rtol)
        assert r.method == method.__name__

    @pytest.mark.parametrize('method', bracket_methods)
    @pytest.mark.parametrize('function', tstutils_functions)
    def test_basic_individual(self, method, function):
        # Tests individual bracketing root finders on a small set of simple
        # problems, each of which has a root at `x=1`. Checks for converged
        # status and that the root was found.
        a, b = .5, sqrt(3)
        root, r = method(function, a, b, xtol=self.xtol, rtol=self.rtol,
                         full_output=True)

        assert r.converged
        assert_allclose(root, 1.0, atol=self.xtol, rtol=self.rtol)
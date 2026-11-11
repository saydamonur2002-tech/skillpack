        assert_equal(cephes.beta(1,1),1.0)
        assert_allclose(cephes.beta(-100.3, 1e-200), cephes.gamma(1e-200))
        assert_allclose(cephes.beta(0.0342, 171), 24.070498359873497,
                        rtol=1e-13, atol=0)

    def test_betainc(self):
        assert_equal(cephes.betainc(1,1,1),1.0)
        assert_allclose(cephes.betainc(0.0342, 171, 1e-10), 0.55269916901806648)

    def test_betaln(self):
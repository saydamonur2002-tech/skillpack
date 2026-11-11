# Source audit

Upstream: https://github.com/PyWavelets/pywt

Pinned commit: `7b9e57ed639e7f87490a5bcb31f7b6c088d19031`

Observed stars: 2413; repository created 2013. This is repository age, not proof of 50-year-old source code.

License: MIT. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
Copyright (c) 2012-     The PyWavelets Developers <https://github.com/PyWavelets/pywt>

## Faithfulness and changes

Ports the two-tap db1 analysis/reconstruction equations using sqrt(0.5). For even lengths these do not require boundary extension. The upstream complex fixture is explicitly adapted to real components; this is not claimed to be an unchanged real upstream fixture.

## Reference values

pywt/tests/test_dwt_idwt.py:88-103 has explicit complex Haar partial-reconstruction arrays. Fixtures here take their real components, justified by the real-valued linear Haar filter. The original complex fixture is preserved. Coefficients are db1_ in wavelets_coeffs.template.h.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [pywt/_extensions/c/wavelets_coeffs.template.h](https://github.com/PyWavelets/pywt/blob/7b9e57ed639e7f87490a5bcb31f7b6c088d19031/pywt/_extensions/c/wavelets_coeffs.template.h) — SHA-256 `0372cc7ca464d250c7d4cea462885827ec54074e4c8c9a00343eb35a5432bef2` (original lines 1-38 only).
- [pywt/_extensions/c/wt.template.c](https://github.com/PyWavelets/pywt/blob/7b9e57ed639e7f87490a5bcb31f7b6c088d19031/pywt/_extensions/c/wt.template.c) — SHA-256 `ad097db2205dfd57cba9576b28cb14b1620240c7c20cc8cdc511dc6d742b284f` (complete original file).
- [pywt/tests/test_dwt_idwt.py](https://github.com/PyWavelets/pywt/blob/7b9e57ed639e7f87490a5bcb31f7b6c088d19031/pywt/tests/test_dwt_idwt.py) — SHA-256 `323f35f5c4db8bfed6d78495d1d5cf24d42478097e47e23291fdd96be339660b` (complete original file).

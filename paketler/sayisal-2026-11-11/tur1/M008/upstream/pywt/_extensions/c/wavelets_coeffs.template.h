#include "templating.h"

#ifndef TYPE
#error TYPE must be defined here.
#else

/*
 * Filters coefficients for selected wavelets
 *
 * Daubechies:   db1   - db20
 * Symlets:      sym2  - sym20
 * Coiflets:     coif1 - coif5
 * Biorthogonal: bior 1.1, 1.3, 1.5,
 *                    2.2, 2.4, 2.6, 2.8,
 *                    3.1, 3.3, 3.5, 3.7, 3.9,
 *                    4.4, 5.5, 6.8
 * Discrete Meyer wavelet *approximation*: dmey
 *
 * Coefficients for Daubechies wavelets 1-38
 * -----------------------------------------
 * 2000.08.10 - Some more info added.
 * (http://www.musicdsp.org/files/daub.h)
 *
 * Computed by Kazuo Hatano, Aichi Institute of Technology.
 * ftp://phase.etl.go.jp/pub/phase/wavelet/index.html
 *
 * Compiled and verified by Olli Niemitalo.
 *
 * Coefficients for Coiflets wavelets 1-17
 * -----------------------------------------
 * Computed by Kazuo Hatano, Aichi Institute of Technology.
 * http://repository.kulib.kyoto-u.ac.jp/dspace/handle/2433/60181
 */

static const TYPE CAT(db1_, TYPE)[2] = {
   7.071067811865475244008443621048490392848359376884740365883398e-01,
 7.071067811865475244008443621048490392848359376884740365883398e-01
};

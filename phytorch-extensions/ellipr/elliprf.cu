#include "ellipr.cuh"


DEFINE_COMPLEX_FUNCTION(elliprf, (x, y, z)) {
    ELLIPR_CHECK_xyz

    if (y==z) return elliprc<scalar_t>(x, y);
    if (x==z) return elliprc<scalar_t>(y, x);
    if (x==y) return elliprc<scalar_t>(z, x);

    auto Am = (x + y + z) / ltrl(3.);
    ELLIPR_HEADER(3.)

    while (pow4 * Q > abs(Am)) {
        ELLIPR_STEP
        ELLIPR_UPDATE(zm + lm)
    }

    ELLIPR_XY
    auto Z = - (X + Y),
            E2 = X*Y - Z*Z,
            E3 = X*Y*Z;

    return (ltrl(1.) - E2 / ltrl(10.) + E2 * E2 / ltrl(14.) + E3 / ltrl(24.) - ltrl(3. / 44.) * E2 * E3) / sqrt(Am);
}

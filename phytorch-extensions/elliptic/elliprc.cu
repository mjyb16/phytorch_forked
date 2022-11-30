#include "elliptic.cuh"


DEFINE_COMPLEX_FUNCTION(elliprc, (x, y)) {
    if (isinf(x) or isinf(y)) return ltrl(1) / (x*y);
    if (not y) return numeric_limits<T>::infinity();
    if (not x) return ltrl(M_PI_2) / sqrt(y);

    // principal value
    if (not y.imag() and y.real() < 0)
        return sqrt(x / (x-y)) * elliprc<scalar_t>(x-y, -y);

    auto Am = (x + y + y) / ltrl(3), xm = x, ym = y, A0 = Am;
    auto Q = pow(3*EPS, -1./6.) * abs(A0 - x);
    scalar_t pow4 = 1.;

    while (pow4 * Q > abs(Am)) {
        auto lm = 2*sqrt(xm)*sqrt(ym) + ym;
        xm = (xm + lm) / ltrl(4); ym = (ym + lm) / ltrl(4);
        Am = (Am + lm) / ltrl(4); pow4 /= 4.;
    }

    auto s = (y - A0) * pow4 / Am;
    return (
        1
        + s*s * ltrl(3./10.)
        + s*s*s / ltrl(7)
        + s*s*s*s * ltrl(3./8.)
        + s*s*s*s*s * ltrl(9./22.)
        + s*s*s*s*s*s * ltrl(159./208.)
        + s*s*s*s*s*s*s * ltrl(9./8.)
    ) / sqrt(Am);

    // TODO: handle x=y in elliprc better
    if (abs(sqrt(1-x/y)) < max((scalar_t) 1e-3, 100*sqrt(numeric_limits<scalar_t>::epsilon())))
        return (ltrl(7./6.) - (x/y) / ltrl(6)) / sqrt(y);

    // Formally, have to T(1), but this error most times "cancels" with wrong
    // continuity of acos...
    return acos(sqrt(x) / sqrt(y)) / (sqrt(1-x/y) * sqrt(y));

    auto v = sqrt(x) / sqrt(y), _1vv = T(1) - v*v, s1vv = sqrt(_1vv), lv = v*TIMAG + s1vv;
    auto ac = ltrl(M_PI_2) + TIMAG*log(lv);
    auto _1xy = T(1)-x/y, s1xy = sqrt(_1xy);
    //
    // // printf("v=%.20e+i%.20e, v^2=%.20e+i%.20e, 1-v^2=%.20e+i%.20e\n",
    // //        v.real(), v.imag(),
    // //        (v*v).real(), (v*v).imag(),
    // //        _1vv.real(), _1vv.imag());
    // // printf("sqrt(%.4e+i%.4e)=%.4e+i%.4e\n", (T(1)-v*v).real(), (1-v*v).imag(), s1vv.real(), s1vv.imag());
    // // printf("log(%.4e+i%.4e) = %.4e+i%.4e\n", lv.real(), lv.imag(), log(lv).real(), log(lv).imag());
    // // printf("acos(%.4e+i%.4e) = %.4e+i%.4e\n", v.real(), v.imag(), ac.real(), ac.imag());
    // // printf("sqrt(%.4e+i%.4e) = %.4e+i%.4e\n", _1xy.real(), _1xy.imag(), s1xy.real(), s1xy.imag());
    //
    return ac / (s1xy * sqrt(y));
}

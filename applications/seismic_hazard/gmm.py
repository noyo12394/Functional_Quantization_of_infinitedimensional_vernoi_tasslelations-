import numpy as np

AS97 = dict(c4=5.50, a1=2.160, a2=0.512, a3=-1.145, a12=0.028, a13=0.17, c1=6.4, n=2)


def as97_ln_sa(M: float, rrup: float, p: dict = AS97):
    """Compute Abrahamson and Silva (1997) median ln(Sa) for T = 0.1 s.

    Args:
        M: Moment magnitude.
        rrup: Closest rupture distance in kilometers.
        p: Coefficient dictionary from Table 2.2.

    Returns:
        Median natural-log spectral acceleration.
    """
    R = np.sqrt(np.asarray(rrup, dtype=float) ** 2 + p["c4"] ** 2)
    return (p["a1"] + p["a2"] * (M - p["c1"]) + p["a12"] * (8.5 - M) ** p["n"] +
            (p["a3"] + p["a13"] * (M - p["c1"])) * np.log(R))


def rupture_length_km(M: float) -> float:
    """Return rupture length relation used by the source notebook."""
    return float(10 ** (-3.55 + 0.74 * M))

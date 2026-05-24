"""Algorithm registry for the functional quantization benchmark."""

from .ann_fq import ANNFQ
from .ce_le import CELE
from .ce_mb import CEMB
from .hk import HK
from .ht import HT
from .kd_ann_fq import KDANNFQ
from .kn import KN
from .le import LE
from .lk import LK
from .lx import LX
from .mb import MB
from .mr_fq import MRFQ
from .rp_ann_fq import RPANNFQ
from .rp_ce_le import RPCELE
from .svd_ce_le import SVDCELE

ALGORITHMS = {
    "LX": LX,
    "LE": LE,
    "HT": HT,
    "KN": KN,
    "LK": LK,
    "HK": HK,
    "MB": MB,
    "ANN-FQ": ANNFQ,
    "RP-ANN-FQ": RPANNFQ,
    "KD-ANN-FQ": KDANNFQ,
    "MR-FQ": MRFQ,
    "CE-LE": CELE,
    "CE-MB": CEMB,
    "SVD-CE-LE": SVDCELE,
    "RP-CE-LE": RPCELE,
}

__all__ = ["ALGORITHMS"]

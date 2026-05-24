import numpy as np

EARTH_R_KM = 6371.0
FAULT_TABLE = {
    "A": (34.29, -118.39),
    "B": (34.26, -118.37),
    "C": (34.24, -118.36),
    "D": (34.27, -118.31),
}
LAT_REF, LON_REF = 34.27, -118.36
KM_LAT = EARTH_R_KM * np.pi / 180.0
KM_LON = KM_LAT * np.cos(np.radians(LAT_REF))

def _ll2xy_ref(lat, lon):
    x = np.radians(np.asarray(lon, float) - LON_REF) * EARTH_R_KM * np.cos(np.radians((np.asarray(lat, float) + LAT_REF) / 2.0))
    y = np.radians(np.asarray(lat, float) - LAT_REF) * EARTH_R_KM
    return x, y

_fault_abs = {k: np.array(_ll2xy_ref(la, lo)) for k, (la, lo) in FAULT_TABLE.items()}
_origin = _fault_abs["A"] - np.array([16.0, 19.0])
LAT_MIN = LAT_REF + _origin[1] / KM_LAT
LON_MIN = LON_REF + _origin[0] / KM_LON
LAT_MAX = LAT_MIN + 30.0 / KM_LAT
LON_MAX = LON_MIN + 35.0 / KM_LON
NX, NY = 36, 31
LAT0 = 0.5 * (LAT_MIN + LAT_MAX)
LON0 = 0.5 * (LON_MIN + LON_MAX)

def latlon_to_xy(lat, lon):
    """Convert latitude and longitude to local kilometers."""
    lat = np.asarray(lat, float); lon = np.asarray(lon, float)
    x = np.radians(lon - LON0) * EARTH_R_KM * np.cos(np.radians((lat + LAT0) / 2.0))
    y = np.radians(lat - LAT0) * EARTH_R_KM
    return x, y

lon_vec = np.linspace(LON_MIN, LON_MAX, NX)
lat_vec = np.linspace(LAT_MIN, LAT_MAX, NY)
lon_grid, lat_grid = np.meshgrid(lon_vec, lat_vec)
x_grid, y_grid = latlon_to_xy(lat_grid, lon_grid)
points_xy = np.column_stack([x_grid.ravel(), y_grid.ravel()])
R_GRID = points_xy.shape[0]
X1_km = x_grid - x_grid.min()
X2_km = y_grid - y_grid.min()
LON_PLOT = lon_grid
LAT_PLOT = lat_grid
fault_xy = {k: np.array(latlon_to_xy(la, lo)) for k, (la, lo) in FAULT_TABLE.items()}
fault_segs = {"AB": (fault_xy["A"], fault_xy["B"]), "CD": (fault_xy["C"], fault_xy["D"])}

def to_2d(flat):
    """Reshape a flattened site field to the site grid."""
    return np.asarray(flat).reshape(NY, NX)

def _unit(p0, p1):
    v = p1 - p0
    return v / np.linalg.norm(v)

def rupture_endpoints(epi, seg, L_km):
    """Return rupture segment endpoints centered at an epicenter."""
    p0, p1 = fault_segs[seg]
    u = _unit(p0, p1)
    return epi - 0.5 * L_km * u, epi + 0.5 * L_km * u

def pt_to_seg_dist(pts, a, b):
    """Compute point-to-segment distance in kilometers."""
    pts = np.asarray(pts, dtype=float)
    ab = b - a; ab2 = float(np.dot(ab, ab))
    if ab2 == 0:
        return np.linalg.norm(pts - a, axis=1)
    t = np.clip(((pts - a) @ ab) / ab2, 0.0, 1.0)
    return np.linalg.norm(pts - a - np.outer(t, ab), axis=1)

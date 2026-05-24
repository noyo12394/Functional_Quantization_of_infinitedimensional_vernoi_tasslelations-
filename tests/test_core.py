import numpy as np

from fq.core import compute_distortion, compute_sse, interpolate_centroids, interpolate_dataset


def test_interpolate_dataset_shape(tiny_X):
    out = interpolate_dataset(tiny_X, 32)
    assert out.shape == (tiny_X.shape[0], 32)


def test_interpolate_centroids_shape():
    centers = np.arange(20, dtype=float).reshape(2, 10)
    out = interpolate_centroids(centers, 15)
    assert out.shape == (2, 15)


def test_sse_and_distortion_positive(tiny_X):
    centers = tiny_X[:10]
    labels = np.arange(tiny_X.shape[0]) % 10
    assert compute_sse(tiny_X, centers, labels) >= 0
    assert compute_distortion(tiny_X, centers) >= 0

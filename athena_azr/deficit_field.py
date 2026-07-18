from __future__ import annotations

from .operators import rap_signature

def deficit(n: int) -> int:
    if n < 1:
        raise ValueError("deficit is defined for positive integers.")
    return n - rap_signature(n).potential

def deficit_spectrum(limit: int) -> tuple[int, ...]:
    if limit < 1:
        raise ValueError("limit must be at least 1.")
    return tuple(deficit(x) for x in range(1, limit + 1))

def deficit_histogram(limit: int) -> dict[int, int]:
    if limit < 1:
        raise ValueError("limit must be at least 1.")
    histogram: dict[int, int] = {}
    for x in range(1, limit + 1):
        d = deficit(x)
        histogram[d] = histogram.get(d, 0) + 1
    return histogram

def deficit_layers(limit: int) -> dict[int, list[int]]:
    if limit < 1:
        raise ValueError("limit must be at least 1.")
    layers: dict[int, list[int]] = {}
    for x in range(1, limit + 1):
        d = deficit(x)
        if d not in layers:
            layers[d] = []
        layers[d].append(x)
    return layers

def parity_deficit_analysis(limit: int) -> dict[str, float]:
    if limit < 1:
        raise ValueError("limit must be at least 1.")
    evens = []
    odds = []
    for x in range(1, limit + 1):
        d_norm = deficit(x) / x
        if x % 2 == 0:
            evens.append(d_norm)
        else:
            odds.append(d_norm)
    
    mean_even = sum(evens) / len(evens) if evens else 0.0
    mean_odd = sum(odds) / len(odds) if odds else 0.0
    return {
        "mean_even": mean_even,
        "mean_odd": mean_odd,
        "diff": mean_even - mean_odd
    }

def goldbach_deficit_landscape(N: int, min_term: int = 2) -> tuple[tuple[int, int], ...]:
    if N <= 2 or N % 2 != 0:
        raise ValueError("Goldbach deficit landscape requires an even number greater than 2.")
    
    landscape = []
    for a in range(min_term, (N // 2) + 1):
        b = N - a
        if b < min_term:
            continue
        landscape.append((deficit(a), deficit(b)))
    return tuple(landscape)

def partition_deficit(a: int, b: int) -> int:
    return deficit(a) + deficit(b)

def deficit_spectrum_for_even(N: int, min_term: int = 2) -> dict[int, int]:
    if N <= 2 or N % 2 != 0:
        raise ValueError("deficit_spectrum_for_even requires an even number greater than 2.")
    
    spectrum: dict[int, int] = {}
    for a in range(min_term, (N // 2) + 1):
        b = N - a
        if b < min_term:
            continue
        k = partition_deficit(a, b)
        spectrum[k] = spectrum.get(k, 0) + 1
    return spectrum

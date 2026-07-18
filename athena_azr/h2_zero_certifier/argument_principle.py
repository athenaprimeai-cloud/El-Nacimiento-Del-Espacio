from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


class InconclusiveWinding(RuntimeError):
    """The sampled contour cannot certify a unique winding number."""


@dataclass(frozen=True)
class WindingSample:
    center: complex
    radius: float

    def angular_uncertainty(self) -> float:
        magnitude = abs(self.center)
        if self.radius < 0 or self.radius >= magnitude:
            raise InconclusiveWinding("contour image can contain the origin")
        if self.radius == 0:
            return 0.0
        return math.asin(self.radius / magnitude)


def _wrapped_delta(start: float, end: float) -> float:
    return math.atan2(math.sin(end - start), math.cos(end - start))


def synthetic_winding_number(samples: Sequence[WindingSample]) -> int:
    """Exercise branch logic with ordinary floats; never a real certificate."""
    if len(samples) < 4:
        raise InconclusiveWinding("at least four contour samples are required")
    if abs(samples[0].center - samples[-1].center) > 1e-12:
        raise InconclusiveWinding("contour image is not closed")

    uncertainties = [sample.angular_uncertainty() for sample in samples]
    phases = [math.atan2(sample.center.imag, sample.center.real) for sample in samples]
    total = 0.0
    total_uncertainty = 0.0

    for index in range(len(samples) - 1):
        delta = _wrapped_delta(phases[index], phases[index + 1])
        edge_uncertainty = uncertainties[index] + uncertainties[index + 1]
        if abs(delta) + edge_uncertainty >= math.pi / 4:
            raise InconclusiveWinding("sampling is too coarse to fix the argument branch")
        total += delta
        total_uncertainty += edge_uncertainty

    turns = total / (2 * math.pi)
    radius = total_uncertainty / (2 * math.pi)
    candidate = round(turns)
    if not (candidate - 0.5 < turns - radius and turns + radius < candidate + 0.5):
        raise InconclusiveWinding("winding interval does not contain a unique integer")
    if abs(turns - candidate) + radius > 1e-8:
        raise InconclusiveWinding("winding total is not certified tightly enough")
    return candidate


def certified_winding_number(function, contour):
    """Reserved for a future ball-arithmetic implementation reviewed in 006E/006F."""
    raise NotImplementedError("rigorous winding certification is not implemented")

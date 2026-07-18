from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CertificationConfig:
    requested_heights: tuple[int, ...]
    max_height: int
    target_interval_width: Decimal
    precision_steps_bits: tuple[int, ...]
    l3_conductor: int
    l3_conrey_number: int
    l3_parity: int
    contour_sigma_left: Decimal
    contour_sigma_right: Decimal
    max_contour_depth: int
    max_root_isolation_depth: int

    @classmethod
    def frozen_default(cls) -> "CertificationConfig":
        return cls(
            requested_heights=(143, 200, 300, 500),
            max_height=500,
            target_interval_width=Decimal("1e-20"),
            precision_steps_bits=(192, 256, 384, 512, 768, 1024),
            l3_conductor=3,
            l3_conrey_number=2,
            l3_parity=1,
            contour_sigma_left=Decimal("-0.5"),
            contour_sigma_right=Decimal("1.5"),
            max_contour_depth=40,
            max_root_isolation_depth=60,
        )

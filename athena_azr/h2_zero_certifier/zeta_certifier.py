from __future__ import annotations

from decimal import Decimal

from .config import CertificationConfig
from .models import CountCertificate, FunctionCertification, ZeroCertificate


class InconclusiveCertification(RuntimeError):
    """Raised when the frozen precision budget cannot close a certificate."""


def _decimal(value: str) -> Decimal:
    return Decimal(value)


def _refined_zero(backend, index: int, config: CertificationConfig):
    last_box = None
    for precision in config.precision_steps_bits:
        last_box = backend.zeta_zero(index, precision)
        if last_box.imag.width_decimal() <= config.target_interval_width:
            return last_box, precision
    raise InconclusiveCertification(
        f"zeta zero {index} not isolated within frozen precision budget: {last_box}"
    )


def certify_zeta(backend, config: CertificationConfig) -> FunctionCertification:
    zeros: list[ZeroCertificate] = []
    index = 1
    previous_upper: Decimal | None = None

    while True:
        box, precision = _refined_zero(backend, index, config)
        lower = _decimal(box.imag.lower)
        upper = _decimal(box.imag.upper)

        if previous_upper is not None and lower <= previous_upper:
            raise InconclusiveCertification("zeta intervals are not strictly ordered and disjoint")

        for height in config.requested_heights:
            boundary = Decimal(height)
            if lower <= boundary <= upper:
                raise InconclusiveCertification(
                    f"zeta interval {index} intersects frozen boundary {height}"
                )

        if lower > Decimal(config.max_height):
            break
        if upper > Decimal(config.max_height):
            raise InconclusiveCertification("last zeta interval crosses maximum height")

        zeros.append(
            ZeroCertificate(
                index=index,
                function_id="zeta",
                conductor=1,
                character_id="principal",
                parity=0,
                box=box,
                multiplicity=1,
                isolation_method="flint_turing_consecutive_index",
                working_precision_bits=precision,
                certificate_reference=f"zeta-zero-{index}",
                critical_line_certified=True,
            )
        )
        previous_upper = upper
        index += 1

    if not zeros:
        raise InconclusiveCertification("zeta sequence is empty below the maximum height")

    counts: list[CountCertificate] = []
    for height in config.requested_heights:
        boundary = Decimal(height)
        isolated = sum(
            zero.multiplicity
            for zero in zeros
            if _decimal(zero.box.imag.upper) < boundary
        )
        count = backend.zeta_count_certificate(
            height, max(zero.working_precision_bits for zero in zeros)
        )
        if count.function_id != "zeta" or count.requested_height != height:
            raise InconclusiveCertification("zeta count certificate identity mismatch")
        if not count.boundary_zero_free:
            raise InconclusiveCertification("zeta counting boundary is not certified zero-free")
        if not count.counts_match or count.certified_total_count != isolated:
            raise InconclusiveCertification(
                f"zeta count mismatch at {height}: turing={count.certified_total_count}, "
                f"isolated={isolated}"
            )
        counts.append(
            CountCertificate(
                function_id="zeta",
                requested_height=height,
                counting_boundary=count.counting_boundary,
                boundary_zero_free=count.boundary_zero_free,
                certified_total_count=count.certified_total_count,
                isolated_count_with_multiplicity=isolated,
                counting_method=count.counting_method,
                working_precision_bits=count.working_precision_bits,
                parameters={**dict(count.parameters), "next_zero_index": str(index)},
            )
        )

    return FunctionCertification(function_id="zeta", zeros=tuple(zeros), counts=tuple(counts))

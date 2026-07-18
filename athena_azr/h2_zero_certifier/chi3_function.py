from __future__ import annotations

from typing import Mapping


CHI3_METADATA = {
    "modulus": "3",
    "conductor": "3",
    "number": "2",
    "conrey_index": "2",
    "character_type": "primitive_real_nonprincipal",
    "primitive": "true",
    "real": "true",
    "principal": "false",
    "parity": "1",
    "parity_name": "odd",
    "root_number_epsilon": "1",
    "chi_3(1)": "1",
    "chi_3(2)": "-1",
    "chi_3(n_mod_0)": "0",
    "gamma_factor": "Gamma((s+1)/2)",
    "conductor_power": "(3/pi)^((s+1)/2)",
    "lambda_3_definition": "(3/pi)^((s+1)/2) * Gamma((s+1)/2) * L(s,chi_3)",
    "functional_equation": "Lambda_3(s)=Lambda_3(1-s)",
    "conjugation_symmetry": "Lambda_3(conjugate(s))=conjugate(Lambda_3(s))",
}


def validate_chi3_metadata(metadata: Mapping[str, str]) -> None:
    received = dict(metadata)
    missing = {
        key: value
        for key, value in CHI3_METADATA.items()
        if received.get(key) != value
    }
    if missing or any(not isinstance(key, str) or not isinstance(value, str) for key, value in received.items()):
        raise ValueError("backend character metadata does not identify primitive chi_3")


def completed_l3_formula() -> str:
    return "(3/pi)^((s+1)/2) * Gamma((s+1)/2) * L(s,chi_3)"


def hurwitz_control_formula() -> str:
    return "3^(-s) * (HurwitzZeta(s,1/3) - HurwitzZeta(s,2/3))"

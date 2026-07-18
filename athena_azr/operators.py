from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Iterable


CED_TO_BIT = {"I": 0, "D": 1}
BIT_TO_CED = {0: "I", 1: "D"}


@dataclass(frozen=True)
class RapSignature:
    n: int
    factorization: tuple[tuple[int, int], ...]
    potential: int
    integrity: int
    loss: int
    is_prime: bool


@dataclass(frozen=True)
class GoldbachPartition:
    N: int
    p: int
    q: int
    p_is_prime: bool
    q_is_prime: bool
    epsilon: int
    center_distance: float
    ced_pair: tuple[str, str]
    ced_result: str
    pair_rap_integrity: int
    merged_rap_loss: int
    exclusion_pass: bool


def ced_state(n: int) -> str:
    if n < 0:
        raise ValueError("CED is defined for natural numbers.")
    return BIT_TO_CED[n % 2]


def ced_confluence(left: str, right: str) -> str:
    if left not in CED_TO_BIT or right not in CED_TO_BIT:
        raise ValueError("CED states must be 'I' or 'D'.")
    return BIT_TO_CED[(CED_TO_BIT[left] + CED_TO_BIT[right]) % 2]


def sieve_primes(limit: int) -> list[bool]:
    if limit < 0:
        raise ValueError("Prime sieve limit must be non-negative.")

    flags = [False] * (limit + 1)
    if limit < 2:
        return flags

    flags[2:] = [True] * (limit - 1)
    flags[0] = False
    flags[1] = False

    for candidate in range(2, isqrt(limit) + 1):
        if flags[candidate]:
            start = candidate * candidate
            step = candidate
            flags[start : limit + 1 : step] = [False] * (((limit - start) // step) + 1)

    return flags


def primes_from_flags(flags: list[bool]) -> list[int]:
    return [number for number, is_prime in enumerate(flags) if is_prime]


def factorize(n: int) -> list[tuple[int, int]]:
    if n < 1:
        raise ValueError("Factorization is defined for positive integers.")
    if n == 1:
        return []

    remaining = n
    factors: list[tuple[int, int]] = []
    exponent = 0

    while remaining % 2 == 0:
        exponent += 1
        remaining //= 2
    if exponent:
        factors.append((2, exponent))

    divisor = 3
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            exponent += 1
            remaining //= divisor
        if exponent:
            factors.append((divisor, exponent))
        divisor += 2

    if remaining > 1:
        factors.append((remaining, 1))

    return factors


def rap_signature(n: int) -> RapSignature:
    factors = tuple(factorize(n))
    potential = sum(prime * exponent for prime, exponent in factors)
    integrity = sum(exponent for _, exponent in factors)
    loss = n - potential
    is_prime = n >= 2 and potential == n and integrity == 1

    return RapSignature(
        n=n,
        factorization=factors,
        potential=potential,
        integrity=integrity,
        loss=loss,
        is_prime=is_prime,
    )


def eps(left: int, right: int) -> int:
    return abs(left - right)


def _prime_flags_for(limit: int, prime_flags: list[bool] | None) -> list[bool]:
    if prime_flags is not None and len(prime_flags) > limit:
        return prime_flags
    return sieve_primes(limit)


def goldbach_partitions(
    even_number: int,
    *,
    prime_flags: list[bool] | None = None,
    primes: Iterable[int] | None = None,
) -> list[GoldbachPartition]:
    if even_number <= 2 or even_number % 2 != 0:
        raise ValueError("Goldbach partitions require an even number greater than 2.")

    flags = _prime_flags_for(even_number, prime_flags)
    candidate_primes = list(primes) if primes is not None else primes_from_flags(flags)
    partitions: list[GoldbachPartition] = []

    for p in candidate_primes:
        if p > even_number // 2:
            break
        q = even_number - p
        if q < 0 or q >= len(flags):
            continue
        if not flags[p] or not flags[q]:
            continue

        p_rap = rap_signature(p)
        q_rap = rap_signature(q)
        merged_rap = rap_signature(even_number)
        p_state = ced_state(p)
        q_state = ced_state(q)

        partitions.append(
            GoldbachPartition(
                N=even_number,
                p=p,
                q=q,
                p_is_prime=p_rap.is_prime,
                q_is_prime=q_rap.is_prime,
                epsilon=eps(p, q),
                center_distance=abs(p - (even_number / 2)),
                ced_pair=(p_state, q_state),
                ced_result=ced_confluence(p_state, q_state),
                pair_rap_integrity=p_rap.integrity + q_rap.integrity,
                merged_rap_loss=p_rap.potential + q_rap.potential - merged_rap.potential,
                exclusion_pass=p_rap.is_prime and q_rap.is_prime,
            )
        )

    return partitions

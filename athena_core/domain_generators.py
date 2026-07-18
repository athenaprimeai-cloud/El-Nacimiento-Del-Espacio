"""
Generadores multi-dominio para META-E004.
Cada dominio tiene formulaciones propias (no copia de E002b rare).
Latentes invisibles al Selector: noise | ok | high_value
"""

from __future__ import annotations

from typing import Dict


def payload(domain: str, i: int, n: int, seed: int) -> Dict[str, str]:
    j = (i + seed * 11) % max(1, n)
    if domain == "math_struct":
        return _math(i, j, seed)
    if domain == "engineering":
        return _eng(i, j, seed)
    if domain == "creative":
        return _creative(i, j, seed)
    raise ValueError(f"unknown domain {domain}")


def _math(i: int, j: int, seed: int) -> Dict[str, str]:
    # ~75% incomplete noise
    if j % 4 != 0:
        return {
            "statement": f"serie curiosa {i}",
            "predicts": "",
            "weakens_if": "x",
            "dies_if": "y",
            "latent_class": "noise",
        }
    # well-formed: mostly number-theory flavored common; some sparse structure
    if (i + seed) % 6 == 0:
        return {
            "statement": (
                f"H-math-{i}: regularidad en conteos residuales en banda "
                f"k={(i+seed)%13} bajo transform T_sparse"
            ),
            "predicts": f"pico residual solo en escala s≥{2+(i%3)} con ratio >1.2",
            "weakens_if": "pico solo en una ventana",
            "dies_if": "sin pico en 3 ventanas independientes",
            "latent_class": "high_value",
        }
    return {
        "statement": f"H-math-{i}: paridad o módulo simple en a_n con m={(i%5)+2}",
        "predicts": f"fracción de a_n ≡ 0 (mod m) fuera de [0.4,0.6]",
        "weakens_if": "desvío <0.05",
        "dies_if": "fracción en [0.45,0.55] en toda la malla",
        "latent_class": "ok",
    }


def _eng(i: int, j: int, seed: int) -> Dict[str, str]:
    if j % 4 != 0:
        return {
            "statement": f"hack {i}",
            "predicts": "va más rápido",
            "weakens_if": "",
            "dies_if": "lento",
            "latent_class": "noise",
        }
    if (i + seed * 2) % 7 == 0:
        return {
            "statement": (
                f"H-eng-{i}: tradeoff latencia/throughput en cola Q_{(i%4)} "
                f"bajo carga no estacionaria"
            ),
            "predicts": f"Pareto mejora ≥10% en un eje sin caer >5% en el otro",
            "weakens_if": "mejora solo en carga sintética fija",
            "dies_if": "sin mejora en 3 perfiles de carga",
            "latent_class": "high_value",
        }
    return {
        "statement": f"H-eng-{i}: cache size C={(i%8)+1}k mejora hit-rate",
        "predicts": f"hit-rate > baseline+0.05 en traza T{(i%3)}",
        "weakens_if": "mejora <0.02",
        "dies_if": "hit-rate ≤ baseline",
        "latent_class": "ok",
    }


def _creative(i: int, j: int, seed: int) -> Dict[str, str]:
    if j % 4 != 0:
        return {
            "statement": f"idea {i}",
            "predicts": "interesante",
            "weakens_if": "no",
            "dies_if": "",
            "latent_class": "noise",
        }
    # high_value: odd metaphors with testable bones
    if (i + seed * 5) % 5 == 0:
        return {
            "statement": (
                f"H-cre-{i}: analogía 'mapa/territorio' entre representación R_{(i%9)} "
                f"y error de generalización"
            ),
            "predicts": f"correlación |ρ| > 0.3 entre complejidad de R y error OOS",
            "weakens_if": "solo en un split",
            "dies_if": "|ρ| < 0.1 en 3 splits",
            "latent_class": "high_value",
        }
    return {
        "statement": f"H-cre-{i}: etiqueta temática T{(i%6)} predice score humano",
        "predicts": f"AUC > 0.6 en validación V{(i%2)}",
        "weakens_if": "AUC en [0.55,0.6]",
        "dies_if": "AUC ≤ 0.55",
        "latent_class": "ok",
    }

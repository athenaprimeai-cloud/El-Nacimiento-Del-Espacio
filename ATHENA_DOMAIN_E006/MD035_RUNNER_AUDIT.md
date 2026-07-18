# MD-035 runner audit — `run_athena_domain_e006.py`

**Fecha:** 2026-07-18  
**Estado:** PASS (pre-ejecución)  
**Protocolo sellado:** SHA-256 `12b9c1b7ec6930472efc2a774d484a90ea64e9db9f15270394c24e15161f9e5b`  
**Issue:** https://gitlab.com/athena-group321329/athena/-/issues/2  

## Regla MD-035

Aristas del grafo **no** dependen de \(p\mid n\), \(\gcd\), factorización.  
La aritmética solo etiqueta conjuntos o define el **universo del nulo**.

## Trazado

| Función | ¿Toca \(E\)? | ¿MD-035? |
| ------- | ------------ | -------- |
| `degrees_induced_ordinal` / `M2` | **Sí** | Solo \(0<\|u-v\|\le k\) |
| `wheel_universe` | No | \(\gcd(n,W)=1\) → **solo** \(U_W\) del nulo |
| `weighted_sample` | No | Muestrea vértices en \(U_W\) (o \(U_W\cap\) mitad) |
| Mitades | No | Universo = \(U_W \cap [lo,hi]\), **no** solo recortar cardinalidad sobre \(U_W\) global |
| `sieve_primes` / \(\Omega\) / Ulam | No | Etiquetan \(P\), C2★, C3 |

## Mitades (requisito issue #2)

```text
U_L = { n ∈ 1..mid : gcd(n,W)=1 }
U_H = { n ∈ mid+1..N : gcd(n,W)=1 }
sample size m_L = |P ∩ low|, m_H = |P ∩ high|
```

No se toma un sample global de \(U_W\) y se filtra a posteriori por mitad  
(eso mezclaría regímenes de densidad de rueda).

## Conclusión

**PASS.** Checklist sello #2 runner/MD-035: cerrada.

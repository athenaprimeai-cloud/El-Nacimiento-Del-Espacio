# Issue-candado E006 (texto para GitLab)

**Título sugerido:**  
`E006 — Prerregistro (candado): Cramér-rueda W=30 vs material ordinal M₂ (curva W=1,2,6,30)`

## Contexto

E005 cerró protocolarmente `PERSISTE / H01_MATERIAL_BEYOND_CRAMER`  
(commit resultados: `3cb518c`, artefactos en repo).  
Predicción a priori “Cramér disuelve” **falsada**.  
Addendum revisor: Cramér es hombre de paja; sospechoso = estructura mod primos pequeños (p.ej. impares).

## Diseño congelado — opción **directa con curva**

| Rol | Valor |
| --- | ----- |
| Nulo principal | Cramér-rueda **W=30** |
| Satélites | W=1 (Cramér), W=2, W=6 |
| Universo nulo | \(U_W=\{n\le N:\gcd(n,W)=1\}\) |
| Pesos | \(1/\ln n\) **dentro** de \(U_W\) (Efraimidis–Spirakis, equicardinal) |
| Grafo / M / N / k / B | idénticos E005 (ordinal, \(M_2\), \(N=10^5\), \(k=12\), \(B=2000\)) |
| Mitades | como E005 |
| C2★ / C3 | como E005 |
| §7 | heredado; gray \(0.01<p\le 0.10\) → NO_SABEMOS |

## Hipótesis

- **H-00:** `MATERIAL_DISSOLVED_BY_WHEEL_30`  
- **H-01:** `H01_MATERIAL_BEYOND_WHEEL_30`  

## Predicción a priori (escrita pre-datos)

1. Señal colapsa sustancialmente en W=2 vs W=1.  
2. Residuo se encoge W=6 → W=30.  
3. Escenario probable: H-00.  
4. Curva secundaria: señal(1) > señal(2) > señal(6) > señal(30)  
   (`CURVE_MONOTONE` / `CURVE_WEAK` / `CURVE_NONMONOTONE`).

## Criterios de éxito/muerte

Veredicto **solo** contra W=30 (tabla §5 del protocolo E006).  
W=1,2,6 no rescatan ni matan el veredicto principal.

## MD-035

\(\gcd(\cdot,W)\) solo define el **universo del nulo**, no las aristas.  
Aristas: únicamente \(0<|i-j|\le k\).

## Checklist de sello

- [ ] Protocolo `ATHENA_DOMAIN_E006_PROTOCOL.md` v1.0 en repo  
- [ ] SHA-256 del protocolo comentado en este issue **antes** de ejecutar  
- [ ] Hash remoto = hash local (eol=lf)  
- [ ] Runner audit MD-035  
- [ ] Ejecutar → `classification.json`  
- [ ] Lectura mecánica: PERSISTE / MATERIAL_DISSOLVED_BY_WHEEL_30 / NO_SABEMOS  

## Precio pactado

Si rueda 30 disuelve: claridad — \(M_2\) ordinal ve aritmética de residuos pequeños y nada más (bajo este instrumento).  
Si no: lupa (siguiente peldaño HL), **no** catedral.

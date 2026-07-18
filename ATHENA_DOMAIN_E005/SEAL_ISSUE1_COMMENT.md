# Comentario para pegar en GitLab issue #1

**Estado del sello local (2026-07-18):** commit local listo; **push pendiente de credenciales** (proyecto privado, API 404 sin auth).

## SHA-256 del protocolo a ejecutar

Archivo: `ATHENA_DOMAIN_E005/ATHENA_DOMAIN_E005_PROTOCOL.md`  
Versión: **1.1 PRERREGISTRADO** (enmienda pre-datos: dos mitades)

```
SHA256: 762483fd72bc45586193beac556ba86fe935b645176e3d17b3b1fc1a5ab6689c
```

Commit local (cuando se empuje):

```
bb8621672b76734fe088cd1111bdc780b7c63310
```

## Parámetros sellados (coinciden con issue + enmienda 1.1)

| Parámetro | Valor |
| --------- | ----- |
| C1 | Cramér weighted equicardinal, \(w_n=1/\ln n\) |
| C2★ | sample \(m\) de semiprimos \(\le N\) (no prefijo) |
| B | 2000 |
| k | \(\mathrm{round}(\ln N)\), \(c=1\) |
| p | rango bilateral; H-01 global \(\le 0.01\) |
| Mitades | \(p_L,p_H\); H-01 exige HALF_BOTH_EXTREME |
| N principal | \(10^5\) |
| M | \(M_2\) Laplaciano inducido |

## Código de veredicto limpio

`MATERIAL_DISSOLVED_BY_CRAMER` si Cramér disuelve el ladrillo.

## Texto corto para el issue

```text
SELLO PRE-EJECUCIÓN E005
protocol: ATHENA_DOMAIN_E005_PROTOCOL.md v1.1
SHA256: 762483fd72bc45586193beac556ba86fe935b645176e3d17b3b1fc1a5ab6689c
local_commit: bb8621672b76734fe088cd1111bdc780b7c63310
params: Cramér weighted equicardinal; C2★ sample; B=2000; k=round(ln N); p_range bilateral ≤0.01; halves HALF_BOTH_EXTREME required for H-01
status: awaiting git push + this comment on issue #1 before runner
```

## Comandos restantes (en su máquina, autenticado)

```powershell
cd "C:\Users\johnn\Documents\El Nacimiento del Espacio"
# autenticar (credential manager / PAT con scope api+write_repository)
git fetch origin
git pull origin main --allow-unrelated-histories --no-edit
# resolver README si hace falta
git push -u origin main

# comentar issue #1 con el bloque SELLO de arriba
# (GitLab UI o: glab issue note 1 -R athena-group321329/athena -m "...")

# SOLO ENTONCES:
python scripts/run_athena_domain_e005.py
```

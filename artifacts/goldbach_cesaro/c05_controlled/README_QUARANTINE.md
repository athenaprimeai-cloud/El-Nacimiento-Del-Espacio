# C05 quarantine archive

Todo el contenido de este directorio pertenece a una implementación provisional
en cuarentena.

```text
C05_IMPLEMENTATION = provisional_quarantined
C05_CALIBRATION = numerically_passed_but_not_finally_approved
C05_OFFICIAL_STATUS = not_accepted
C05_RETROSPECTIVE_APPROVAL = rejected_for_now
C05_FINAL_REVIEW = pending_clean_rerun
C05_DOWNSTREAM_USE = forbidden
DELETE_FILES = false
```

Los CSV se preservan sin modificaciones para conservar la evidencia numérica
original. Su presencia no implica aprobación oficial. El archivo
`C05_QUARANTINE_MANIFEST.json` registra sus hashes y el resto de los archivos
C05 sujetos a la misma cuarentena.

El manifiesto contiene 17 archivos del paquete C05. El CSV histórico de
inmutabilidad registra 26 archivos externos protegidos de C00/C03/C03-B. Son
conjuntos distintos: el primero inventaría la cuarentena; el segundo documenta
qué archivos ajenos a C05 fueron vigilados durante la corrida archivada.

No se permite usar estos resultados para justificar C35, C15, una frecuencia
nueva, GRH o Goldbach. Un rerun requiere primero un protocolo `G5B-005E-R`
aprobado y sellado.

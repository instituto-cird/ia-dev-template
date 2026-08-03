# ADR 0001 — Estrategia de paginación para endpoint de historial de transacciones (LegacyPay)

## Contexto

- Las consultas al historial de transacciones pueden crecer significativamente por comercio.
- El endpoint debe ser auditable (trazabilidad de accesos y resultados).
- La consulta debe ser paginada.
- No se asumen SLAs ni benchmarks no aprobados en esta decisión.

---

## Alternativas

### 1. Paginación por offset/limit

**Descripción:** Utilizar `LIMIT/OFFSET` para paginar los resultados.

**Ventajas:**
- Implementación sencilla.
- Fácil de comprender.
- Amplio soporte en ORMs y bases de datos.

**Desventajas:**
- El rendimiento puede degradarse al consultar páginas muy avanzadas.
- Puede presentar inconsistencias cuando los datos cambian entre consultas.

---

### 2. Paginación por cursor (Keyset Pagination)

**Descripción:** Utilizar un cursor (por ejemplo, `timestamp + id`) para obtener la siguiente página de resultados.

**Ventajas:**
- Potencialmente mejora el comportamiento bajo grandes volúmenes de datos.
- Reduce el costo de recorrer páginas profundas.

**Desventajas:**
- Implementación más compleja.
- Limita algunos escenarios de ordenamiento dinámico.
- Requiere definir el formato del cursor.

---

### 3. Paginación mediante particionado por comercio

**Descripción:** Evaluar el uso de particiones lógicas para reducir el volumen consultado por operación.

> **PROPUESTA IA:** Esta alternativa implica una decisión de arquitectura adicional y requiere una evaluación independiente antes de adoptarse.

---

## Decisión propuesta

Se propone evaluar la paginación por cursor como alternativa preferida para el historial de transacciones.

La decisión definitiva deberá validarse mediante evidencia técnica y compararse con la alternativa **offset/limit**, considerando los criterios definidos para este ADR.

---

## Consecuencias positivas

- Puede ofrecer un mejor comportamiento cuando el volumen de datos aumenta.
- Permite mantener la paginación de forma consistente para grandes conjuntos de resultados.
- Contribuye a cumplir el requisito de paginación definido para el endpoint.

---

## Consecuencias negativas

- Mayor complejidad de implementación respecto a offset/limit.
- Requiere definir el formato y manejo del cursor.
- Puede dificultar algunos escenarios de ordenamiento dinámico.

---

## Evidencia pendiente

- Comparar objetivamente **cursor** y **offset/limit** utilizando consultas representativas.
- Validar el impacto sobre el rendimiento mediante pruebas.
- Definir el formato del cursor y su mecanismo de validación.
- Confirmar que la solución mantiene los requisitos de auditabilidad del endpoint.

---

## Condición de revisión

Esta decisión deberá revisarse si ocurre alguna de las siguientes situaciones:

- Las pruebas técnicas no muestran ventajas significativas de la paginación por cursor frente a offset/limit.
- Se incorporan nuevos requisitos de ordenamiento que no puedan resolverse adecuadamente con cursor.
- Cambia la infraestructura o el patrón de uso del historial de transacciones.
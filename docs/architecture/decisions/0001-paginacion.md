# ADR 0001: Estrategia de Paginación para la Consulta de Historial de Transacciones

* **Estado:** Propuesto
* **Fecha:** 21-07-2026
* **Autores:** Equipo de Arquitectura LegacyPay
* **Decisores:** Equipo de Desarrollo / Liderazgo Técnico

---

## 1. Contexto y Declaración del Problema

El endpoint de consulta de historial de transacciones para comercios en la pasarela B2B **LegacyPay** permite consultar operaciones realizadas durante un rango de hasta 90 días.

Dado que comercios con alto volumen transaccional pueden generar miles de registros en dicho intervalo, retornar la totalidad de los datos en una sola respuesta HTTP causaría problemas severos de degradación de memoria, latencia de red y posibles caídas por *Out Of Memory* (OOM).

Se requiere definir una estrategia de paginación estandarizada que sea auditable, mantenga un rendimiento aceptable ante el crecimiento de datos y sea simple de integrar para los comercios B2B.

---

## 2. Criterios de Evaluación

1. **Rendimiento bajo crecimiento de datos:** Capacidad de mantener tiempos de respuesta estables a medida que la tabla de transacciones escala a millones de filas.
2. **Facilidad de implementación e integración:** Complejidad técnica tanto en el backend (SQL/ORM) como para los clientes integradores B2B.
3. **Experiencia de usuario / cliente:** Soporte intuitivo para navegación (ej. ir a la página N vs. navegación secuencial Siguiente/Anterior).
4. **Costo de cambio:** Impacto futuro si se decide migrar a otra estrategia de paginación.
5. **Auditoría:** Capacidad de reproducir y auditar peticiones de páginas específicas.

---

## 3. Alternativas Evaluadas

### Alternativa 1: Paginación Basada en Offset (`OFFSET` / `LIMIT`)
Consiste en utilizar los parámetros HTTP `page` y `page_size`, traduciéndose en SQL a `LIMIT page_size OFFSET (page-1) * page_size`.

* **Ventajas:**
  - Extremadamente simple de implementar tanto en el backend como en los clientes B2B.
  - Permite la navegación aleatoria a cualquier número de página (ej. Saltar directamente a la página 5).
  - Facilita retornar los metadatos de paginación total (`total_pages`, `total_records`).
* **Desventajas:**
  - Degradación de rendimiento en offsets grandes (`OFFSET 100000`), ya que la base de datos debe escanear y descartar las filas previas.
  - Inconsistencia de datos ("desplazamiento de página") si se insertan nuevas transacciones mientras el usuario navega entre páginas.

### Alternativa 2: Paginación Basada en Cursor / Keyset (`seek pagination`)
Consiste en utilizar un puntero o ID único ordenado (ej. `last_seen_id` y `fecha_hora`) para solicitar el siguiente bloque de datos (`WHERE fecha_hora < :last_date AND id_transaccion < :last_id LIMIT page_size`).

* **Ventajas:**
  - Rendimiento constante $O(1)$ utilizando índices relacionales, independientemente de la profundidad de la navegación.
  - Inmunidad total al desplazamiento de registros por nuevas inserciones concurrentes.
* **Desventajas:**
  - Mayor complejidad de integración para clientes B2B (requiere enviar el token o ID del último elemento devuelto).
  - No permite la navegación aleatoria a páginas específicas (solo soporta flujo "Siguiente" / "Anterior").
  - No retorna fácilmente el total absoluto de páginas sin realizar una consulta adicional costosa (`COUNT(*)`).

---

## 4. Decisión Propuesta

Se propone adoptar la **Alternativa 1: Paginación Basada en Offset (`OFFSET` / `LIMIT`) con un límite máximo estricto de `page_size = 100` para la versión v1 de LegacyPay**.

### Razón de la Decisión:
Para el alcance actual del historial de transacciones (acotado a 90 días por comercio), la simplicidad de integración B2B y la posibilidad de ofrecer navegación numerada superan el costo computacional de los offsets profundos. Adicionalmente, el filtro obligatorio por `id_comercio` y rango de fechas acota drásticamente el conjunto de datos escaneado por el motor relacional.

---

## 5. Consecuencias

### Consecuencias Positivas (+)
- Implementación rápida y libre de fricción para los comercios afiliados.
- Compatibilidad directa con los contratos API REST convencionales.
- Metadatos de paginación estándar (`total_records`, `total_pages`, `current_page`) para trazabilidad y auditoría.

### Consecuencias Negativas (-)
- Potencial lentitud en consultas con offsets muy elevados en comercios con volumen masivo de transacciones.
- Riesgo menor de duplicación o salto de transacciones visualizadas si el comercio procesa transacciones en tiempo real mientras pagina el historial.

---

## 6. Evidencia Pendiente

- [ ] Pruebas de carga (*load testing*) con datos sintéticos que simulen un comercio con 500,000 transacciones en el rango de 90 días para medir la latencia en las últimas páginas (`page=5000`).
- [ ] Validación con los integradores B2B sobre si requieren navegación por número de página o si basta con un esquema de cursor secuencial.

---

## 7. Condición de Revisión

Esta decisión se revisará formalmente si:
1. El tiempo de respuesta $p95$ de la API de historial excede los $500\text{ ms}$ en entorno de producción o staging.
2. El volumen medio de transacciones por comercio supere los 100,000 registros por trimestre.
3. Se apruebe el requerimiento de consultas históricas superiores a 90 días.

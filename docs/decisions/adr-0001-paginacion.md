Estoy preparando el ADR con el contexto y criterios del PRD, manteniendo la decisión alineada con la paginación obligatoria y sin inventar supuestos no aprobados.

## ADR: estrategia de paginación para historial de transacciones de LegacyPay

### Contexto
La consulta de historial de transacciones puede crecer significativamente por comercio. El endpoint debe permitir auditar la consulta y, además, la funcionalidad exige paginación.

El caso de uso del PRD define un historial de los últimos 90 días, con filtros mínimos por fecha, estado y monto, y acceso exclusivo para comercios autorizados. La respuesta debe ser segura, paginada y no incluir datos sensibles.

Los criterios que guían la decisión son:
- rendimiento bajo crecimiento de datos;
- facilidad de implementación;
- experiencia de usuario;
- costo de cambio;
- evidencia pendiente.

No se han definido benchmarks ni SLA aprobados, por lo que la decisión debe priorizar un diseño simple, trazable y compatible con el crecimiento real del volumen sin asumir requisitos no validados.

---

### Alternativas

#### 1. Paginación por offset
Se envían parámetros como page y limit, y el backend calcula offset a partir del número de página.

Ventajas:
- muy simple de implementar;
- fácil de probar y auditar;
- compatible con UI de navegación por páginas;
- útil cuando el usuario necesita “ir a la página N”.

Desventajas:
- puede degradar el rendimiento con grandes volúmenes si la paginación se mueve hacia páginas altas;
- la posición puede volverse inestable si se insertan o eliminan registros entre páginas;
- no es ideal cuando la colección crece muy rápido y la consulta se vuelve más intensiva.

#### 2. Paginación por cursor
Se usa un token o cursor estable, generalmente basado en un campo ordenable y único, por ejemplo created_at + id.

Ventajas:
- mejor comportamiento ante crecimiento de volúmenes grandes;
- más estable frente a cambios de datos entre páginas;
- evita saltos costosos en grandes colecciones.

Desventajas:
- más compleja de implementar y de auditar;
- requiere un diseño más cuidadoso de orden y de validación del cursor;
- la UX suele ser menos “navegación por página” y más “siguiente/previo”;
- puede requerir mayor esfuerzo de cambio si luego se quiere soportar una paginación más tradicional.

#### 3. Sin paginación / carga completa
Se devuelve todo el histórico del comercio en una sola respuesta.

Ventajas:
- implementación mínima.

Desventajas:
- incompatible con el requisito del PRD;
- mala experiencia de usuario;
- alto costo de memoria y respuesta;
- difícil de auditar y de controlar en crecimiento de datos.

---

### Decisión propuesta
Se adopta paginación por offset con orden determinista, priorizando simplicidad y trazabilidad sobre optimización máxima de volumen.

La estrategia propuesta es:
- usar parámetros explícitos de paginación, por ejemplo page y limit;
- ordenar siempre por una clave consistente y auditada, por ejemplo created_at desc y id desc;
- devolver metadata útil para la UI y la auditoría, como total, page, limit, hasNext;
- aplicar los filtros antes de paginar, con validación de rango de 90 días;
- mantener la respuesta con solo campos permitidos y sin datos sensibles.

Esta opción se considera la mejor decisión inicial porque responde directamente al PRD y reduce el riesgo técnico en una primera entrega, sin introducir complejidad de cursor o diseño de token que aún no tiene evidencia de necesidad.

---

### Consecuencias positivas
- Cumple con la obligación del PRD de que la consulta sea paginada.
- Es fácil de implementar en API, caso de uso y repositorio.
- Facilita auditoría y trazabilidad porque la página y el límite son claros y explícitos.
- Es intuitiva para usuarios y para pruebas de regresión.
- El costo de cambio es bajo si se requiere ajustar el límite o la UI en una etapa posterior.
- Permite validar con evidencia real la evolución del volumen de transacciones antes de decidir un cambio más sofisticado.

---

### Consecuencias negativas
- El rendimiento puede degradarse a medida que crecen los registros y el comercio avanza a páginas altas.
- La navegación por páginas puede volverse menos estable si hay inserciones frecuentes entre páginas.
- No es la opción más eficiente para colecciones muy grandes o con crecimiento acelerado.
- Puede requerir ajustes futuros si se observa que la consulta está afectando la latencia o la carga del repositorio.

---

### Evidencia pendiente
Antes de consolidar esta decisión como definitiva, falta evidenciar:
- volumen real de transacciones por comercio en el rango de 90 días;
- distribución esperada por páginas y por filtros;
- impacto real del ordenamiento y del cálculo de offset en el repositorio;
- complejidad de la auditoría del endpoint con la metadata devuelta;
- necesidad de una paginación más eficiente basada en cursor si el crecimiento del dato lo exige.

La evidencia pendiente no debe inventar benchmarks ni nuevos SLAs; debe basarse en mediciones reales del sistema y en la evolución del volumen observado.

---

### Condición de revisión
Este ADR debe revisarse si:
- el volumen de transacciones por comercio aumenta significativamente por encima del patrón observado;
- la paginación por offset impacta de manera relevante la latencia o la carga de consultas;
- se detecta una necesidad de auditoría más estricta que exija un ordenamiento o una trazabilidad más robusta;
- el producto define un límite de página o un comportamiento de navegación que haga necesario cambiar la estrategia.

En ese caso, se evaluará una transición hacia paginación por cursor, siempre con evidencia concreta y sin cambiar la intención del requisito funcional base.

---
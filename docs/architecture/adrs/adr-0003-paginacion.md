# ADR-0003 · Paginación con cursor para el endpoint de Historial de Transacciones

> **Escenario A del Lab 2** · versión de referencia canónica.
>
> **Fecha:** ago-2026
> **Estado:** Aprobado
> **Autor:** Equipo LegacyPay
> **Relacionado:** PRD Historial de Transacciones · Historia INVEST #3 (paginación)

---

## 1. Contexto

LegacyPay necesita exponer el endpoint `GET /api/v1/transacciones` que devuelve el historial de transacciones de un comercio para los últimos 90 días. En análisis de tráfico interno detectamos que:

- **Volumen esperado:** un comercio grande *(top 5% del portfolio)* procesa hasta **100.000 transacciones por trimestre**. En el rango de 90 días de consulta puede tener **~30.000-100.000 filas** que satisfacen los filtros.
- **Requisito de latencia del PRD (§5):** `p95 < 500ms` bajo carga de 100 req/s.
- **Uso previsto:** los comercios consultan el historial con paginación · típicamente navegan las primeras 5-10 páginas · pocos casos van a páginas profundas *(>50)*.
- **Restricción operacional:** la BD principal (Postgres 15) es compartida con el módulo de procesamiento en tiempo real · consultas costosas afectan la latencia de las operaciones críticas.

Con estos parámetros, la estrategia de paginación es una decisión con impacto directo en latencia · costo operacional · y experiencia del comercio.

## 2. Opciones evaluadas

### Opción A · OFFSET pagination *(clásica)*

```sql
SELECT * FROM transaccion
WHERE comercio_id = ? AND created_at BETWEEN ? AND ?
ORDER BY created_at DESC
LIMIT 50 OFFSET 500;
```

**Ventajas:**
- Simple de implementar · una línea SQL adicional
- Permite saltar directamente a "página N" *(útil para UI con paginador numerado)*
- Familiar para el equipo · no requiere capacitación

**Desventajas:**
- **Rendimiento degrada linealmente con el offset:** `OFFSET 10000` en Postgres tiene que leer y descartar 10.000 filas · latencia crece proporcionalmente
- Bajo carga alta con offsets profundos, es común ver `p95 > 2s` · **rompe el requisito del PRD**
- Riesgo de resultados inconsistentes si hay inserts concurrentes durante la paginación

### Opción B · CURSOR pagination *(basada en índice compuesto)*

```sql
SELECT * FROM transaccion
WHERE comercio_id = ? AND created_at BETWEEN ? AND ?
  AND (created_at, id) < (?, ?)  -- cursor de la página anterior
ORDER BY created_at DESC, id DESC
LIMIT 51;
```

**Ventajas:**
- **Rendimiento constante independiente de la profundidad** · paginar la página 1 o la 1000 tiene la misma latencia
- Cumple `p95 < 500ms` incluso con datasets grandes y offsets profundos
- Resultados consistentes ante inserts concurrentes *(el cursor es un punto fijo en el tiempo)*
- Alineado con las prácticas actuales de APIs REST modernas *(Stripe · GitHub · Twitter usan variantes de cursor)*

**Desventajas:**
- **No permite saltar a "página N":** solo next/prev · el frontend no puede mostrar "página 5 de 12"
- Requiere **índice compuesto** `(comercio_id, created_at DESC, id DESC)` · consume ~15% más de espacio en disco
- Si el orden cambia *(ej: usuario aplica filtro nuevo)* · el cursor previo se invalida · hay que regenerarlo

### Opción C · Keyset pagination *(variante académica de cursor)*

```sql
SELECT * FROM transaccion
WHERE comercio_id = ? AND id > ?
ORDER BY id
LIMIT 50;
```

**Ventajas:**
- Rendimiento constante *(similar a cursor)*
- Muy simple si el orden es siempre por PK

**Desventajas:**
- **NO soporta ordenamiento por `created_at DESC`** *(que es el orden requerido por el PRD)* · limitación estructural
- Menos flexible ante filtros combinados
- En la práctica es casi idéntico a cursor cuando se necesita ordenamiento personalizado

## 3. Decisión

**Adoptamos CURSOR pagination (Opción B)** sobre el índice compuesto `(comercio_id, created_at DESC, id DESC)`.

Formato del cursor: base64-encoded JSON con `{created_at: ISO8601, id: UUID}` de la última fila de la página anterior. El endpoint acepta el cursor como query param `cursor` y devuelve `next_cursor` en la respuesta.

## 4. Consecuencias

### Positivas

- ✅ **Latencia constante** independiente de la profundidad de paginación · cumple `p95 < 500ms` del PRD
- ✅ **Consistencia ante concurrencia:** los usuarios que paginan mientras se insertan nuevas transacciones no ven filas duplicadas ni saltadas
- ✅ **Escalabilidad:** un comercio con 100K+ transacciones tiene la misma UX que uno con 100 · no hay penalty por volumen
- ✅ **Alineado con la industria:** cuando los desarrolladores se enfrenten a APIs profesionales *(Stripe · GitHub · Twitter)* encontrarán el mismo patrón

### Negativas *(honestas · no minimizadas)*

- ❌ **No permite saltar a página N** · el frontend NO puede mostrar "página 5 de 12" · solo next/prev · limitación de UX que hay que comunicar a producto
- ❌ **Requiere índice compuesto adicional** · ocupa ~15% más de espacio en disco · requiere migración cuidadosa en tablas grandes
- ❌ **El cursor se invalida cuando cambia el orden** · si el usuario aplica un filtro nuevo mientras pagina · hay que regenerar el cursor · el frontend debe manejar esta condición explícitamente
- ❌ **Complejidad en debug:** un cursor es una string opaca · más difícil de leer en logs que un offset numérico · hay que loguear el cursor decodificado en modo debug
- ❌ **Casos de borde con timestamps duplicados:** si múltiples transacciones tienen exactamente el mismo `created_at`, el tie-breaker es `id` · sin él habría inconsistencias · el índice DEBE incluir `(created_at, id)` como par

## 5. Revisión

Esta decisión se revisará si se cumple alguna de estas condiciones:

- Los comercios reportan formalmente que **necesitan saltar directamente a páginas específicas** *(feature request con caso de uso claro · no preferencia)*
- La latencia `p95` supera **700ms bajo carga real de producción** durante 2 semanas consecutivas *(indicaría que el cursor no está resolviendo el problema para el que se eligió)*
- El equipo migra a otro RDBMS que no soporta índices compuestos eficientes *(escenario improbable pero posible)*
- Se identifica una alternativa emergente con mejor UX y rendimiento *(ej: feature nativa de Postgres para paginación optimizada)*

**Fecha de próxima revisión programada:** 6 meses desde la fecha de este ADR · o cuando se cumpla una condición de arriba.

---

## Referencias

- PRD Historial de Transacciones · Historia INVEST #3
- ERD · índice compuesto `idx_transaccion_comercio_created`
- Post técnico: *Use the Index, Luke · Pagination Done the PostgreSQL Way*
- Stripe API docs · pagination pattern *(referencia de industria)*
- **Adenda M1 · sesgo de popularidad:** sin este ADR · un dev futuro le pregunta a Claude *"¿cómo pagino?"* · Claude responde OFFSET (lo más popular en su corpus) · este ADR es el ancla que evita esa deriva

---

*ADR-0003 · Paginación por cursor · Escenario A · Historial de Transacciones · LegacyPay · Cohorte 2026-I · versión de referencia canónica.*

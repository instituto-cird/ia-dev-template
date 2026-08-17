# AI Usage Log

## Artefacto: PRD.md

Herramienta utilizada:
IA Generativa.

Uso realizado:
Se utilizó IA para apoyar la estructuración del documento de requisitos, organización de funcionalidades y definición de criterios de aceptación.

Validación humana:
Se revisaron los requisitos, restricciones de seguridad y alcance funcional antes de la implementación.


## Artefacto: ERD.md

Herramienta utilizada:
IA Generativa.

Uso realizado:
Se utilizó IA para proponer la estructura inicial del modelo entidad-relación del sistema.

Validación humana:
Se verificaron entidades, atributos y relaciones para mantener coherencia con los requisitos.


## Artefacto: ADR-001-ai-control.md

Herramienta utilizada:
IA Generativa.

Uso realizado:
Se utilizó IA para redactar una decisión arquitectónica relacionada con controles humanos y seguridad.

Validación humana:
Se revisó la decisión final y su alineación con buenas prácticas de desarrollo responsable con IA.


## Entrada 1 · Contrato Pydantic

Objetivo:
Generar los contratos de entrada y respuesta para la funcionalidad de soporte definida en el PRD.

Herramienta y modelo:
Asistente de IA.

Contexto proporcionado:
PRD de LegacyPay Support Assistant, incluyendo número de transacción, monto reclamado, motivo y control de operaciones críticas.

Salida inicial:
Se propusieron modelos Pydantic para validar los datos de entrada y estructurar la respuesta.

Problema detectado:
Las reglas relacionadas con autenticación, persistencia, identidad y estado externo no deben resolverse únicamente mediante Pydantic.

Corrección humana:
Se mantuvieron en el contrato únicamente las validaciones propias de los datos de entrada. Se utilizó Decimal para los montos y se configuró extra="forbid" para rechazar campos no definidos.

Evidencia:
Los tests de validación del contrato pasan correctamente.

Pregunta abierta:
La integración con persistencia y autenticación queda fuera del alcance de esta implementación.


## Entrada 2 · Tests

Objetivo:
Crear una suite pytest para validar el camino exitoso y los riesgos relevantes de la solicitud de soporte.

Herramienta y modelo:
Asistente de IA.

Contexto proporcionado:
Contrato SupportRequest, SupportService y riesgos definidos en el PRD.

Salida inicial:
Se propusieron tests para un camino exitoso, monto inválido y campos no definidos.

Problema detectado:
Un test que solamente verificara un valor configurado por un mock podría producir falsa confianza, porque podría validar el comportamiento del mock en lugar del comportamiento real de la implementación.

Corrección humana:
Se evitó mockear el método que se pretende probar. Los tests finales verifican directamente la validación del contrato y el comportamiento real de SupportService.

Evidencia:
La suite final contiene camino exitoso, validaciones de entrada y un escenario de solicitud de reembolso que debe permanecer en revisión. Actualmente pytest reporta 43 tests pasando.


## Entrada 3 · Refactor

Objetivo:
Separar responsabilidades entre la capa HTTP y la lógica de negocio sin modificar el comportamiento probado.

Herramienta y modelo:
Asistente de IA.

Contexto proporcionado:
La funcionalidad de soporte y el requisito del laboratorio de separar al menos dos responsabilidades.

Salida inicial:
Se propuso separar la recepción HTTP de la lógica de negocio mediante un Router y un Service.

Problema detectado:
Mantener la lógica de negocio directamente dentro del endpoint aumentaría el acoplamiento con FastAPI y dificultaría probarla de manera independiente.

Corrección humana:
Se creó un Router responsable de la capa HTTP y un SupportService responsable de crear la solicitud de soporte y establecer su estado inicial.

Evidencia:
El endpoint delega la operación en SupportService y la suite completa permanece en verde: 43 passed.

Justificación:
Se aplicó el patrón Service Layer. La separación reduce el acoplamiento entre HTTP y la lógica de negocio y permite probar SupportService de forma independiente. Se mantuvo una arquitectura pequeña y proporcional al alcance del laboratorio, sin agregar capas innecesarias.
## Evidencia U2.3 · Test generado por IA con falsa confianza

Test defectuoso identificado:
Se detectó un test que reemplazaba `SupportService.create_request()` por un lambda que devolvía directamente `"pending_review"` y luego verificaba ese mismo resultado.

Problema:
El test no ejecutaba la lógica real de `SupportService`. Por lo tanto, podía pasar aunque la implementación de `create_request()` estuviera rota. Esto producía falsa confianza.

Verificación realizada:
Se modificó deliberadamente el resultado del lambda a `"WRONG_BEHAVIOR"`. El test falló con una aserción que esperaba `"pending_review"`, demostrando que la prueba estaba verificando el mock y no el comportamiento real del servicio.

Corrección:
Se eliminó el reemplazo artificial del método y se construyó un `SupportRequest` real. El test ejecuta `SupportService.create_request(request)` y verifica `transaction_id`, `claimed_amount` y `status`.

Evidencia:
El test corregido pasó correctamente y la suite completa quedó en 44 tests passing.

Conclusión:
La prueba corregida aporta evidencia sobre el comportamiento real del servicio y no depende de configurar previamente el resultado que pretende verificar.

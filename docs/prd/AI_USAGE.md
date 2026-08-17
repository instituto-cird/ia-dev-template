# AI Usage Log

## Artefacto: PRD.md

Herramienta utilizada:
IA Generativa.

Uso realizado:
Se utilizó IA para apoyar la estructuración del documento de requisitos, organización de funcionalidades y definición de criterios de aceptación.

Validación humana:
Se revisaron los requisitos, restricciones de seguridad y alcance funcional antes de la entrega.


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
PRD de LegacyPay Support Assistant, incluyendo transacción, monto reclamado, motivo y control de operaciones críticas.

Salida inicial:
Se generaron modelos Pydantic para validar los datos de la solicitud y respuesta.

Problema detectado:
Las reglas relacionadas con identidad, persistencia o estado externo no deben resolverse únicamente mediante Pydantic.

Corrección humana:
Se mantuvieron en el contrato únicamente las validaciones propias de los datos de entrada.

Evidencia:
Los tests de validación pasan correctamente.

Pregunta abierta:
La integración con persistencia y autenticación queda fuera del alcance de esta implementación.


## Entrada 2 · Tests

Objetivo:
Crear una suite pytest para validar el camino exitoso y casos borde de la solicitud de soporte.

Herramienta y modelo:
Asistente de IA.

Contexto proporcionado:
Contrato SupportRequest y riesgos definidos en el PRD.

Salida inicial:
Se propusieron tests para un camino exitoso, monto inválido y campos no definidos.

Problema detectado:
Un test que simplemente verificara un valor configurado por un mock podría producir falsa confianza.

Corrección humana:
Se evitó mockear el método que se pretende probar y se verificó directamente el comportamiento del contrato y del servicio.

Evidencia:
La suite final ejecuta correctamente los casos definidos y pytest reporta 41 tests passing.


## Entrada 3 · Refactor

Objetivo:
Separar responsabilidades entre la capa HTTP y la lógica de negocio.

Herramienta y modelo:
Asistente de IA.

Contexto proporcionado:
La funcionalidad de soporte y el requisito de separar responsabilidades sin ampliar innecesariamente la arquitectura.

Salida inicial:
Se propuso separar Router y Service.

Problema detectado:
La lógica de negocio no debe quedar mezclada con la recepción de solicitudes HTTP.

Corrección humana:
Se creó SupportService para la lógica de negocio y un Router separado para manejar HTTP.

Evidencia:
El endpoint utiliza SupportService y la suite completa permanece en verde: 41 passed.

Justificación:
El patrón Service Layer reduce el acoplamiento entre HTTP y reglas de negocio y facilita probar la lógica de manera independiente, sin agregar una arquitectura innecesariamente compleja.
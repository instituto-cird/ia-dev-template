# ADR-001: Control humano sobre acciones críticas de IA

## Contexto

El sistema utiliza Inteligencia Artificial Generativa para asistir al equipo de soporte en el análisis de solicitudes de clientes.

Existe un riesgo al permitir que un modelo de IA ejecute directamente operaciones sensibles como reembolsos o modificaciones financieras.

## Decisión

La IA será utilizada únicamente para tareas de análisis, extracción de información y generación de propuestas.

Las operaciones críticas deberán ser ejecutadas por servicios del sistema que requieran autorización humana.

## Justificación

Esta decisión reduce riesgos de seguridad, evita acciones no autorizadas y mantiene la responsabilidad humana sobre decisiones importantes.

## Consecuencias

### Positivas

- Mayor control sobre operaciones financieras.
- Mejor trazabilidad de decisiones.
- Uso responsable de inteligencia artificial.

### Negativas

- Algunas operaciones requieren intervención manual.
- Puede aumentar el tiempo de resolución en ciertos casos.
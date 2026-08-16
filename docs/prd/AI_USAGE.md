# AI_USAGE — Lab 3

## Entrada 1 · Contratos

**Objetivo:**  
Generar el contrato Pydantic para el endpoint de consulta del historial de transacciones.

**Herramienta y modelo:**  
Chat de Visual Studio Code · modo Auto

**Contexto proporcionado:**  
Se proporcionó el archivo `docs/prd/PRD.md` junto con PROMPT-A · con Context Payload completo
#file:docs/prd/PRD.md
CONTEXTO:
Stack: Python 3.12 · FastAPI · Pydantic v2 · pytest
Clean Architecture · este archivo va en app/schemas/
TAREA:
Del PRD (Entidades e Historias), generá el modelo Pydantic v2
para el request de creación del endpoint.
REQUISITOS:
· Validaciones estrictas (EmailStr · Field(gt=0) · pattern regex)
· Comentarios que expliquen POR QUÉ cada validación
· Sin lógica de negocio (va en service · no en el schema)
RESTRICCIONES: solo código Python · sin datos reales · determinístico

**Salida inicial:**  
La IA generó un modelo Pydantic con los campos y validaciones del request.

**Problema detectado:**  
La salida inicial incluía un campo `email` que no formaba parte del contrato ni de las reglas de negocio definidas en el PRD.

**Corrección humana:**  
Eliminé el campo `email` y ajusté el schema para mantener únicamente los campos y validaciones respaldados por el PRD.

**Evidencia:**  
El contrato quedó alineado con el PRD y la suite de pruebas automatizadas continuó ejecutándose correctamente.

**Pregunta abierta:**  
¿Existen otros requisitos del PRD que deban incorporarse al contrato sin trasladar lógica de negocio al schema?
---

## Entrada 2 · Tests

**Objetivo:**  
Generar y fortalecer los tests del endpoint de historial de transacciones mediante TDD.

**Herramienta y modelo:**  
Chat de Visual Studio Code · modo Auto

**Contexto proporcionado:**  
Se proporcionaron el PRD y el schema Pydantic, junto con el
#file:docs/prd/PRD.md
#file:app/schemas/models.py
CONTEXTO:
Stack: Python 3.12 · FastAPI · Pydantic v2 · pytest · TestClient
El endpoint POST vivirá en app.main:app
TAREA:
Escribí 3 tests con TestClient, sin la implementación del endpoint:
1. Happy Path (201) · 2. Error 422 (Field inválido) · 3. Caso borde del PRD
REQUISITOS:
· Patrón AAA con comentarios (# Arrange · # Act · # Assert)
· Assert sobre COMPORTAMIENTO, no valor mockeado
RESTRICCIONES: sin datos reales · sin red · determinístico · solo Python

**Salida inicial:**  
La IA generó los tests iniciales del contrato y posteriormente, durante la auditoría, detectó que uno de los asserts agrupaba varios errores posibles y podía producir falsa confianza.

**Problema detectado:**  
Un test enviaba varios valores inválidos al mismo tiempo y aceptaba indistintamente un error en `estado` o `page_size`, por lo que no comprobaba exactamente qué regla estaba fallando. Además, faltaban pruebas de reglas del PRD como el límite de 90 días y el enmascarado del PAN.

**Corrección humana:**  
Separé las validaciones de `estado` y `page_size` en tests independientes con asserts específicos. Además, agregué un test para el límite máximo de 90 días y otro para verificar el enmascarado del PAN.

**Evidencia:**  
Los tests verifican ahora comportamientos específicos del contrato y reglas del PRD, manteniendo la suite en verde después de los cambios.

**Pregunta abierta:**  
¿Conviene incorporar posteriormente pruebas específicas para la paginación por cursor y el ordenamiento por fecha descendente?

---

## Entrada 3 · Refactor

**Objetivo:**  
Auditar la implementación generada durante el ciclo TDD e identificar mejoras de mantenimiento sin modificar innecesariamente la arquitectura.

**Herramienta y modelo:**  
Chat de Visual Studio Code · modo Auto

**Contexto proporcionado:**  
Se proporcionaron `app/routers/historial.py`, `app/services/historial_service.py`, `app/repositories/historial_repo.py` y `tests/test_historial.py`. Se indicó que los tests ya estaban en verde y se pidió una auditoría enfocada en asserts tautológicos, responsabilidades entre Service y Repository, validaciones duplicadas, imports o funciones sin uso y cobertura limitada al Happy Path. La IA debía devolver únicamente hallazgos y sugerencias, sin modificar archivos.

#file:app/routers/historial.py
#file:app/services/historial_service.py
#file:app/repositories/historial_repo.py
#file:tests/test_historial.py
CONTEXTO:
Acabo de implementar el endpoint GET /api/v1/transacciones con TDD asistido.
Los 3 tests pasan en verde.
TAREA:
Actuá como auditor de código. Buscá específicamente:
1. Si algún assert es tautológico o compara contra mock.return_value
2. Si el Service tiene lógica que debería estar en el Repository (o al revés)
3. Si hay validaciones duplicadas entre Pydantic y Service
4. Si hay imports o funciones que no se usan
5. Si algún test cubre solo el happy path
Devolvéme:
· Lista de hallazgos con severidad (alta · media · baja)
· Sugerencia concreta de corrección por cada hallazgo
· SIN escribir código todavía · solo auditoría
RESTRICCIONES: no modifiques archivos · solo reportá.

**Salida inicial:**  
La auditoría identificó oportunidades de mejora relacionadas con la separación de responsabilidades, posibles validaciones duplicadas, cobertura de pruebas e imports no utilizados.

**Problema detectado:**  
Se detectó un import (`timedelta`) que no era utilizado y se identificaron oportunidades para fortalecer la cobertura de pruebas y mejorar la organización del código. Algunas recomendaciones implicaban cambios arquitectónicos que excedían el alcance del laboratorio.

**Corrección humana:**  
Eliminé el import no utilizado y apliqué únicamente las mejoras alineadas con el alcance del laboratorio, fortaleciendo además la cobertura de pruebas mediante nuevos casos derivados del PRD. No implementé los refactors arquitectónicos sugeridos porque requerían cambios mayores que no estaban justificados para este ejercicio.

**Evidencia:**  
Luego de la limpieza, la implementación mantuvo el mismo comportamiento y la suite de pruebas continuó en verde.

**Pregunta abierta:**  
¿En una futura iteración conviene separar la transformación de salida, como el enmascarado del PAN, en un mapper o componente específico?
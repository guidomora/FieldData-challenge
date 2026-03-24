## Objetivo de trabajo para agentes

  Cualquier agente que trabaje en este repo debe priorizar:

  - código production-ready;
  - tipado estricto y consistente;
  - separación clara entre API, dominio, acceso a datos y jobs;
  - diseño mantenible y fácil de testear;
  - uso correcto de FastAPI moderno y Pydantic;
  - cambios pequeños, coherentes y bien justificados.

  ## Reglas de arquitectura

  Usar una estructura clara y predecible. Como guía general:

  - `app/api` para routers y dependencias web;
  - `app/core` para configuración, inicialización y cross-cutting concerns;
  - `app/models` para modelos ORM;
  - `app/schemas` para contratos Pydantic de request/response;
  - `app/repositories` para acceso a datos;
  - `app/services` para reglas de negocio;
  - `app/jobs` o `app/workers` para evaluación periódica de alertas;
  - `tests` para pruebas unitarias e integrales.

  Mantener la lógica de negocio fuera de los routers. Los endpoints deben orquestar validación de entrada, dependencias y códigos HTTP, no contener reglas de
  dominio complejas.

  El acceso a base de datos debe concentrarse en repositories o capas equivalentes. Evitar queries dispersas en routers o jobs.

  ## Convenciones FastAPI

  Seguir prácticas modernas de FastAPI:

  - Preferir `Annotated[...]` para parámetros y dependencias.
  - Declarar tipos de retorno o `response_model` explícitos en todos los endpoints.
  - No usar `...` / `Ellipsis` en modelos Pydantic ni en parámetros requeridos.
  - Definir `prefix`, `tags` y dependencias compartidas a nivel de router cuando aplique.
  - No mezclar múltiples operaciones HTTP en una sola función.
  - Usar `async def` solo cuando toda la cadena llamada sea realmente async y no bloqueante.
  - Si una operación usa librerías bloqueantes o código sync, preferir `def` o aislar correctamente el bloqueo.

  ## Reglas de tipado

  El tipado es un requisito de primera clase en este repositorio.

  - No usar `Any` salvo que esté estrictamente justificado.
  - Tipar explícitamente funciones públicas, métodos, variables relevantes y valores de retorno.
  - Tipar dependencias de FastAPI, repositories, services y jobs.
  - Modelar requests y responses con Pydantic de forma explícita.
  - Evitar diccionarios anónimos cuando corresponda un schema o un tipo bien definido.
  - Usar tipos específicos del dominio en lugar de estructuras genéricas cuando mejore claridad.
  - Mantener consistencia entre tipos ORM, schemas de entrada/salida y contratos de servicios.
  - Si una decisión de tipado requiere tradeoff, priorizar legibilidad, validación temprana y mantenibilidad.

  ## Dominio esperado

  El diseño debe contemplar al menos estas capacidades de dominio:

  - usuarios con alertas configurables;
  - campos o entidades equivalentes sobre los que se configuran alertas;
  - tipos de evento climático;
  - umbrales configurables por alerta;
  - datos meteorológicos futuros persistidos y consultables;
  - notificaciones generadas a partir de alertas disparadas;
  - prevención razonable de duplicados si el job corre periódicamente.

  Si falta una definición explícita del challenge, el agente debe hacer una propuesta simple, consistente y justificable, no sobrediseñar.

  ## Base de datos y migraciones

  - Diseñar esquemas normalizados y fáciles de extender.
  - Expresar restricciones de integridad de forma explícita.
  - Agregar índices cuando haya consultas periódicas o joins obvios del job evaluador.
  - Incluir migraciones funcionales y coherentes con el estado actual del modelo.
  - Evitar lógica crítica escondida únicamente en la aplicación si puede reforzarse con constraints de base.

  ## Background jobs

  El job de evaluación de alertas debe:

  - ser determinístico e idempotente en la medida de lo posible;
  - evitar generar notificaciones duplicadas ante re-ejecuciones;
  - separar claramente lectura de datos, evaluación de reglas y persistencia de resultados;
  - ser testeable sin depender de infraestructura externa;
  - documentar supuestos de frecuencia de ejecución y criterios de disparo.

  ## Testing

  Todo cambio relevante debe incluir tests.

  Priorizar:

  - tests unitarios de servicios y reglas de evaluación;
  - tests de integración de repositories y endpoints;
  - casos borde de umbrales, eventos inexistentes, alertas duplicadas y notificaciones repetidas;
  - pruebas sobre comportamiento asincrónico cuando aplique.

  Los tests deben ser claros, independientes y enfocados en comportamiento observable.

  ## Criterio de implementación

  Antes de agregar complejidad, elegir la solución más simple que cumpla bien el desafío. Evitar abstracciones prematuras, patrones innecesarios y
  sobreingeniería.

  Cuando haya varias alternativas válidas, preferir la que:

  - tenga mejores contratos de tipos;
  - sea más fácil de testear;
  - reduzca acoplamiento entre capas;
  - haga más explícitas las reglas de negocio;
  - sea más clara para otro desarrollador que retome el repo.

  ## Calidad de cambios

  Cada cambio debe dejar el código mejor que antes:

  - nombres precisos y consistentes;
  - funciones cortas y con una sola responsabilidad;
  - errores y validaciones con mensajes útiles;
  - sin lógica duplicada;
  - sin imports, modelos o endpoints muertos;
  - sin comentarios obvios o ruido innecesario.

  ## Documentación de API

  La API debe quedar correctamente documentada en Swagger/OpenAPI usando las capacidades nativas de FastAPI.

  - Todo endpoint debe tener `response_model` o tipo de retorno explícito.
  - Usar `summary`, `description`, `tags` y códigos de respuesta cuando aporten claridad real.
  - Documentar parámetros, bodies y errores esperables con schemas bien definidos.
  - Evitar endpoints “opacos” cuya intención solo se entienda leyendo la implementación.
  - La documentación generada en `/docs` debe ser suficiente para entender y probar el flujo principal sin leer el código.
  - Si una regla de negocio no es obvia, reflejarla en la descripción del endpoint o del schema correspondiente.

  Y dentro de las reglas generales cambiaría esta parte:

  Cualquier agente que trabaje en este repo debe priorizar:

  - código production-ready;
  - tipado estricto y consistente;
  - separación clara entre API, dominio, acceso a datos y jobs;
  - diseño mantenible y fácil de testear;
  - uso correcto de FastAPI moderno y Pydantic;
  - documentación clara de la API en Swagger/OpenAPI;
  - cambios pequeños, coherentes y bien justificados.

  Si un agente introduce una decisión importante de diseño, debe dejarla reflejada en README, docstring o comentario breve solo donde aporte contexto real.
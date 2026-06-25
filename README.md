# Simulador de Exámenes - Salesforce Identity & Access Management

Página web interactiva y responsiva para practicar el examen de certificación **Salesforce Certified Identity and Access Management Architect**.

## Características

✅ **141 preguntas únicas** de examen validadas  
✅ **Interfaz responsiva** (móvil, tablet, desktop)  
✅ **Preguntas aleatorias** con selección de cantidad  
✅ **Validación inmediata** de respuestas  
✅ **Explicaciones detalladas** en español para errores  
✅ **Estadísticas finales** por apartado (concepto)  
✅ **Desglose de aciertos/fallos** por tema  

## Contenido

- **132 preguntas únicas** del banco consolidado de 4 sets OCR deduplicados
- **9 preguntas adicionales** del material de estudio 2026 V2 (PDF)
- **Cobertura de 6 apartados**:
  - Accepting Third-Party Identity in Salesforce (21%)
  - Community (Partner and Customer) (18%)
  - Identity Management Concepts (17%)
  - Salesforce as an Identity Provider (17%)
  - Access Management Best Practices (15%)
  - Salesforce Identity (12%)

## Cómo usar

1. Abre `index.html` en tu navegador
2. Selecciona el número de preguntas que deseas practicar (5-141)
3. Haz clic en "Comenzar simulador"
4. Selecciona la(s) respuesta(s) correcta(s):
   - Preguntas de 1 opción: haz clic en el botón
   - Preguntas de múltiples opciones: marca los checkboxes y haz clic en "Comprobar selección"
5. Lee la explicación si es incorrecta
6. Continúa hasta terminar todas las preguntas
7. Revisa el resumen final con estadísticas por apartado

## Tecnología

- **HTML5** + **CSS3** (sin frameworks)
- **JavaScript vanilla** (sin dependencias)
- **JSON** para almacenamiento de preguntas
- Diseño totalmente responsivo con grid CSS

## Estructura de archivos

```
.
├── index.html          # Página principal del simulador
├── styles.css          # Estilos responsivos
├── app.js              # Lógica del simulador
├── questions.json      # Banco de 141 preguntas con respuestas
└── README.md           # Este archivo
```

## Formato de preguntas (JSON)

```json
{
  "id": 1,
  "concept": "Salesforce as an Identity Provider",
  "question": "...",
  "choices": [
    {"id": "A", "text": "..."},
    {"id": "B", "text": "..."}
  ],
  "correctAnswers": ["C"],
  "explanation": "...",
  "references": ["https://..."]
}
```

## Características de validación

- Detección automática de preguntas de selección única vs múltiple
- Enforcement de cardinalidad (número correcto de opciones según la pregunta)
- Ignorancia de mayúsculas en respuestas
- Deduplicación de opciones seleccionadas

## Estadísticas

Tras completar el simulador recibirás:

| Métrica | Descripción |
|---------|------------|
| % Total | Porcentaje de respuestas correctas |
| Aciertos/Fallos | Conteo por concepto |
| % por Apartado | Desempeño detallado por tema |

## Licencia

Uso educativo libre.

---

**Última actualización:** Junio 2026  
**Versión JSON:** 2 (141 preguntas validadas)

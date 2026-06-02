# Scania Predictive Maintenance Project

Proyecto de grado orientado a la priorizacion de mantenimiento predictivo para fallas en el sistema APS de camiones Scania.

## Objetivo

Desarrollar un pipeline reproducible que:

- caracterice el problema de fallas APS
- compare modelos de clasificacion en un contexto desbalanceado
- incorpore seleccion de caracteristicas
- incorpore validacion cruzada estratificada
- compare estrategias explicitas de manejo del desbalance
- incorpore costo de error y seleccion de umbral
- genere una salida de priorizacion util para apoyo a decisiones
- alimente un prototipo ligero de visualizacion

## Estructura principal

```text
complaints_thesis/
  app/
    scania_dashboard.py
  data/
    raw/
    processed/
  notebooks/
    scania_project_pipeline.ipynb
    scania_viability.ipynb
  reports/
    scania_project/
      figures/
      tables/
  requirements.txt
```

## Notebook principal

El notebook principal del proyecto es:

- `notebooks/scania_project_pipeline.ipynb`

Este notebook realiza:

- carga y caracterizacion del dataset
- seleccion de caracteristicas con Random Forest
- comparacion de modelos base y avanzados
- comparacion de manejo del desbalance con `class_weight` y `SMOTE`
- validacion cruzada estratificada
- evaluacion con metricas para clases desbalanceadas
- analisis de costo de error
- seleccion de umbral
- validacion con el conjunto de prueba oficial
- generacion de una tabla de priorizacion

## Fases del trabajo

El proyecto conserva dos ejercicios complementarios:

- `notebooks/scania_viability.ipynb`: fase exploratoria y de validacion inicial del tema
- `notebooks/scania_project_pipeline.ipynb`: fase metodologica consolidada y version principal del proyecto

## Prototipo

La aplicacion ligera del proyecto esta en:

- `app/scania_dashboard.py`

Permite visualizar:

- score de falla
- prioridad operativa
- accion recomendada
- comparacion de modelos
- resultados oficiales
- importancia de variables

## Requisitos

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Datos

Este repositorio no incluye los datasets crudos pesados.

Se espera que los archivos siguientes esten en `data/raw/`:

- `aps_failure_training_set.csv`
- `aps_failure_test_set.csv`
- `aps_failure_description.txt`

## Ejecucion del notebook

Abrir y ejecutar:

```text
notebooks/scania_project_pipeline.ipynb
```

Esto generara tablas y figuras en:

- `reports/scania_project/tables`
- `reports/scania_project/figures`

## Ejecucion del prototipo

```powershell
streamlit run app/scania_dashboard.py
```

## Estado actual

Actualmente el proyecto ya incluye:

- validacion del dataset
- seleccion de caracteristicas
- comparacion de modelos con validacion cruzada
- manejo explicito del desbalance con `SMOTE` y pesos de clase
- seleccion del modelo final de la fase consolidada
- calibracion de umbral por costo
- validacion en el test oficial
- salida de priorizacion para la capa de aplicacion
- prototipo ligero desplegable con Streamlit

## Siguiente trabajo

Los siguientes pasos naturales son:

- redaccion del informe tecnico
- interpretacion de variables con mayor contexto de dominio
- refinamiento del prototipo de apoyo a decision

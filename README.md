# Proyecto Final de KeepCoding: Liberando Productos

Este proyecto mejora una aplicación inicial de FastAPI con nuevas funcionalidades y una configuración completa de CI/CD, monitorización y alertas. Sigue los pasos a continuación para poner en marcha el proyecto y realizar el despliegue.

## Tabla de Contenidos

1. [Requisitos](#requisitos)  
2. [Estructura del Proyecto](#estructura-del-proyecto)  
3. [Configuración de la Aplicación](#configuración-de-la-aplicación)  
4. [Ejecución Local](#ejecución-local)  
5. [Dockerización](#dockerización)  
6. [Pruebas Unitarias](#pruebas-unitarias)  
7. [Monitorización y Alertas](#monitorización-y-alertas)  
8. [Pipeline de CI/CD](#pipeline-de-ci-cd)  

## Requisitos

Para ejecutar este proyecto, necesitas tener instalado:

- Python 3.11.8 o superior  
- `virtualenv`  
- Docker  
- Prometheus y Alertmanager  
- Acceso a una cuenta de Slack para configurar el canal de alertas  

Instala `virtualenv` con:

```bash
pip3 install virtualenv

## Configuración de la Aplicación

python3 -m venv venv
source venv/bin/activate

## Instala las dependencias especificadas en requirements.txt

pip3 install -r requirements.txt

# Ejecución Local
Para ejecutar el servidor FastAPI en tu máquina local:

Activa el entorno virtual:
source venv/bin/activate

Ejecuta el servidor
python3 src/application/app.py

# Dockerización

Para ejecutar la aplicación en Docker:

Construye la imagen Docker:
docker build -t simple-server:0.0.1 .

Ejecuta el contenedor Docker mapeando los puertos para Prometheus y FastAPI
docker run -d -p 8000:8000 -p 8081:8081 --name simple-server simple-server:0.0.1

Verifica que el servidor está corriendo
docker logs -f simple-server

# Pruebas Unitarias
Ejecuta todas las pruebas con cobertura:
pytest --cov

Para generar un reporte HTML de cobertura
pytest --cov --cov-report=html

# Monitorización y Alertas

Configura Prometheus editando prometheus/prometheus.yml:
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'simple-server'
    static_configs:
      - targets: ['localhost:8000']

Configura Alertmanager en prometheus/alertmanager.yml para enviar alertas a Slack
route:
  group_by: ['alertname']
  receiver: 'slack-notifications'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - send_resolved: true
        channel: '<nombre-del-canal>'
        text: '{{ .CommonAnnotations.summary }}'

# Prueba de Alertas

Para probar las alertas, realiza varias llamadas a los endpoints y verifica los contadores en la página de Prometheus en http://localhost:8000.

Pipeline de CI/CD
Este proyecto utiliza GitHub Actions para el pipeline de CI/CD. El archivo de configuración se encuentra en .github/workflows/ci_cd.yaml.

El pipeline incluye las fases de Testing y Build & Push.
Asegúrate de configurar los secretos en GitHub para acceder al contenedor de GitHub Container Registry (GHCR).
Configuración del Pipeline
El archivo ci_cd.yaml contiene la configuración del pipeline:
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t simple-server:${{ github.sha }} .
      - name: Push to GHCR
        run: docker push ghcr.io/<your-username>/simple-server:${{ github.sha }}

## Comprobación de Endpoints y Métricas

Prueba el endpoint /:
curl -X GET http://0.0.0.0:8081/

Prueba el endpoint /health:
curl -X GET http://0.0.0.0:8081/health

Prueba el nuevo endpoint /bye:
curl -X GET http://0.0.0.0:8081/bye

Métricas:

Accede a http://0.0.0.0:8000 para ver las métricas.
Verifica que los contadores aumentan al hacer llamadas a los endpoints.




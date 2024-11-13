from fastapi import FastAPI
from prometheus_client import Counter, start_http_server

app = FastAPI()

# Métricas Prometheus
server_requests_total = Counter('server_requests_total', 'Total number of requests to this webserver')
healthcheck_requests_total = Counter('healthcheck_requests_total', 'Total number of requests to healthcheck')
main_requests_total = Counter('main_requests_total', 'Total number of requests to main endpoint')
bye_requests_total = Counter('bye_requests_total', 'Total number of requests to bye endpoint')

# Endpoint principal
@app.get("/")
def read_root():
    main_requests_total.inc()
    server_requests_total.inc()
    return {"health": "ok"}

# Endpoint de salud
@app.get("/health")
def read_health():
    healthcheck_requests_total.inc()
    server_requests_total.inc()
    return {"message": "Hello World"}

# Nuevo endpoint /bye
@app.get("/bye")
def read_bye():
    bye_requests_total.inc()
    server_requests_total.inc()
    return {"msg": "Bye Bye"}

if __name__ == "__main__":
    # Inicia el servidor de Prometheus en el puerto 8000
    start_http_server(8000)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)

from fastapi import FastAPI
from .security import install_cors
from .routers import health, query, download
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Text2SQL API", version="0.1.0")

# Serve files in the 'web' folder at http://localhost:8000/ui
app.mount("/ui", StaticFiles(directory="../web", html=True), name="ui")


install_cors(app)
app.include_router(health.router)
app.include_router(query.router)
app.include_router(download.router)

@app.get("/")
def root():
    return {"ok": True}

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.logging import logger
from app.services.data_service import DataManager
from app.services.vector_engine import VectorEngine


# Lifecycle Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load Model and Data
    logger.info("Initializing System Resources...")
    try:
        DataManager.get_instance() # Force load data
        VectorEngine.get_instance() # Force load model
        logger.info("System Ready.")
    except Exception as e:
        logger.critical(f"System failed to initialize: {e}")
        raise e
    yield
    # Shutdown: Cleanup if needed
    logger.info("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Mount Configs
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/search", response_class=HTMLResponse)
async def handle_search_ui(
    request: Request,
    query: str = Form(...),
):
    try:
        engine = VectorEngine.get_instance()
        results = engine.search(query)
        return templates.TemplateResponse(
            request=request,
            name="results.html",
            context={"query": query, "results": results}
        )
    except Exception as e:
        logger.error(f"UI Search Error: {e}")
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "An error occurred while processing your request."}
        )

# API Endpoints
@app.get("/api/v1/search")
async def search_api(query: str):
    try:
        engine = VectorEngine.get_instance()
        results = engine.search(query)
        return JSONResponse(content={
            "query": query,
            "count": len(results),
            "results": results
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

if __name__ == "__main__":
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)

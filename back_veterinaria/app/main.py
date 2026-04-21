"""
Punto de entrada principal de la aplicación con arquitectura limpia
"""
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.presentation.api.routers import (
    auth,
    users,
    services,
    appointments,
    products,
    orders,
    adoptions,
    ai_chat,
    service_requests,
    pets,
    vet,
)
from app.core.exceptions import (
    DomainException,
    NotFoundException,
    ConflictException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException,
    BusinessRuleException
)

app = FastAPI(
    title="Veterinaria API",
    description="API REST para sistema de gestión veterinaria con arquitectura limpia",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
def _startup_ensure_service_catalog() -> None:
    from app.core.catalog_bootstrap import ensure_demo_services_rows

    ensure_demo_services_rows()


origins = list({settings.FRONTEND_URL, "http://localhost:5173", "http://127.0.0.1:5173"} | set(settings.BACKEND_CORS_ORIGINS))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    # «Servicio» inexistente es catálogo vacío / datos, no recurso de URL → 400
    code = status.HTTP_404_NOT_FOUND
    if (exc.details or {}).get("resource") == "Servicio":
        code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(
        status_code=code,
        content={"detail": exc.message, "type": "not_found"},
    )


@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message, "type": "conflict"}
    )


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message, "type": "unauthorized"},
        headers={"WWW-Authenticate": "Bearer"}
    )


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.message, "type": "forbidden"}
    )


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "type": "validation_error"}
    )


@app.exception_handler(BusinessRuleException)
async def business_rule_exception_handler(request: Request, exc: BusinessRuleException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "type": "business_rule_violation"}
    )


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message, "type": "domain_error"}
    )


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(services.router, prefix="/api/v1/services", tags=["Services"])
app.include_router(appointments.router, prefix="/api/v1/appointments", tags=["Appointments"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(adoptions.router, prefix="/api/v1/adoptions", tags=["Adoptions"])
app.include_router(ai_chat.router, prefix="/api/v1/ai", tags=["AI Chat"])
app.include_router(service_requests.router, prefix="/api/v1/service-requests", tags=["Service Requests"])
app.include_router(pets.router, prefix="/api/v1/pets", tags=["Pets"])
app.include_router(vet.router, prefix="/api/v1/vet", tags=["Veterinario"])

# Raíz del proyecto (back_veterinaria): StaticFiles exige que el directorio exista (p. ej. en Docker).
_project_root = Path(__file__).resolve().parent.parent
_uploads_dir = _project_root / "uploads"
_static_dir = _project_root / "static"
_uploads_dir.mkdir(parents=True, exist_ok=True)
_static_dir.mkdir(parents=True, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=str(_uploads_dir)), name="uploads")
app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")


@app.get("/")
async def root():
    return {
        "message": "Veterinaria API - Clean Architecture",
        "version": "2.0.0",
        "architecture": "Clean Architecture with SOLID principles",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "OK",
        "message": "Veterinaria API is running",
        "environment": settings.ENVIRONMENT,
        "architecture": "clean"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )

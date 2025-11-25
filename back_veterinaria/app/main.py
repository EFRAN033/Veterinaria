"""
Punto de entrada principal de la aplicación con arquitectura limpia
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.presentation.api.routers import auth, users, services, appointments, products, orders, adoptions, ai_chat
from app.core.exceptions import (
    DomainException,
    NotFoundException,
    ConflictException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException,
    BusinessRuleException
)

# Create FastAPI app
app = FastAPI(
    title="Veterinaria API",
    description="API REST para sistema de gestión veterinaria con arquitectura limpia",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers - Manejo centralizado de errores
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message, "type": "not_found"}
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


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(adoptions.router, prefix="/api/adoptions", tags=["Adoptions"])
app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Chat"])


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

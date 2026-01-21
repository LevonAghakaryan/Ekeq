from fastapi import APIRouter
from .home import router as home_router
from .catalog import router as catalog_router
from .product import router as product_router
from .invitation import router as invitation_router
from .admin import router as admin_router

# Գլխավոր router որը կմիավորի բոլորը
main_router = APIRouter()

# Միացնել բոլոր sub-router-ները
main_router.include_router(home_router, tags=["Home"])
main_router.include_router(catalog_router, tags=["Catalog"])
main_router.include_router(product_router, tags=["Product"])
main_router.include_router(invitation_router, tags=["Invitation"])
main_router.include_router(admin_router, prefix="/admin", tags=["Admin"])

__all__ = ["main_router"]
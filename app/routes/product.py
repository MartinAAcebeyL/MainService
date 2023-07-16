from fastapi import APIRouter, Depends, Response, Request
from app.models.product import Product
from app.models.productUser import ProductUser
from app.models.db import get_session


router = APIRouter(
    prefix="/api/v1", tags=["products"],
    responses={404: {"description": "Not found"}})


@router.get("/products")
async def get_products(db=Depends(get_session)):
    products = db.query(Product).all()
    return {"products": products}


@router.post("/products/{product_id}/like")
async def create_product(product_id: int, request: Request, db=Depends(get_session)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return Response({
            "message": "Product not found",
        }, status_code=404)
    user_id = request.body().get("user_id")
    product_user = ProductUser(product_id=product_id, user_id=user_id)
    db.add(product_user)
    db.commit()
    return Response({
        "message": "Product liked",
    }, status_code=200)

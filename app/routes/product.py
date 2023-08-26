from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from app.models.product import Product
from app.models.productUser import ProductUser
from app.models.db import get_session
from producer import publish
from fastapi.encoders import jsonable_encoder
import requests

router = APIRouter(
    prefix="/api/v1/products", tags=["products"],
    responses={404: {"description": "Not found"}})


@router.get("/")
async def get_products(db=Depends(get_session)):
    products = db.query(Product).all()
    return {"products": products}


@router.post("/{product_id}/like")
async def create_product(product_id: int, db=Depends(get_session)):

    url = "http://backendadminservice:8000/api/v1/clients/"
    try:
        req = requests.get(url)
        product_user = ProductUser(
            user_id=req.json()['id'], product_id=product_id)
        db.add(product_user)
        db.commit()
        db.refresh(product_user)
        serialized_product_user = jsonable_encoder(product_user)
        publish('product_liked', product_id)
        return JSONResponse(status_code=201, content={"message": "sucess",
                                                      "product_user": serialized_product_user})
    except requests.exceptions.RequestException as e:
        return Response(status_code=404, content="error")
    except Exception as e:
        return Response(status_code=404, content="error")

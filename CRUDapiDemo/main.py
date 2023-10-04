from typing import Annotated
from sqlalchemy.sql import func
from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy.testing import db
from starlette import status
from database import engine, SessionLocal
import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def first_highest_id_record(dbSession: Session = Depends(get_db)):
    r = dbSession.query(func.max(models.Product.id)).first()
    return r


@app.get('/')
async def test():
    return 'Hello welcome to my CRUD API Demo'


@app.get('/product', status_code=status.HTTP_200_OK)
async def read_all_product(dbSession: Session = Depends(get_db)):
    products = dbSession.query(models.Product).all()
    return products


@app.get('/product/{product_id}', status_code=status.HTTP_200_OK)
async def read_product_by_id(product_id: int = Path(gt=0), dbSession: Session = Depends(get_db)):
    products = dbSession.query(models.Product).filter(models.Product.id == product_id).all()
    return  products


@app.post('/product', status_code=status.HTTP_201_CREATED)
async def create_product(product: models.ProductRequest, dbSession: Session = Depends(get_db)):
    p = dbSession.query(models.Product).order_by(models.Product.id.desc()).first()
    maxId= 1
    if p is not None:
        maxId=p.id

    p = models.Product()
    p.id=maxId+1
    p.name=product.name
    p.description=product.description
    p.price_per_unit=product.price_per_unit
    p.base_unit=product.base_unit
    p.stock=product.stock
    dbSession.add(p)
    dbSession.commit()
    return p


@app.put('/product', status_code=status.HTTP_204_NO_CONTENT)
async def update_product(product_request: models.ProductRequest, dbSession: Session = Depends(get_db)):
    p = dbSession.query(models.Product).filter(models.Product.id == product_request.id).first()
    if p is None:
        raise HTTPException(status_code=404, detail='Product not Found')
    p.id = product_request.id
    p.name = product_request.name
    p.description = product_request.description
    p.price_per_unit = product_request.price_per_unit
    p.base_unit = product_request.base_unit
    p.stock = product_request.stock
    dbSession.add(p)
    dbSession.commit()


@app.delete('/product', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int = Query(gt=0), dbSession: Session = Depends(get_db)):
    p = dbSession.query(models.Product).filter(models.Product.id == product_id).first()
    if p is None:
        raise HTTPException(status_code=404, detail='Product not Found')
    dbSession.query(models.Product).filter(models.Product.id == product_id).delete()
    dbSession.commit()



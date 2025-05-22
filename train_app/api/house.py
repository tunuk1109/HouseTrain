
from train_app.db.models import House
from train_app.db.schema import HouseSchema
from train_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import  List
from fastapi import Depends, HTTPException, APIRouter, status
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


house_router = APIRouter(prefix='/house', tags=['House'])

BASE_DIR = Path(__file__).resolve().parent.parent.parent

model_path = BASE_DIR / 'house_price_model_job.pkl'
scaler_path = BASE_DIR / 'scaler.pkl'

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@house_router.post('/', response_model=HouseSchema)
async def create_house(house: HouseSchema, db: Session = Depends(get_db)):
    house_db = House(**house.dict())

    db.add(house_db)
    db.commit()
    db.refresh(house_db)
    return house_db

@house_router.get('/', response_model=List[HouseSchema])
async def house_list(db: Session = Depends(get_db)):
    house_db = db.query(House).all()
    return house_db

@house_router.get('/house_id', response_model=HouseSchema)
async def house_detail(house_id: int, db: Session = Depends(get_db)):
    house_db = db.query(House).filter(House.id == house_id).first()
    if house_db is None:
        raise HTTPException(status_code=404, detail='Thus house not find')
    return house_db

@house_router.put('/house_id', response_model=HouseSchema)
async def house_update(house_id: int, house: HouseSchema, db: Session = Depends(get_db)):
    house_db = db.query(House).filter(House.id == house_id).first()
    if house_db is None:
        raise HTTPException(status_code=404, detail='Thus house not find')

    for house_key, house_value in house.dict().items():
        setattr(house_db, house_key, house_value)

    db.add(house_db)
    db.commit()
    db.refresh(house_db)
    return house_db

@house_router.delete('/house_id')
async def house_delete(house_id: int, db: Session = Depends(get_db)):
    house_db = db.query(House).filter(House.id == house_id).first()
    if house_db is None:
        raise HTTPException(status_code=404, detail='This house not find')

    db.delete(house_db)
    db.commit()
    return {'message': 'This house is deleted'}


model_columns = [
    'GrLivArea',
    'YearBuilt',
    'GarageCars',
    'TotalBsmtSF',
    'FullBath',
    'OverallQual'
]

@house_router.post('/predict/')
async def predict_price(house: HouseSchema, db: Session = Depends(get_db)):
    input_data = {
        'GrLivArea': house.GrLivArea,
        'YearBuilt': house.YearBuilt,
        'GarageCars': house.GarageCars,
        'TotalBsmtSF': house.TotalBsmtSF,
        'FullBath': house.FullBath,
        'OverallQual': house.OverallQual
    }
    input_df = pd.DataFrame([input_data])
    scaler_dr = scaler.transform(input_df)
    predicted_price = model.predict(scaler_dr)[0]
    return {'predicted_price' : round(predicted_price)}

















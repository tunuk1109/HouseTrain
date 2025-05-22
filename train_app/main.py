from fastapi import FastAPI
from train_app.api import auth, house
import uvicorn


train_app = FastAPI(title='House')

train_app.include_router(auth.auth_router)
train_app.include_router(house.house_router)


if __name__ == '__main__':
    uvicorn.run(train_app, host='127.0.0.1', port=8000)

from fastapi import FastAPI
from authentication.database import Base, engine
from routes.users import router

app = FastAPI(debug=True)

Base.metadata.create_all(bind=engine)

app.include_router(router)
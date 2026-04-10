from fastapi import FastAPI
from project1.database import Base, engine
from project1.routes.users import router
from project1.routes.tasks import router as tasks_router

app = FastAPI(debug=True)

Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(tasks_router)
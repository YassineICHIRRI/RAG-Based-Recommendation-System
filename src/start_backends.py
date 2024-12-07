from fastapi import FastAPI

from src.backends.api import router


app = FastAPI()
app.include_router(router=router)




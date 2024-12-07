from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1", 
    tags = ["api_v1",]
)


@router.post("/hello")
def hello_endpoint():
    return "Hello"
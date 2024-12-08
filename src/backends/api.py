from fastapi import APIRouter, Request

from .save_records import save_news_records
from .mongodb import select_all_from_mongodb


router = APIRouter(
    prefix="/api/v1", 
    tags = ["api_v1",]
)


@router.post("/save-records/{collection_name}")
async def save_news_records_endpoint(request: Request, collection_name: str = "almassa_news"):
    """
        Save records in mongodb and vectore store (ChrombDB)
    """
    return await save_news_records(
        request=request, collection_name=collection_name
    )


@router.get("/select-all-mongo/{collection_name}")
def select_all_from_mongodb_endpoint(collection_name: str = "almassa_news"):

    return select_all_from_mongodb(collection_name=collection_name)

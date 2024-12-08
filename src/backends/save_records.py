from fastapi import Request
from fastapi.encoders import jsonable_encoder
from src import configs

from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import uuid


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512, chunk_overlap=40, length_function=len, is_separator_regex=False
)

embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def save_records_mongo(
    collection_name: str, json_data: list[dict]
):
    conn = configs.get_connection()

    db = conn["news"]

    collection = db[collection_name]

    uuids_list = [str(uuid.uuid4()) for _ in range(len(json_data))]

    json_data = [
        {   "news_id": uuids_list[i],
            "title": data["title"],
            "content": data["content"],
            "metadata": {
                **{key: data[key] for key in data if key not in ("title", "content")},
            }
        } for i, data in enumerate(json_data)
    ]

    collection.insert_many(jsonable_encoder(json_data))

    return uuids_list


def docs_split_and_create_embeddings_save_vecdb(collection_name: str, json_data, uuids_list: list[str]):

    docs = [
        Document(
            page_content="\n".join([data["title"], data["content"]]),
            metadata= {
                "source": {
                    "db": "news",
                    "collection": collection_name,
                    "news_id": uuids_list[i]
                },
                # **{key: data[key] for key in data if key not in ("title", "content")},
            }
        ) 
        for i, data in enumerate(json_data)
    ]

    chunks = text_splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        documents=filter_complex_metadata(chunks), embedding=embedder, persist_directory=str(configs.vecdb_path)
    )
    vector_store.persist()

    # vector_store = Chroma(persist_directory=str(configs.vecdb_path), embedding_function=embedder)

    # retriever = vector_store.as_retriever(
    #     search_type="similarity_score_threshold",
    #     search_kwargs={
    #         "k": 20,
    #         "score_threshold": 0.1,
    #     },
    # )

    # res = retriever.invoke("عرض للقفطان")


async def save_news_records(request: Request, collection_name: str):

    json_data = await request.json()

    uuids_list = save_records_mongo(
        collection_name=collection_name, json_data=json_data
    )

    docs_split_and_create_embeddings_save_vecdb(
        collection_name=collection_name, json_data=json_data, uuids_list=uuids_list
    )

    return {
        "message": "News received successfully",
    }
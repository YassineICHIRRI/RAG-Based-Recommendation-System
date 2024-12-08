# RAG-Based-Recommendation-System


create a virtualenv :

```
conda create rag-recsys python=3.11.10
```

```
conda activate rag-recsys
```

Install requirements

```
pip install -r requirements.txt
```

start backend server 

```
uvicorn src.start_backends:app --reload
```

# TODO: 

:white_check_mark: Create `save-records` endpoint, which will charge of two things, add `records` (scraped news) to mongodb as well as vector store.
:white_check_mark: Create `select-all-mongo` that given `collection_name`, fetch that data from mongodb.
:white_large_square: Create `get-recommendations` that accepts as body: `title` and recommned news that are similar to this.
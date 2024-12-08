from pathlib import Path
from dataclasses import dataclass
import pymongo

base_dir = Path(__file__).parent.parent

base_url = "http://localhost:8000/api/v1"

vecdb_path = base_dir / "db"
vecdb_path.mkdir(exist_ok=True)


@dataclass
class MongoConfigs:
    host: str = "localhost"
    port: int = 27017

news_db = "news"


def get_connection():

    mongo_configs = MongoConfigs()
    return pymongo.MongoClient(
        mongo_configs.host, mongo_configs.port
    )
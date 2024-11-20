from src.mongodb import NewsClient



client = NewsClient(collection_name="sabah")

client.clear()

# client.insert({
#     "title": "sabah",
#     "body": "sabah body"
# })

# res = client.find({})

# for doc in res:
#     print(doc)

# client.clear()
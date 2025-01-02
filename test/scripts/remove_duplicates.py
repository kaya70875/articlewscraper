from pymongo import MongoClient, errors

def remove_duplicates(mongo_uri, mongo_db, collection_name, unique_field, batch_size=1000):
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[collection_name]

    # Step 1: Identify duplicates in batches
    last_id = None
    duplicates_removed = 0

    while True:
        query = {}
        if last_id:
            query["_id"] = {"$gt": last_id}

        cursor = collection.find(query, {unique_field: 1}).sort("_id").limit(batch_size)
        batch = list(cursor)

        if not batch:
            break

        ids = [doc["_id"] for doc in batch]
        last_id = ids[-1]

        pipeline = [
            {"$match": {"_id": {"$in": ids}}},
            {"$group": {
                "_id": f"${unique_field}",
                "count": {"$sum": 1},
                "docs": {"$push": "$_id"}
            }},
            {"$match": {
                "count": {"$gt": 1}
            }}
        ]

        try:
            duplicates = list(collection.aggregate(pipeline))
        except errors.OperationFailure as e:
            print(f"Aggregation failed: {e.details}")
            client.close()
            return

        # Step 2: Remove duplicates
        for duplicate in duplicates:
            # Keep one document and remove the rest
            ids_to_remove = duplicate["docs"][1:]
            collection.delete_many({"_id": {"$in": ids_to_remove}})
            duplicates_removed += len(ids_to_remove)

    client.close()
    print(f"Removed {duplicates_removed} duplicate documents from the collection.")

if __name__ == "__main__":
    mongo_uri = "mongodb+srv://kaya70875:PqVLhzC3Txm6ZJpD@mern.8pqqmzg.mongodb.net/?retryWrites=true&w=majority&appName=mern"
    mongo_db = "learn-with-articles"
    collection_name = "sentences"
    unique_field = "text"

    remove_duplicates(mongo_uri, mongo_db, collection_name, unique_field)
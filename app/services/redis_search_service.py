import redis
from redisearch import Client, TextField, NumericField, TagField, IndexDefinition, Query

class RedisSearchService:
    def __init__(self, host="localhost", port=6379):
        self.redis_connection = redis.Redis(host=host, port=port, decode_responses=True)

    def create_index(self, index_name: str, fields: list):
        client = Client(index_name, conn=self.redis_connection)

        redis_fields = []
        for f in fields:
            ftype = f["type"].lower()
            if ftype == "text":
                redis_fields.append(TextField(
                    f["name"],
                    sortable=f.get("sortable", False),
                    weight=f.get("weight", 1.0)
                ))
            elif ftype == "numeric":
                redis_fields.append(NumericField(
                    f["name"],
                    sortable=f.get("sortable", False)
                ))
            elif ftype == "tag":
                redis_fields.append(TagField(
                    f["name"],
                    sortable=f.get("sortable", False)
                ))
            else:
                raise ValueError(f"Unsupported field type: {f['type']}")

        try:
            client.create_index(
                redis_fields,
                definition=IndexDefinition(
                    prefix=[f"{index_name.lower()}:"]
                )
            )
        except Exception as e:
            if "Index already exists" in str(e):
                return {"message": f"Index '{index_name}' already exists"}
            raise e

        return {"message": f"Index '{index_name}' created successfully"}

    def add_document(self, index_name: str, document_id: str, fields: dict):
        client = Client(index_name, conn=self.redis_connection)
        try:
            client.redis.hset(f"{index_name}:{document_id}", mapping=fields)
            return {
                "message": f"Document '{document_id}' indexed successfully",
                "key": f"{index_name}:{document_id}"
            }
        except Exception as e:
            return {"error": str(e)}
 
    def search_documents(self, index_name: str, term: str, limit: int = 10, offset: int = 0):
        client = Client(index_name, conn=self.redis_connection)
        try:
            # Escape the term to avoid syntax issues
            safe_term = term.replace("-", "\\-").replace(":", "\\:")

            # Create a RediSearch query that matches the term anywhere
            query = Query(safe_term).paging(offset, limit).with_scores()

            results = client.search(query)

            docs = []
            for doc in results.docs:
                docs.append({
                    "id": doc.id,
                    "fields": {k: v for k, v in doc.__dict__.items() if not k.startswith("__")},
                    "score": doc.score
                })

            return {
                "total": results.total,
                "documents": docs
            }
        except Exception as e:
            return {"error": str(e)}
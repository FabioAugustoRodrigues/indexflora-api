from redisearch import Client, TextField, NumericField, TagField, IndexDefinition, Query
import redis

from fastapi import HTTPException

import re

class RedisSearchClient:
    def __init__(self, host="redis", port=6379):
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
                raise HTTPException(status_code=400, detail=f"Unsupported field type: {f['type']}")

        try:
            client.create_index(
                redis_fields,
                definition=IndexDefinition(
                    prefix=[f"{index_name.lower()}:"]
                )
            )
        except Exception as e:
            if "Index already exists" in str(e):
                raise HTTPException(status_code=409, detail=f"Index '{index_name}' already exists")
            raise HTTPException(status_code=500, detail=str(e))

    def add_document(self, index_name: str, document_id: str, fields: dict):
        client = Client(index_name, conn=self.redis_connection)
        try:
            client.redis.hset(f"{index_name}:{document_id}", mapping=fields)

            return f"{index_name}:{document_id}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
 
    def escape_term(self, term: str) -> str:
        """Escape special characters in RediSearch queries."""
        return re.sub(r'([\-@|*~:])', r'\\\1', term)

    def search_documents(self, index_name: str, term: str, limit: int = 10, offset: int = 0):
        client = Client(index_name, conn=self.redis_connection)
        try:
            # Split term into words and escape each
            terms = [self.escape_term(t) + "*" for t in term.strip().split()]

            # Combine terms with OR to match any word
            query_str = " | ".join(terms)

            # Create query with pagination and scores
            query = Query(query_str).paging(offset, limit).with_scores()
            results = client.search(query)

            # Build document list
            docs = [
                {
                    "id": doc.id,
                    "fields": {k: v for k, v in doc.__dict__.items() if not k.startswith("__") and k not in ["id", "score"]},
                    "score": doc.score
                }
                for doc in results.docs
            ]

            return {
                "total": results.total,
                "documents": docs
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
import redis
from redisearch import Client, TextField, NumericField, TagField, IndexDefinition

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

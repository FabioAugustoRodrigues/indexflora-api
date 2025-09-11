import json

class SchemaValidatorService:
    @staticmethod
    def validate(document: dict, schema_fields):
        expected_field_names = [f["name"] for f in schema_fields]

        extra_fields = [k for k in document.keys() if k not in expected_field_names]
        missing_fields = [name for name in expected_field_names if name not in document]

        return extra_fields, missing_fields


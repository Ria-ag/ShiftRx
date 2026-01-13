from jsonschema import validate, ValidationError
import json

def validate_icr(output):
    schema = json.load(open("icr.schema.json"))
    
    try:
        validate(instance=output, schema=schema)
        print("Validation successful!")
        return True
    except ValidationError as e:
        print("Validation failed:")
        print(f"  Error: {e.message}")
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        print(f"  Schema path: {' -> '.join(str(p) for p in e.schema_path)}")
        raise
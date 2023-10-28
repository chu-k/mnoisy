from pathlib import Path
from typing import Any, Dict, Optional

import jsonschema
import yaml


def load_schema_yaml(schema_path: Path) -> Dict[str, Any]:
    with open(schema_path, "r") as schema_fp:
        return yaml.safe_load(schema_fp)


def validate_against_schema(input_data: dict, schema_path: Path, sub_schema: Optional[str] = None) -> None:
    """Validate the schema."""
    try:
        schema = load_schema_yaml(schema_path)
        schema = schema.get(sub_schema, {}) if sub_schema else schema
    except KeyError:
        raise KeyError(f"Schema {schema_path} does not contain nested schema {sub_schema}")
    try:
        jsonschema.validate(input_data, schema)
    except jsonschema.ValidationError as e:
        raise e

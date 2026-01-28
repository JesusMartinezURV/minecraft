import jsonschema
from jsonschema import FormatChecker, validate

message_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "source", "target", "timestamp"],
    "properties": {
        "type": {"type": "string"},
        "source": {"type": "string"},
        "target": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "payload": {
            "anyOf": [
                {
                    "type": "array",
                    "items": {"type": "string"}
                },
                {
                    "type": "object"
                }
            ]
        },
        "status": {"enum": ["SUCCESS", "FAILED"]},
        "context": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}


def validate_message(message):
    """Return True when a message matches the schema; False otherwise."""
    try:
        validate(instance=message, schema=message_schema, format_checker=FormatChecker())

        if message.get("source") == message.get("target"):
            raise ValueError("Source and target cannot be the same")

        return True

    except (jsonschema.exceptions.ValidationError, ValueError):
        return False
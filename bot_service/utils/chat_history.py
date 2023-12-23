import json

from vertexai.preview.generative_models import Content


def to_json(history: list[Content]):
    """
    Converts a history from ChatSession to a list of JSON strings.
    Will be saved in Google Firestore.
    """
    if not history:
        return []
    return [json.dumps({c.role: c.text}, ensure_ascii=False) for c in history]


def from_json(input: list[str]):
    """
    Converts list of JSON objects to the list of Content objects.
    Passed as an input to Gemini-Pro model.
    """
    if not input:
        return []
    result = []
    for item in input:
        obj = json.loads(item)
        key = list(obj.keys())[0]
        result.append(
            Content.from_dict({"role": key, "parts": [{"text": obj.get(key)}]})
        )
    return result

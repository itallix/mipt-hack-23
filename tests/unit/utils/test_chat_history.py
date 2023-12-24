from vertexai.preview.generative_models import Content

from bot_service.utils.chat_history import from_json, to_json

history = [
    Content.from_dict(
        {
            "role": "user",
            "parts": [{"text": "Hello!"}],
        }
    ),
    Content.from_dict(
        {
            "role": "model",
            "parts": [{"text": "Hi!"}],
        }
    ),
]

json_history = ['{"user": "Hello!"}', '{"model": "Hi!"}']


def test_convert_to_json():
    assert to_json(None) == []
    assert to_json([]) == []
    assert to_json(history) == json_history


def test_convert_from_json():
    assert from_json(None) == []
    assert from_json([]) == []
    actual = from_json(json_history)
    assert len(actual) == len(history)
    for idx, content in enumerate(actual):
        assert actual[idx].role == history[idx].role
        assert actual[idx].text == history[idx].text

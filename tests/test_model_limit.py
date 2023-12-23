import time

import pytest
from vertexai.preview.generative_models import GenerativeModel


@pytest.mark.skip(reason="Long running test, disabled by default")
def test_limit():
    model = GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    for _ in range(100):
        chat.send_message("Расскажи сказку")
        print(chat.history)
        time.sleep(0.5)

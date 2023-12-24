from typing import Any

import pytest
from vertexai.preview.generative_models import GenerativeModel


@pytest.fixture(scope="session")
def model() -> GenerativeModel:
    return GenerativeModel("gemini-pro-vision")


@pytest.fixture()
def context() -> Any:
    class Context(object):
        pass

    return Context()

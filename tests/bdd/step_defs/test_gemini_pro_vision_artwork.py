from pytest_bdd import given, parsers, scenarios, then, when
from vertexai.preview.generative_models import GenerationConfig, Image

scenarios("../features/gemini_pro_vision_artwork.feature")


PREFIX = "Give me response in format: "
PAINTING_PROMPT = PREFIX + "author fullname - painting name"
LANDMARK_PROMPT = PREFIX + "city - landmark name"


@given(parsers.parse('The painting "{name}"'))
def painting(context, name):
    context.prompt = PAINTING_PROMPT
    with open(f"tests/bdd/data/paintings/{name}", "rb") as f:
        context.image = Image.from_bytes(f.read())


@given(parsers.parse('The landmark "{name}"'))
def landmark(context, name):
    context.prompt = LANDMARK_PROMPT
    with open(f"tests/bdd/data/landmarks/{name}", "rb") as f:
        context.image = Image.from_bytes(f.read())


@when("Gemini Pro Vision triggered")
def gemini_pro_vision_triggered(model, context) -> None:
    response = model.generate_content(
        [context.image, context.prompt],
        generation_config=GenerationConfig(temperature=0.1, top_k=1, top_p=1),
    )
    context.response = response.text


@then(parsers.parse('The model response should match "{expected}"'))
def check_response(context, expected) -> None:
    assert expected == context.response.strip()

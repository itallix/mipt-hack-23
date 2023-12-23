from bot_service.utils.markdown import markdown_to_text


def test_convert_markdown_to_text():
    text = "## Title\n **caption**"
    assert markdown_to_text(text) == "Title\ncaption"

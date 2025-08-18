import pytest
from unittest.mock import MagicMock

from threat_modeling_bot import main


@pytest.fixture
def mock_openai(mocker):
    """Fixture to mock the OpenAI API call."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "# Mocked Threat Model Report"

    mock_create = mocker.patch("openai.ChatCompletion.create")
    mock_create.return_value = mock_response
    return mock_create


def test_generate_threat_model(mock_openai):
    """
    Tests the generate_threat_model function to ensure it formats the prompt
    and calls the OpenAI API correctly.
    """
    architecture = "## Test Architecture"
    prompt_template = "Analyze this: {user_architecture}"

    result = main.generate_threat_model(architecture, prompt_template)

    # Check that the result is what we mocked
    assert result == "# Mocked Threat Model Report"

    # Check that the API was called with the correctly formatted prompt
    mock_openai.assert_called_once()
    called_args, called_kwargs = mock_openai.call_args
    final_prompt = called_kwargs["messages"][-1]["content"]
    assert "Analyze this: ## Test Architecture" in final_prompt
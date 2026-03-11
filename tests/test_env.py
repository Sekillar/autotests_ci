import os


def test_env_variables_exist():
    base_url = os.getenv("BASE_URL")
    api_token = os.getenv("API_TOKEN")

    assert base_url is not None, "BASE_URL is not set"
    assert api_token is not None, "API_TOKEN is not set"

import os
import pytest
from dotenv import load_dotenv
from clients.base_client import ApiClient

load_dotenv()


@pytest.fixture
def get_token():
    client = ApiClient()
    try:
        response = client.post(
            path='/login',
            data={
                "username": os.getenv('USER'),
                "password": os.getenv('PASSWORD')
            }
        )
        yield response
    finally:
        del client

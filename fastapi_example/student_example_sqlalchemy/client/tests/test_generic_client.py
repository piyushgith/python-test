import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

import pytest
from unittest.mock import Mock, patch
import requests
from pydantic import BaseModel
from ..client.generic_client import GenericAPIClient


# Test Model
class TestModel(BaseModel):
    id: int
    name: str
    value: str


# Fixtures
@pytest.fixture
def base_url():
    return "http://test-api.com/resources"


@pytest.fixture
def test_headers():
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def client(base_url, test_headers):
    return GenericAPIClient(
        base_url=base_url,
        model_class=TestModel,
        headers=test_headers
    )


@pytest.fixture
def mock_response():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"id": 1, "name": "test", "value": "test_value"}
    return mock


# Tests
def test_client_initialization(client, base_url, test_headers):
    assert client.base_url == base_url
    assert client.model_class == TestModel
    assert client.default_headers == test_headers
    assert client.auth is None


def test_merge_headers(client, test_headers):
    additional_headers = {"Content-Type": "application/json"}
    merged = client._merge_headers(additional_headers)
    assert merged == {**test_headers, **additional_headers}


@patch('requests.post')
def test_create(mock_post, client, mock_response):
    mock_post.return_value = mock_response
    data = {"name": "test", "value": "test_value"}

    result = client.create(data)

    assert isinstance(result, TestModel)
    assert result.id == 1
    assert result.name == "test"
    mock_post.assert_called_once()


@patch('requests.get')
def test_read_single(mock_get, client, mock_response):
    mock_get.return_value = mock_response

    result = client.read(1)

    assert isinstance(result, TestModel)
    assert result.id == 1
    mock_get.assert_called_once()


@patch('requests.get')
def test_read_list(mock_get, client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 1, "name": "test1", "value": "value1"},
        {"id": 2, "name": "test2", "value": "value2"}
    ]
    mock_get.return_value = mock_response

    result = client.read()

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, TestModel) for item in result)
    mock_get.assert_called_once()


@patch('requests.put')
def test_update(mock_put, client, mock_response):
    mock_put.return_value = mock_response
    data = {"name": "updated", "value": "updated_value"}

    result = client.update(1, data)

    assert isinstance(result, TestModel)
    assert result.id == 1
    mock_put.assert_called_once()


@patch('requests.delete')
def test_delete(mock_delete, client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    mock_delete.return_value = mock_response

    result = client.delete(1)

    assert result is True
    mock_delete.assert_called_once()


def test_handle_response_client_error(client):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"detail": "Bad Request"}
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

    with pytest.raises(ValueError, match="Client error: Bad Request"):
        client._handle_response(mock_response)


def test_handle_response_server_error(client):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

    with pytest.raises(ConnectionError, match="Server error:"):
        client._handle_response(mock_response)

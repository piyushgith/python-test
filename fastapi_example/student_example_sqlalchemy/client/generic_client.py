import requests
from typing import Optional, Dict, Any, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class GenericAPIClient(Generic[T]):
    def __init__(self, base_url: str, model_class: type[T], headers: Optional[Dict[str, str]] = None, 
                 username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the generic API client
        
        Args:
            base_url (str): The base URL of the API
            model_class (type[T]): The Pydantic model class to use for serialization/deserialization
            headers (Optional[Dict[str, str]]): Default headers to include in all requests
            username (Optional[str]): Username for HTTP Basic Authentication
            password (Optional[str]): Password for HTTP Basic Authentication
        """
        self.base_url = base_url.rstrip('/')
        self.model_class = model_class
        self.default_headers = headers or {}
        self.auth = requests.auth.HTTPBasicAuth(username, password) if username and password else None

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if 400 <= response.status_code < 500:
                error_detail = response.json().get('detail', str(e))
                raise ValueError(f"Client error: {error_detail}")
            elif 500 <= response.status_code < 600:
                raise ConnectionError(f"Server error: {str(e)}")
            else:
                raise

    def _merge_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Merge default headers with additional headers"""
        headers = self.default_headers.copy()
        if additional_headers:
            headers.update(additional_headers)
        return headers

    def create(self, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> T:
        """
        Create a new resource
        
        Args:
            data (Dict[str, Any]): The data to create the resource with
            headers (Optional[Dict[str, str]]): Additional headers for this request
            
        Returns:
            T: The created resource
        """
        try:
            response = requests.post(
                f"{self.base_url}",
                json=data,
                headers=self._merge_headers(headers),
                auth=self.auth
            )
            result = self._handle_response(response)
            return self.model_class.model_validate(result)
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to create resource: {str(e)}")
        except ValueError as e:
            raise
        except Exception as e:
            raise RuntimeError(f"Unexpected error creating resource: {str(e)}")

    def read(self, resource_id: Optional[int] = None, params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> T | list[T]:
        """
        Read a resource or list of resources
        
        Args:
            resource_id (Optional[int]): The ID of the resource to read. If None, returns all resources
            params (Optional[Dict[str, Any]]): Query parameters for the request
            headers (Optional[Dict[str, str]]): Additional headers for this request
            
        Returns:
            T | list[T]: The requested resource(s)
        """
        try:
            url = f"{self.base_url}/{resource_id}" if resource_id else self.base_url
            response = requests.get(
                url,
                params=params,
                headers=self._merge_headers(headers),
                auth=self.auth
            )
            result = self._handle_response(response)
            
            if isinstance(result, list):
                return [self.model_class.model_validate(item) for item in result]
            return self.model_class.model_validate(result)
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to read resource: {str(e)}")
        except ValueError as e:
            raise
        except Exception as e:
            raise RuntimeError(f"Unexpected error reading resource: {str(e)}")

    def update(self, resource_id: int, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> T:
        """
        Update a resource
        
        Args:
            resource_id (int): The ID of the resource to update
            data (Dict[str, Any]): The data to update the resource with
            headers (Optional[Dict[str, str]]): Additional headers for this request
            
        Returns:
            T: The updated resource
        """
        try:
            response = requests.put(
                f"{self.base_url}/{resource_id}",
                json=data,
                headers=self._merge_headers(headers),
                auth=self.auth
            )
            result = self._handle_response(response)
            return self.model_class.model_validate(result)
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to update resource: {str(e)}")
        except ValueError as e:
            raise
        except Exception as e:
            raise RuntimeError(f"Unexpected error updating resource: {str(e)}")

    def delete(self, resource_id: int, headers: Optional[Dict[str, str]] = None) -> bool:
        """
        Delete a resource
        
        Args:
            resource_id (int): The ID of the resource to delete
            headers (Optional[Dict[str, str]]): Additional headers for this request
            
        Returns:
            bool: True if deletion was successful
        """
        try:
            response = requests.delete(
                f"{self.base_url}/{resource_id}",
                headers=self._merge_headers(headers),
                auth=self.auth
            )
            result = self._handle_response(response)
            return result.get('ok', False)
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to delete resource: {str(e)}")
        except ValueError as e:
            raise
        except Exception as e:
            raise RuntimeError(f"Unexpected error deleting resource: {str(e)}")

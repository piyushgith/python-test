import requests
import sqlite3
from datetime import datetime
import json

class APIClient:
    def __init__(self, db_path='api_responses.db'):
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        """Create the responses table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endpoint TEXT NOT NULL,
                    request_data TEXT,
                    response_data TEXT,
                    status_code INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def make_post_request(self, url, data):
        """
        Make a POST request and save the response to the database
        
        Args:
            url (str): The API endpoint URL
            data (dict): The data to send in the POST request
            
        Returns:
            dict: The response from the API
        """
        try:
            # Make the POST request
            response = requests.post(url, json=data)
            
            # Save to database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO api_responses (endpoint, request_data, response_data, status_code)
                    VALUES (?, ?, ?, ?)
                ''', (
                    url,
                    json.dumps(data),
                    response.text,
                    response.status_code
                ))
                conn.commit()
            
            # Return the response
            return {
                'status_code': response.status_code,
                'response': response.json() if response.text else None
            }
            
        except requests.RequestException as e:
            print(f"Error making request: {e}")
            return {'error': str(e)}
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

# Example usage
if __name__ == '__main__':
    # Create an instance of the APIClient
    client = APIClient()
    
    # Example POST request to a test API
    test_url = 'https://jsonplaceholder.typicode.com/posts'
    test_data = {
        'title': 'Test Post',
        'body': 'This is a test post',
        'userId': 1
    }
    
    # Make the request
    result = client.make_post_request(test_url, test_data)
    
    # Print the result
    print("API Response:", json.dumps(result, indent=2))

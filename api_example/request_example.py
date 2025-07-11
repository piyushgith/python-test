import requests
import json
from datetime import date
from datetime import timedelta
import time
# Assuming api_client.py is in the same directory

base_url="http://127.0.0.1:8000/employees/"


class EmployeeAPIClient:

    def create_multiple_employee_records(self, num_records=50):
        """
        Creates multiple employee records by making 50 POST calls.
        """
        print(f"Attempting to create {num_records} employee records...")
        responses = []
        for i in range(1, num_records + 1):
            employee_data = {
                "name": f"Employee {i}",
                "email": f"employee{i}@example.com",
                "position": f"Position {i % 5 + 1}",
                "startDate": (date.today() - timedelta(days=i*10)).isoformat(),
                "endDate": (date.today() + timedelta(days=i*365)).isoformat() # Random end date up to 20 years in the future
            }
            print(f"Making POST request to {base_url} with data: {employee_data}")
            # Make the POST request to create the employee record
            try:
                response = requests.post(base_url, json=employee_data)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                print(f"Response for employee {i}: {response.status_code} - {response.text}")
                responses.append(response)
                print(f"Successfully created employee {i} with ID: {response.json().get('id')}")
            except requests.exceptions.HTTPError as e:
                print(f"Failed to create employee {i} due to HTTP error: {e.response.status_code} - {e.response.text}")
                responses.append(e.response) # Append the response that caused the error
            except requests.exceptions.RequestException as e:
                print(f"Failed to create employee {i} due to request error: {e}")
                responses.append({'error': str(e)}) # Append a dictionary with error info

        print(f"Finished creating {num_records} employee records.")
        return responses

if __name__ == '__main__':
    # Ensure your FastAPI server (server.py) is running on http://127.0.0.1:8000
    # before running this script.
    print("Starting to create employee records...")
    t1=time.time()
    employee_client = EmployeeAPIClient()
    employee_client.create_multiple_employee_records()
    t2=time.time()
    print(f"Time taken to create employee records: {t2 - t1} seconds")
    print("Employee records creation process completed.")
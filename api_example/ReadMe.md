## `api_example`

This project implements a FastAPI server for managing employee records with CRUD operations.

- **Persistent Storage**: Uses SQLite for persistent storage, managed by `employee.py`.
- **API Clients**: Includes synchronous (`request_example.py`) and asynchronous (`request_aio_example.py`) API clients for testing endpoints.
- **Server Logic**: See `server.py` for API routes and logic.
- **(Swagger UI)**:  `http://127.0.0.1:8000/docs`

To run the FastAPI server, navigate to the directory containing your `server.py` file (or whatever you've named your FastAPI application file) in your terminal or command prompt.

Then, execute the following command:

```
python -m venv venv; venv/Scripts/activate.ps1; pip install -r requirements.txt;
```

**Explanation:**
go to api_example folder

```bash
uvicorn server:app --reload
```



**Explanation:**

*   **`uvicorn`**: This is the ASGI server that FastAPI uses.
*   **`server:app`**:
    *   `server`: Refers to the Python file `server.py`.
    *   `app`: Refers to the FastAPI application instance (e.g., `app = FastAPI()`) within `server.py`.
*   **`--reload`**: This flag tells Uvicorn to automatically reload the server whenever you make changes to your code, which is very useful during development.

**Example:**

If your FastAPI application is in `api_example/server.py`, and you are in the `api_example` directory, you would run:

```bash

uvicorn server:app --reload

```

After running the command, you should see output indicating that the server is running, typically on `http://127.0.0.1:8000`. You can then open your web browser and go to that address to see your API. For the interactive API documentation (Swagger UI), go to `http://127.0.0.1:8000/docs`.

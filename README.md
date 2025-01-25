# sfx

## Description
A application designed to play sound effects via requests to an API.

## Requirements
- Python >= 3.13

## Dependencies
- fastapi[standard] >= 0.115.6
- pygame >= 2.6.1
- sqlmodel >= 0.0.22
- streamlit >= 1.41.1

## Installation
1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd sfx
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
### Running the Backend
To run the FastAPI backend, use the following command:
```sh
uvicorn backend:app --reload
```
## Project Structure

```
sfx/
├── .gitignore
├── backend.py
├── frontend.py
├── pyproject.toml
├── README.md
└── uv.lock
```
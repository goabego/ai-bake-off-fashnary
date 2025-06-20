# Fashionary Installation Guide

This guide provides step-by-step instructions for setting up both the backend (FastAPI/Poetry) and frontend (Next.js/npm) environments for the Fashionary application.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python:** Version 3.8 or higher.
-   **Poetry:** A dependency management and packaging tool for Python. If you don't have it, follow the [official Poetry installation instructions](https://python-poetry.org/docs/#installation).
-   **Node.js:** Version 18 or later is recommended. This includes npm (Node Package Manager). You can download it from [nodejs.org](https://nodejs.org/).
-   **Docker:** (Optional) Required if you plan to use containerized deployment or run the Docker-specific tests. Get Docker from [docker.com](https://www.docker.com/get-started).
-   **Git:** For cloning the repository.

## Backend Setup (FastAPI)

The backend is built with FastAPI and managed with Poetry.

1.  **Clone the Repository:**
    If you haven't already, clone the project repository to your local machine:
    ```bash
    git clone https://github.com/goabego/ai-bake-off-fashnary
    cd ai-bake-off-fashnary
    ```

2.  **Install Backend Dependencies:**
    Navigate to the project's root directory (where the `pyproject.toml` file for Poetry is located). Run the following command to install the Python dependencies required for the backend:
    ```bash
    poetry install
    ```
    This command creates a virtual environment (if one doesn't exist) and installs all packages listed in `pyproject.toml` and `poetry.lock`.

3.  **Run the API Server:**
    You can start the FastAPI server in a couple of ways:

    *   **From the project root directory:**
        This command tells Uvicorn where to find the FastAPI application instance (`backend.api:app`).
        ```bash
        poetry run uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
        ```
    *   **Or, by first navigating into the `backend` directory:**
        ```bash
        cd backend
        poetry run uvicorn api:app --reload --host 0.0.0.0 --port 8000
        ```

    **Explanation of options:**
    -   `poetry run`: Executes the command within the Poetry-managed virtual environment.
    -   `uvicorn`: The ASGI server used to run FastAPI.
    -   `backend.api:app` (or `api:app`): Specifies the location of the FastAPI app instance (`app`) inside the `api.py` file within the `backend` directory.
    -   `--reload`: Enables auto-reloading of the server when code changes are detected. This is useful for development.
    -   `--host 0.0.0.0`: Makes the server accessible from other devices on your network (not just `localhost`).
    -   `--port 8000`: Specifies the port on which the server will listen.

    Once started, the API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc).

## Frontend Setup (Next.js)

The frontend is a Next.js application.

1.  **Navigate to the Frontend Directory:**
    From the project's root directory, change into the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  **Install Frontend Dependencies:**
    Inside the `frontend` directory, run the following command to install the Node.js dependencies listed in `package.json`:
    ```bash
    npm install
    ```
    (If you prefer using Yarn: `yarn install`)

3.  **Run the Frontend Development Server:**
    Once the dependencies are installed, start the Next.js development server:
    ```bash
    npm run dev
    ```
    (If you prefer using Yarn: `yarn dev`)

    This command will typically start the frontend application, and it will be accessible in your web browser at `http://localhost:3000`. The development server also supports hot reloading, so changes you make to the frontend code will be reflected in the browser automatically.

With both the backend and frontend servers running, you should be able to access and interact with the full Fashionary application.

# Fashionary Testing Guide

This document outlines how to run the various tests included in the Fashionary project to help ensure the backend functionality is working as expected.

## Backend API Tests (`backend/api_test.sh`)

A shell script located at `backend/api_test.sh` is provided to test the live backend API endpoints. This script uses `curl` to make HTTP requests to the running API server and `jq` (a command-line JSON processor) to validate the structure and presence of JSON in the responses.

### Prerequisites for API Tests:

1.  **Backend Server Running:** Ensure the FastAPI backend server is running. You can start it by following the instructions in the [INSTALLATION.md](./INSTALLATION.md#backend-setup) guide. Typically, it runs on `http://localhost:8000`.
2.  **`jq` Installed:** The `jq` utility is required to parse and validate JSON responses. If you don't have `jq` installed, you'll need to install it for your system:
    *   **macOS (using Homebrew):**
        ```bash
        brew install jq
        ```
    *   **Debian/Ubuntu:**
        ```bash
        sudo apt-get update
        sudo apt-get install jq
        ```
    *   **Other Systems:** Refer to the [official jq installation instructions](https://stedolan.github.io/jq/download/).

### Running the API Tests:

1.  **Navigate to the `backend` Directory:**
    From the project's root directory, change into the `backend` directory:
    ```bash
    cd backend
    ```

2.  **Make the Script Executable (One-time setup):**
    If you haven't run the script before, you might need to make it executable:
    ```bash
    chmod +x api_test.sh
    ```

3.  **Execute the Test Script:**
    Run the script from within the `backend` directory:
    ```bash
    ./api_test.sh
    ```

The script will iterate through a predefined list of API endpoints, print the status of each test (Pass/Fail), and provide a summary at the end indicating the total number of tests, passes, and failures.

## Docker Tests (`.docker-test.sh`)

A script named `.docker-test.sh` is located at the root of the project. This script is designed to build the backend Docker image using `backend/Dockerfile` and then attempt to run a container from that image. This helps verify that the backend application can be containerized correctly.

### Prerequisites for Docker Tests:

1.  **Docker Installed and Running:** Ensure Docker Desktop or Docker Engine is installed and the Docker daemon is running on your system. You can get Docker from [docker.com](https://www.docker.com/get-started).

### Running the Docker Tests:

1.  **Navigate to the Project Root Directory:**
    Ensure you are in the main `ai-bake-off-fashnary` directory.

2.  **Make the Script Executable (One-time setup):**
    If needed, make the script executable:
    ```bash
    chmod +x .docker-test.sh
    ```

3.  **Execute the Docker Test Script:**
    ```bash
    ./.docker-test.sh
    ```

This script will perform the following actions:
-   Build a Docker image using `backend/Dockerfile` and tag it as `backend:latest`.
-   Attempt to run a Docker container from the `backend:latest` image. The script currently uses the command `docker run -p 8080:8080 backend:latest`.

**Note on Port Mapping:** The FastAPI application inside the Docker container (as defined in `backend/Dockerfile`) listens on port `8000`. The `.docker-test.sh` script maps port `8080` on your host to port `8080` in the container. If you intend to access the API running inside this Docker container from your host machine, you might want to adjust the port mapping in the script to `docker run -p <host_port>:8000 backend:latest` (e.g., `docker run -p 8080:8000 backend:latest` to access it via `http://localhost:8080`). The script's primary purpose here is to check if the container *runs*, not necessarily to ensure it's accessible on a specific port without modification.

---

Running these tests periodically, especially after making changes to the backend code or Docker configuration, is a good practice to catch potential issues early.

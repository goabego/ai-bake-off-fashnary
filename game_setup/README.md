# Game Setup Utilities

This directory contains scripts and resources used for generating and managing the mock databases (`product_database.json`, `users_database.json`) and associated images used by the Fashionary application.

The primary purpose of these utilities is to initialize the datasets. If you need to regenerate, customize, or understand the origin of the data, the scripts in this directory are your starting point.

## Key Files and Scripts

-   **`config.py`**:
    A Python configuration file. Likely holds settings used by the database generation scripts, such as paths, default values, or parameters for data generation.

-   **`generate_products_db.py`**:
    A Python script responsible for generating the `product_database.json` file located in the `../db/` directory. It likely uses images from `game_setup/images/products/` and configuration from `config.py`.
    *Usage (example):* `python generate_products_db.py` (ensure dependencies from `pyproject.toml` are installed, e.g., in a Poetry shell).

-   **`generate_users.py`**:
    A Python script responsible for generating the `users_database.json` file located in the `../db/` directory. It likely uses images from `game_setup/images/users/` and configuration from `config.py`.
    *Usage (example):* `python generate_users.py` (ensure dependencies are installed).

-   **`images.py`**:
    A Python script, possibly containing helper functions or logic related to image processing, selection, or path manipulation used by the database generation scripts.

-   **`update_image_paths.py`**:
    A utility script to update image paths within the database files. This might be useful if image locations change or need to be standardized.
    *Usage (example):* Inspect the script for specific arguments it might take, e.g., `python update_image_paths.py --datapath ../db/product_database.json ...`

-   **`update_uuids.py`**:
    A utility script to update UUIDs (Unique Universal Identifiers) in the database files. This could be for refreshing IDs or ensuring uniqueness after modifications.
    *Usage (example):* Inspect the script for its specific command-line arguments.

-   **`python-test-backend.py`**:
    A Python script for testing the backend API. This offers an alternative or supplementary set of tests to the shell script `backend/api_test.sh`.
    *Usage (example):* `python python-test-backend.py` (ensure the backend server is running).

-   **`vertex-imagen-test.py`**:
    A Python script likely used for testing or demonstrating capabilities related to Google Cloud's Vertex AI Imagen service, possibly for image generation or analysis. The `imagen-*.png` files in this directory might be related to this script.

-   **`images/` (directory)**:
    This subdirectory contains:
    -   `images/products/`: Source images for various products.
    -   `images/users/`: Source images for user profiles.
    -   Other images (e.g., `imagen-*.png`): Likely related to tests or demonstrations of image generation capabilities.
    These images are used by the generation scripts to populate the `image_path` and `image_url` fields in the databases. The actual images served by the application are typically copied to or referenced from the root `images/` directory.

-   **`product_database.json` / `users_database.json` (local copies)**:
    This directory may contain local copies or backups of the database files. The canonical databases used by the running application are located in the `../db/` directory. These local versions might be used as a base for the generation scripts or for comparison.

-   **`pyproject.toml` / `poetry.lock`**:
    These files define the Python dependencies for the scripts within the `game_setup` directory, managed by Poetry. To run these scripts, you'll typically need to install these dependencies first (e.g., by running `poetry install` from within this directory, or ensuring the project root's Poetry environment includes them if they are shared).

## General Workflow for Data Regeneration
1.  Install dependencies: `poetry install` (if this directory is a separate Poetry project, or if the root project's Poetry setup doesn't cover these specific scripts' needs).
2.  Modify `config.py` or the generation scripts (`generate_products_db.py`, `generate_users.py`) as needed.
3.  Run the generation scripts to update the JSON files in the `../db/` directory.
4.  Use utility scripts like `update_image_paths.py` or `update_uuids.py` if further modifications are required.

Always ensure you understand what each script does before running it, especially if it modifies data in the main `../db/` directory.

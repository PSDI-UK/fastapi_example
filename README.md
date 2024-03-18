# Example FastAPI Application with MongoDB

This is an example application that demonstrates how to use FastAPI to create a REST API that interacts with a MongoDB database. It serves as a standalone API and does not include any view logic. It can be utilized alongside a Web App, such as React and AngularJS. It showcases the use of similar data structures - Python dictionaries in the API, BSON in the database and the UI will be using JSON.

## Features

- **MongoDB Integration:** Utilizes the `motor` library for asynchronous interaction with MongoDB.

- **Configurable Settings:** Settings module allows configuration through environment variables or a `.env` file.

- **Logging:** Includes a pre-configured logging setup located in the `utils` directory.

- **Example Routes:** Demonstrates basic CRUD operations on a MongoDB collection through example routes in the `item` and `product` modules.

- **Unit Tests:** Comes with a suite of tests to verify route functionality.

- **CORS Middleware:** Configured to allow requests from any origin, facilitating integration with a Web App.

## Setup

Ensure you have Python 3.10 or higher installed. Follow these steps to set up your environment:

```bash
# Create a virtual environment
python3 -m venv apienv

# Activate the virtual environment
source ./apienv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install the required dependencies
pip install -r requirements_dev.txt
```

To run the application in a development setting, execute the bash script located in `scripts/`. You can set config options by using environmental variables eg. for the MongoDB connection string.

```bash
export MONGO_CONNECTION_STRING='your_mongo_connection_string'

./scripts/run_dev.sh
```

## Tests
To run the tests, use the following command:

```bash
./scripts/run_tests.sh
```

The tests are run with code coverage. You can view a simple report or a HTML version which appears in a htmlcov/ directory.


```bash
coverage report
coverage html
```

## Documentation
FastAPI automatically generates interactive API documentation using Swagger UI and ReDoc. The API documentation can be accessed at http://host.ac.uk/docs or http://host.ac.uk/redoc.


## Environment Variables

The application uses the following environment variables for configuration:

- `MONGODB_URL`: The connection string for the MongoDB database. Default is `mongodb://localhost:27017/mydatabase`.

- `LOG_LEVEL`: The level of logging. Can be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Default is `DEBUG`.

- `MODE`: The mode the application is running in. Can be one of `TEST`, `DEV`, `LIVE`. `TEST` disables attempts to access a remote database, `DEV` enables Docs and `LIVE` disables Docs.

- `ALLOW_ORIGINS`: The origins that are allowed to make requests. This needs to be set when used in conjunction with a web app. Default is `http://localhost`.

These variables can be set in the environment or in a `.env` file at the root of the project. If a variable is set in both places, the environment variable takes precedence.


## Deployment with Docker

This application can be deployed using Docker, which ensures it runs the same way in every environment.

To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:

```bash
docker build -t api .
```

This will create a Docker image named api. 

To run the application, use the following command:

```bash
docker run -p 80:80 api
```

## GitHub Actions

This repository also includes a GitHub Actions workflow that automatically builds a Docker image from the Dockerfile and pushes it to a Harbor repository whenever changes are pushed to main. You can find this workflow in the .github/workflows/docker-publish.yml file. Please ensure to replace the placeholder values with your Docker Hub username and repository name. This can be done using GitHub secrets.

## Files

- `api/`: The main directory for the API
  - `Dockerfile`: Dockerfile for building the API container
  - `src/`: Directory containing the source code of the API
    - `main.py`: The main Python script that starts the FastAPI server and includes the API routes
    - `api/`: Contains a directory for each section of the API
      - `item/`: Represents the top level route /item
        - `routes.py`: Contains all the endpoints for /item. All the GETS, POSTS...
        - `models.py`: Contains the pydantic models used for the /item routes
      - `product/`: Represents the top level route /product
        - ...
    - `utils/`: This directory contains common app logic
      - `database.py`: Contains database connection logic and helper functions
      - `log_config.py`: Configures the logger - level, formatting...
      - `settings.py`: Contains the pydantic model used for input settings such as database connection details
  - `tests/`: Directory containing unit tests for the API
    - `conftest.py`: Standard pytest file for providing fixtures for the tests
    - `test_item.py`: Contains unit tests for the /item routes
    - `test_product.py`: ...
  - `requirements.txt`: This file lists the Python dependencies required to run the application in production
  - `dev_requirements.txt`: This file includes all the dependencies from `requirements.txt` and also dependencies used in development
1. **Clone the Repository:**

 ```bash
   git clone https://github.com/shilpacvenugopal/docker.git
   ```
```bash
   cd docker/
   ```

# Dockerized Python Microservices Application

This project is a Dockerized Python-based microservices application that focuses on user authentication, API key generation, and activity logging across three microservices.

## Microservices Overview

### Data Service
- **Purpose:** Handle user authentication.
- **Endpoints:**
  - `/register` (POST): Register a new user.
  - `/token` (POST): Get an access token by providing username and password.
- **Authentication:** Token-based authentication.
- **Storage:** In-memory structure or a simple database for storing user credentials.

### Processing Service
- **Purpose:** Generate an API key for registered users.
- **Endpoint:**
  - `/generate-api-key` (GET): Generate a random API key (requires user authentication).

### Logging Service
- **Purpose:** Log user activities across services.
- **Endpoints:**
  - `/log` (POST): Log activities such as registration, login, and API key generation.
  - `/logs` (GET): Get a list of logged activities.
- **Storage:** In-memory storage for logged activities.

## Inter-Service Communication

- Data services communicate with the Logging Service to log activities (register, login, API key generation).
- Secure communication and data handling between services are implemented.

## Docker Setup

### Building Services

To build the services, use the following commands:

```bash
docker-compose build
```

### Running Services

To run the services, use the following commands:

```bash
docker-compose up
```

The services will be accessible at the following ports:
- Data Service: http://localhost:5000
- Processing Service: http://localhost:5001
- Logging Service: http://localhost:5002

## API Endpoints and Usage

### Data Service

- **Register a User:**
  - Endpoint: `/register` (POST)
  - Request Body: JSON with `username` and `password`.
  - url:
    ```bash
     http://localhost:5000/register
    ```

- **Get Access Token:**
  - Endpoint: `/token` (POST)
  - Request Body: Form data with `username` and `password`.
  - url:
    ```bash
    http://localhost:5000/token
    ```

### Processing Service

- **Generate API Key:**
  - Endpoint: `/generate-api-key` (GET)
  - Requires an access token obtained from the Data Service.
  - url:
    ```bash
  http://localhost:5001/generate-api-key
    ```

### Logging Service

- **Log Activity:**
  - Endpoint: `/log` (POST)
  - Request Body: JSON with `activity` and `username`.
  - url:
    ```bash
     http://localhost:5002/log
    ```

- **Get Logs:**
  - Endpoint: `/logs` (GET)
  - url:
    ```bash
     http://localhost:5002/logs
    ```


Feel free to customize this README.md file based on your specific project details and preferences.

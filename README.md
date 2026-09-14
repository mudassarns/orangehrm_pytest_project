This project demonstrates UI, API, database, and hybrid test automation.

# OrangeHRM Pytest Automation Framework

## Running OrangeHRM with Docker

The project uses a local Docker-based OrangeHRM environment for UI, API, and database testing.

### Starting OrangeHRM

After restarting the laptop, make sure Docker Desktop is running before starting the OrangeHRM containers.

Start the containers in detached mode:

    docker compose --env-file .env -f docker-orangehrm\docker-compose.yml up -d

Verify the containers:

    docker compose --env-file .env -f docker-orangehrm\docker-compose.yml ps

Expected services:

- `orangehrm` → available at http://localhost:8080
- `mariadb` → available at localhost:3306

The `--env-file .env` option explicitly loads the project's root `.env` file, which contains the Docker database credentials.

### Docker data persistence

The MariaDB database uses a Docker named volume to persist data.

Stopping containers or restarting the laptop does not delete the database.

To stop the containers:

    docker compose --env-file .env -f docker-orangehrm\docker-compose.yml down

The database volume is preserved.

To stop the containers and delete the database volume:

    docker compose --env-file .env -f docker-orangehrm\docker-compose.yml down -v

> `docker compose down -v` deletes the MariaDB volume and resets the OrangeHRM database. Use it only when a fresh database installation is required.

### Docker Compose configuration

The Docker environment is defined in:

    docker-orangehrm/docker-compose.yml

The Compose setup contains:

- OrangeHRM 5.9 application container
- MariaDB 11 database container
- Persistent MariaDB Docker volume
- OrangeHRM exposed on port 8080
- MariaDB exposed on port 3306

### Environment configuration

Docker database credentials are stored in the project's `.env` file and are not committed to Git.

The application and test framework also use environment-specific configuration through `.env`.

The current local QA environment uses the Docker-based OrangeHRM instance:

    QA_ORANGEHRM_BASE_URL=http://localhost:8080

### Useful Docker commands

Check container status:

    docker compose --env-file .env -f docker-orangehrm\docker-compose.yml ps

View all container logs:

    docker compose --env-file .env -f docker-orangehrm\docker-compose.yml logs

View OrangeHRM logs:

    docker compose --env-file .env -f docker-orangehrm\docker-compose.yml logs orangehrm

View MariaDB logs:

    docker compose --env-file .env -f docker-orangehrm\docker-compose.yml logs mariadb

### Running the test suite

Make sure Docker Desktop is running and the OrangeHRM and MariaDB containers are up before running the tests.

Run the complete test suite:

    pytest -v

Run tests in parallel:

    pytest -n 4 -v

Run tests against a specific environment:

    pytest -v --env qa